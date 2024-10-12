import click
from opshin import build
from opshin.prelude import TxOutRef, TxId
from pycardano import (
    TransactionBuilder,
    TransactionOutput,
    PlutusV2Script,
    MultiAsset,
    Redeemer,
    plutus_script_hash,
    Value,
    VerificationKeyHash,
    AssetName,
    ScriptHash,
)

from src.utils import get_address, get_signing_info, get_chain_context
from src.utils.network import show_tx
from src.week05 import assets_dir, lecture_dir


@click.command()
@click.argument("wallet_name")
@click.argument("token_name")
@click.option(
    "--amount",
    type=int,
    default=1,
)
@click.option(
    "--script",
    type=click.Choice(["free", "nft", "signed"]),
    default="nft",
)
def main(
    wallet_name: str,
    token_name: str,
    amount: int,
    script: str,
):
    # Load chain context
    context = get_chain_context()

    # Get payment address
    payment_address = get_address(wallet_name)

    # Get input utxo
    utxo_to_spend = None
    for utxo in context.utxos(payment_address):
        if utxo.output.amount.coin > 3000000:
            utxo_to_spend = utxo
            break
    assert utxo_to_spend is not None, "UTxO not found to spend!"

    tn_bytes = bytes(token_name, encoding="utf-8")
    signatures = []
    if script == "nft":
        # Build script
        script_path = lecture_dir.joinpath("nft.py")
        oref = TxOutRef(
            id=TxId(bytes(utxo_to_spend.input.transaction_id)),
            idx=utxo_to_spend.input.index,
        )
        plutus_script = build(script_path, oref, tn_bytes)
    elif script == "signed":
        # Build script
        script_path = lecture_dir.joinpath("signed.py")
        pkh = bytes(get_address(wallet_name).payment_part)
        pkh2 = bytes(get_address("alice").payment_part)
        signatures.append(VerificationKeyHash(pkh))
        plutus_script = build(script_path, pkh2)
    else:
        cbor_path = assets_dir.joinpath(script, "script.cbor")
        with open(cbor_path, "r") as f:
            cbor_hex = f.read()
        cbor = bytes.fromhex(cbor_hex)
        plutus_script = PlutusV2Script(cbor)

    # Load script info
    script_hash = plutus_script_hash(plutus_script)

    # Build the transaction
    builder = TransactionBuilder(context)
    builder.add_minting_script(script=plutus_script, redeemer=Redeemer(0))
    builder.mint = MultiAsset.from_primitive({bytes(script_hash): {tn_bytes: amount}})
    if amount > 0:
        builder.add_input(utxo_to_spend)
        builder.add_output(
            TransactionOutput(
                payment_address, amount=Value(coin=2000000, multi_asset=builder.mint)
            )
        )
    else:
        assert script != "nft", "lecture nft script doesn't allow burning"
        burn_utxo = None

        def f(pi: ScriptHash, an: AssetName, a: int) -> bool:
            return pi == script_hash and an.payload == tn_bytes and a >= -amount

        for utxo in context.utxos(payment_address):
            if utxo.output.amount.multi_asset.count(f):
                burn_utxo = utxo
        builder.add_input(burn_utxo)
        assert burn_utxo, "UTxO containing token not found!"

    builder.required_signers = signatures

    # Sign the transaction
    payment_vkey, payment_skey, payment_address = get_signing_info(wallet_name)
    signed_tx = builder.build_and_sign(
        signing_keys=[payment_skey],
        change_address=payment_address,
    )

    # Submit the transaction
    context.submit_tx(signed_tx)

    show_tx(signed_tx)


if __name__ == "__main__":
    main()
