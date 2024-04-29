from functools import cache
from typing import Optional

import pyaiken
import pycardano
import uplc
from opshin.prelude import *
from pycardano import (
    ScriptHash,
    RedeemerTag,
    Address,
    ChainContext,
    plutus_script_hash,
    datum_hash,
    PlutusV2Script,
    UTxO,
)
from src.utils import network


def to_staking_credential(
    sk: Union[
        pycardano.VerificationKeyHash,
        pycardano.ScriptHash,
        pycardano.PointerAddress,
        None,
    ]
):
    try:
        return SomeStakingCredential(to_staking_hash(sk))
    except NotImplementedError:
        return NoStakingCredential()


def to_staking_hash(
    sk: Union[
        pycardano.VerificationKeyHash, pycardano.ScriptHash, pycardano.PointerAddress
    ]
):
    if isinstance(sk, pycardano.PointerAddress):
        return StakingPtr(sk.slot, sk.tx_index, sk.cert_index)
    if isinstance(sk, pycardano.VerificationKeyHash):
        return StakingHash(PubKeyCredential(sk.payload))
    if isinstance(sk, pycardano.ScriptHash):
        return StakingHash(ScriptCredential(sk.payload))
    raise NotImplementedError(f"Unknown stake key type {type(sk)}")


def to_wdrl(wdrl: Optional[pycardano.Withdrawals]) -> Dict[StakingCredential, int]:
    if wdrl is None:
        return {}

    def m(k: bytes):
        sk = pycardano.Address.from_primitive(k).staking_part
        return to_staking_hash(sk)

    return {m(key): val for key, val in wdrl.to_primitive().items()}


def to_valid_range(validity_start: Optional[int], ttl: Optional[int], posix_from_slot):
    if validity_start is None:
        lower_bound = LowerBoundPOSIXTime(NegInfPOSIXTime(), FalseData())
    else:
        start = posix_from_slot(validity_start) * 1000
        lower_bound = LowerBoundPOSIXTime(FinitePOSIXTime(start), TrueData())
    if ttl is None:
        upper_bound = UpperBoundPOSIXTime(PosInfPOSIXTime(), FalseData())
    else:
        end = posix_from_slot(ttl) * 1000
        upper_bound = UpperBoundPOSIXTime(FinitePOSIXTime(end), TrueData())
    return POSIXTimeRange(lower_bound, upper_bound)


def to_pubkeyhash(vkh: pycardano.VerificationKeyHash):
    return PubKeyHash(vkh.payload)


def to_tx_id(tx_id: pycardano.TransactionId):
    return TxId(tx_id.payload)


def to_dcert(c: pycardano.Certificate) -> DCert:
    raise NotImplementedError("Can not convert certificates yet")


def multiasset_to_value(ma: pycardano.MultiAsset) -> Value:
    if ma is None:
        return {b"": {b"": 0}}
    return {
        PolicyId(policy_id): {
            TokenName(asset_name): quantity for asset_name, quantity in asset.items()
        }
        for policy_id, asset in ma.to_shallow_primitive().items()
    }


def value_to_value(v: pycardano.Value):
    ma = multiasset_to_value(v.multi_asset)
    ma[b""] = {b"": v.coin}
    return ma


def to_payment_credential(
    c: Union[pycardano.VerificationKeyHash, pycardano.ScriptHash]
):
    if isinstance(c, pycardano.VerificationKeyHash):
        return PubKeyCredential(PubKeyHash(c.payload))
    if isinstance(c, pycardano.ScriptHash):
        return ScriptCredential(ValidatorHash(c.payload))
    raise NotImplementedError(f"Unknown payment key type {type(c)}")


def to_tx_out(o: pycardano.TransactionOutput):
    if o.datum is not None:
        output_datum = SomeOutputDatum(o.datum)
    elif o.datum_hash is not None:
        output_datum = SomeOutputDatumHash(o.datum_hash.payload)
    else:
        output_datum = NoOutputDatum()
    if o.script is None:
        script = NoScriptHash()
    else:
        script = SomeScriptHash(pycardano.script_hash(o.script).payload)
    return TxOut(
        o.address,
        value_to_value(o.amount),
        output_datum,
        script,
    )


def to_tx_out_ref(i: pycardano.TransactionInput):
    return TxOutRef(
        TxId(i.transaction_id.payload),
        i.index,
    )


def to_tx_in_info(i: pycardano.TransactionInput, o: pycardano.TransactionOutput):
    return TxInInfo(
        to_tx_out_ref(i),
        to_tx_out(o),
    )


def to_redeemer_purpose(r: pycardano.Redeemer, tx_body: pycardano.TransactionBody):
    v = r.tag
    if v == pycardano.RedeemerTag.SPEND:
        spent_input = tx_body.inputs[r.index]
        return Spending(to_tx_out_ref(spent_input))
    elif v == pycardano.RedeemerTag.MINT:
        minted_id = sorted(tx_body.mint.data.keys())[r.index]
        return Minting(PolicyId(minted_id.payload))
    elif v == pycardano.RedeemerTag.CERT:
        # TODO: fix redeemer purpose
        return Certifying(None)
    elif v == pycardano.RedeemerTag.REWARD:
        # TODO: fix redeemer purpose
        return Rewarding(None)
    else:
        raise NotImplementedError()


def to_tx_info(
    tx: pycardano.Transaction,
    resolved_inputs: List[pycardano.TransactionOutput],
    resolved_reference_inputs: List[pycardano.TransactionOutput],
    posix_from_slot,
):
    tx_body = tx.transaction_body
    datums = [
        o.datum
        for o in tx_body.outputs + resolved_inputs + resolved_reference_inputs
        if o.datum is not None
    ]
    if tx.transaction_witness_set.plutus_data:
        datums += tx.transaction_witness_set.plutus_data
    redeemers = (
        tx.transaction_witness_set.redeemer
        if tx.transaction_witness_set.redeemer
        else []
    )
    return TxInfo(
        [to_tx_in_info(i, o) for i, o in zip(tx_body.inputs, resolved_inputs)],
        [
            to_tx_in_info(i, o)
            for i, o in zip(tx_body.reference_inputs, resolved_reference_inputs)
        ]
        if tx_body.reference_inputs is not None
        else [],
        [to_tx_out(o) for o in tx_body.outputs],
        value_to_value(pycardano.Value(tx_body.fee)),
        multiasset_to_value(tx_body.mint),
        [to_dcert(c) for c in tx_body.certificates] if tx_body.certificates else [],
        to_wdrl(tx_body.withdraws),
        to_valid_range(tx_body.validity_start, tx_body.ttl, posix_from_slot),
        [to_pubkeyhash(s) for s in tx_body.required_signers]
        if tx_body.required_signers
        else [],
        {to_redeemer_purpose(r, tx_body): r.data for r in redeemers},
        {pycardano.datum_hash(d).payload: d for d in datums},
        to_tx_id(tx_body.id),
    )


@dataclass
class ScriptInvocation:
    script: pycardano.ScriptType
    datum: Optional[pycardano.Datum]
    redeemer: pycardano.Redeemer
    script_context: ScriptContext


def generate_script_contexts(tx_builder: pycardano.TransactionBuilder):
    """Generates for each evaluated script, with which parameters it should be called"""
    # TODO this only handles PlutusV2, no other script contexts are currently supported

    tx = tx_builder._build_full_fake_tx()
    # we assume that reference inputs are UTxO objects!
    input_to_resolved_output = {}
    for utxo in tx_builder.inputs + list(tx_builder.reference_inputs):
        assert isinstance(utxo, pycardano.UTxO)
        input_to_resolved_output[utxo.input] = utxo.output
    # input_to_resolved_output = {
    #     utxo.input: utxo.output
    #     for utxo in tx_builder.inputs + tx_builder.reference_inputs
    # }
    resolved_inputs = [
        UTxO(i, input_to_resolved_output[i]) for i in tx.transaction_body.inputs
    ]
    resolved_reference_inputs = [
        UTxO(i, input_to_resolved_output[i])
        for i in tx.transaction_body.reference_inputs
    ]
    return generate_script_contexts_resolved(
        tx, resolved_inputs, resolved_reference_inputs
    )


def generate_script_contexts_resolved(
    tx: pycardano.Transaction,
    resolved_inputs: List[UTxO],
    resolved_reference_inputs: List[UTxO],
    posix_from_slot,
):
    tx_info = to_tx_info(
        tx,
        [i.output for i in resolved_inputs],
        [i.output for i in resolved_reference_inputs],
        posix_from_slot,
    )
    datum = None
    script_contexts = []
    for i, spending_input in enumerate(resolved_inputs):
        if not isinstance(spending_input.output.address.payment_part, ScriptHash):
            continue
        try:
            spending_redeemer = next(
                r
                for r in tx.transaction_witness_set.redeemer
                if r.index == i and r.tag == RedeemerTag.SPEND
            )
        except (StopIteration, TypeError):
            raise ValueError(
                f"Missing redeemer for script input {i} (index or tag set incorrectly or missing redeemer)"
            )
        potential_scripts = tx.transaction_witness_set.plutus_v2_script or []
        for input in resolved_reference_inputs + resolved_inputs:
            if input.output.script is not None:
                potential_scripts.append(input.output.script)
        try:
            spending_script = next(
                s
                for s in tx.transaction_witness_set.plutus_v2_script
                if plutus_script_hash(PlutusV2Script(s))
                == spending_input.output.address.payment_part
            )
        except (StopIteration, TypeError):
            raise NotImplementedError(
                "Can not validate spending of non plutus v2 script (or plutus v2 script is not in context)"
            )
        if spending_input.output.datum is not None:
            datum = spending_input.output.datum
        elif spending_input.output.datum_hash is not None:
            datum_h = spending_input.output.datum_hash
            try:
                datum = next(
                    d
                    for d in tx.transaction_witness_set.plutus_data or []
                    if datum_hash(d) == datum_h
                )
            except StopIteration:
                raise ValueError(
                    f"No datum with hash '{datum_h.payload.hex()}' provided for transaction"
                )
        else:
            raise ValueError(
                "Spending input is missing an attached datum and can not be spent"
            )
        script_contexts.append(
            ScriptInvocation(
                spending_script,
                datum,
                spending_redeemer,
                ScriptContext(tx_info, Spending(to_tx_out_ref(spending_input.input))),
            )
        )
    for i, minting_script_hash in enumerate(tx.transaction_body.mint or []):
        try:
            minting_redeemer = next(
                r
                for r in tx.transaction_witness_set.redeemer
                if r.index == i and r.tag == RedeemerTag.MINT
            )
        except StopIteration:
            raise ValueError(
                f"Missing redeemer for mint {i} (index or tag set incorrectly or missing redeemer)"
            )
        try:
            minting_script = next(
                s
                for s in tx.transaction_witness_set.plutus_v2_script
                if plutus_script_hash(PlutusV2Script(s)) == minting_script_hash
            )
        except StopIteration:
            raise NotImplementedError(
                "Can not validate spending of non plutus v2 script (or plutus v2 script is not in context)"
            )

        script_contexts.append(
            ScriptInvocation(
                minting_script,
                datum,
                minting_redeemer,
                ScriptContext(
                    tx_info, Minting(pycardano.script_hash(minting_script).payload)
                ),
            )
        )
    return script_contexts


@cache
def uplc_unflat(hex: str):
    return uplc.unflatten(bytes.fromhex(hex))


def evaluate_script(script_invocation: ScriptInvocation):
    uplc_program = uplc_unflat(script_invocation.script.hex()).dumps(
        dialect=uplc.UPLCDialect.Aiken
    )
    args = [script_invocation.redeemer.data, script_invocation.script_context]
    if script_invocation.datum is not None:
        args.insert(0, script_invocation.datum)
    program_args = []
    for a in args:
        data = f"(con data #{PlutusData.to_cbor(a).hex()})"
        program_args.append(data)
    allowed_cpu_steps = script_invocation.redeemer.ex_units.steps
    allowed_mem_steps = script_invocation.redeemer.ex_units.mem
    ((suc, err), logs, (remaining_cpu_steps, remaining_mem_steps)) = pyaiken.uplc.eval(
        uplc_program, program_args, allowed_cpu_steps, allowed_mem_steps
    )
    if logs:
        print("Script debug logs:")
        print("==================")
        print("\n".join(logs))
        print("==================")
    return (
        (suc, err),
        (
            remaining_cpu_steps,
            remaining_mem_steps,
        ),
        logs,
    )


def get_ref_utxo(contract: PlutusV2Script, context: ChainContext):
    script_address = Address(payment_part=plutus_script_hash(contract), network=network)
    for utxo in context.utxos(script_address):
        if utxo.output.script == contract:
            return utxo
    return None
