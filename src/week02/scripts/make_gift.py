import click
from pycardano import (
    OgmiosChainContext,
    Network,
    Address,
    TransactionBuilder,
    TransactionOutput,
    PlutusData,
)

from src.utils import get_address, get_signing_info
from src.week02 import assets_dir


@click.command()
@click.argument("name")
@click.option(
    "--amount",
    type=int,
    default=3000000,
    help="Amount of lovelace to send to the script address.",
)
@click.option(
    "--script",
    type=click.Choice(
        ["burn", "custom_types", "fourty_two", "fourty_two_typed", "gift"]
    ),
    default="gift",
    help="Which lecture script address to send funds to.",
)
def main(name: str, amount: int, script: str):
    # Load chain context
    context = OgmiosChainContext("ws://localhost:1337", network=Network.TESTNET)

    # Load script info
    with open(assets_dir.joinpath(script, "testnet.addr")) as f:
        script_address = Address.from_primitive(f.read())

    # Get payment address
    payment_address = get_address(name)

    # Build the transaction
    builder = TransactionBuilder(context)
    builder.add_input_address(payment_address)
    datum = PlutusData()  # Plutus Unit type
    builder.add_output(
        TransactionOutput(address=script_address, amount=amount, datum=datum)
    )

    # Sign the transaction
    payment_vkey, payment_skey, payment_address = get_signing_info(name)
    signed_tx = builder.build_and_sign(
        signing_keys=[payment_skey],
        change_address=payment_address,
    )

    # Submit the transaction
    context.submit_tx(signed_tx.to_cbor())

    print(f"transaction id: {signed_tx.id}")
    print(f"Cardanoscan: https://preview.cardanoscan.io/transaction/{signed_tx.id}")


if __name__ == "__main__":
    main()
