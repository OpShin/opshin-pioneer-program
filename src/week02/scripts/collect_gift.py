import click
from pycardano import (
    OgmiosChainContext,
    Address,
    TransactionBuilder,
    UTxO,
    PlutusV2Script,
    plutus_script_hash,
    Redeemer,
    RedeemerTag,
)

from src.utils import get_address, get_signing_info, network, ogmios_url
from src.week02 import assets_dir


@click.command()
@click.argument("name")
@click.option(
    "--script",
    type=click.Choice(
        ["burn", "custom_types", "fourty_two", "fourty_two_typed", "gift"]
    ),
    default="gift",
    help="Which lecture script address to attempt to spend.",
)
def main(name: str, script: str):
    # Load chain context
    context = OgmiosChainContext(ogmios_url, network=network)

    # Load script info
    # We need `plutus_script: PlutusV2Script` and `script_address: Address`.
    # There are multiple ways to get there but the simplest is to use "script.cbor"
    with open(assets_dir.joinpath(script, "script.cbor"), "r") as f:
        cbor_hex = f.read()

    cbor = bytes.fromhex(cbor_hex)

    # with open(assets_dir.joinpath(script, "script.plutus"), "r") as f:
    #     script_plutus = json.load(f)
    #     script_hex = script_plutus["cborHex"]
    # cbor_wrapped = cbor2.dumps(cbor)
    # cbor_wrapped_hex = cbor_wrapped.hex()
    # assert script_hex == cbor_wrapped_hex

    plutus_script = PlutusV2Script(cbor)
    script_hash = plutus_script_hash(plutus_script)
    script_address = Address(script_hash, network=network)

    # with open(assets_dir.joinpath(script, "testnet.addr")) as f:
    #     addr = Address.from_primitive(f.read())
    #     assert script_address == addr

    # Get payment address
    payment_address = get_address(name)

    # Find a script UTxO
    utxo_to_spend = None
    for utxo in context.utxos(str(script_address)):
        if utxo.output.datum:
            utxo_to_spend = utxo
            break
    assert isinstance(utxo_to_spend, UTxO), "No script UTxOs found!"

    # Find a collateral UTxO
    non_nft_utxo = None
    for utxo in context.utxos(str(payment_address)):
        # multi_asset should be empty for collateral utxo
        if not utxo.output.amount.multi_asset:
            non_nft_utxo = utxo
            break
    assert isinstance(non_nft_utxo, UTxO), "No collateral UTxOs found!"

    # Build the transaction
    # no output is specified since everything minus fees is sent to change address
    if script in ["fourty_two", "fourty_two_typed"]:
        redeemer = Redeemer(RedeemerTag.SPEND, 42)
    elif script == "custom_types":
        from src.week02.lecture.custom_types import MySillyRedeemer

        redeemer = Redeemer(RedeemerTag.SPEND, MySillyRedeemer(42))
    else:
        redeemer = Redeemer(RedeemerTag.SPEND, 0)
    builder = TransactionBuilder(context)
    builder.add_script_input(utxo_to_spend, script=plutus_script, redeemer=redeemer)
    builder.collaterals.append(non_nft_utxo)

    # Sign the transaction
    payment_vkey, payment_skey, payment_address = get_signing_info(name)
    signed_tx = builder.build_and_sign(
        signing_keys=[payment_skey],
        change_address=payment_address,
    )

    # Submit the transaction
    context.submit_tx(signed_tx.to_cbor())

    # context.submit_tx(signed_tx.to_cbor())
    print(f"transaction id: {signed_tx.id}")
    print(f"Cardanoscan: https://preview.cardanoscan.io/transaction/{signed_tx.id}")


if __name__ == "__main__":
    main()
