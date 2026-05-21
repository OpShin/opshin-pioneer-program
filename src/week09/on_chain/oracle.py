from src.week09.on_chain.common import *


@dataclass()
class AssetClass(PlutusData):
    policy_id: bytes
    token_name: bytes


@dataclass()
class OracleParams(PlutusData):
    nft: AssetClass
    operator: PubKeyHash


@dataclass()
class Update(PlutusData):
    CONSTR_ID = 1046


@dataclass()
class Delete(PlutusData):
    CONSTR_ID = 1047


OracleRedeemer = Union[Update, Delete]


def own_input(context: ScriptContext) -> TxOut:
    """Find the oracle input."""
    purpose: Spending = context.purpose
    ref = purpose.tx_out_ref
    outputs = [i.resolved for i in context.tx_info.inputs if ref == i.out_ref]
    assert len(outputs) == 1, "oracle input missing"
    return outputs[0]


def input_has_token(oracle: OracleParams, context: ScriptContext) -> bool:
    """Check that the oracle input contains the NFT."""
    tx_out = own_input(context)
    return tx_out.value[oracle.nft.policy_id][oracle.nft.token_name] == 1


def get_continuing_outputs(context: ScriptContext) -> List[TxOut]:
    """Get all the outputs that pay to the same script address we are currently spending from, if any."""
    inputs = context.tx_info.inputs
    assert len(inputs) == 1, "Can't get any continuing outputs"
    addr = inputs[0].resolved.address
    return [o for o in context.tx_info.outputs if o.address == addr]


def own_output(context: ScriptContext) -> TxOut:
    """Find the oracle output."""
    tx_outs = get_continuing_outputs(context)
    assert len(tx_outs) == 1, "expected exactly one oracle output"
    return tx_outs[0]


def output_has_token(oracle: OracleParams, own_tx_out: TxOut) -> bool:
    """Check that the oracle output contains the NFT."""
    return own_tx_out.value[oracle.nft.policy_id][oracle.nft.token_name] == 1


def check_operator_signature(oracle: OracleParams, context: ScriptContext) -> bool:
    """Check that the 'oracle' is signed by the 'oOperator'."""
    return oracle.operator in context.tx_info.signatories


def check_output_datum(own_tx_out: TxOut, context: ScriptContext) -> bool:
    """Check that the oracle output contains a valid datum."""
    datum: Rate = parse_oracle_datum_unsafe(own_tx_out, context.tx_info)
    return True


def validator(oracle: OracleParams, _: Rate, r: OracleRedeemer, context: ScriptContext):
    if isinstance(r, Update):
        own_tx_out = own_output(context)
        assert input_has_token(oracle, context), "token missing from input"
        assert output_has_token(oracle, own_tx_out), "token missing from output"
        assert check_operator_signature(oracle, context), "operator signature missing"
        assert check_output_datum(own_tx_out, context), "invalid output datum"
    elif isinstance(r, Delete):
        assert check_operator_signature(oracle, context), "operator signature missing"
