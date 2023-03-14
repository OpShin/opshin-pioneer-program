import time

import click
from pycardano import (
    OgmiosChainContext,
    Network,
    Address,
    TransactionBuilder,
    TransactionOutput,
    VerificationKeyHash,
)

from src.utils import get_address, get_signing_info
from src.week03 import assets_dir
from src.week03.lecture.vesting import VestingParams


@click.command()
@click.argument("name")
@click.argument("beneficiary")
@click.option(
    "--amount",
    type=int,
    default=3000000,
    help="Amount of lovelace to send to the script address.",
)
@click.option(
    "--wait_time",
    type=int,
    default=0,
    help="Time to wait in seconds for the validation to succeed.",
)
def main(name: str, beneficiary: str, amount: int, wait_time: int):
    # Load chain context
    context = OgmiosChainContext("ws://localhost:1337", network=Network.TESTNET)

    # Load script info
    with open(assets_dir.joinpath("vesting", "testnet.addr")) as f:
        script_address = Address.from_primitive(f.read())

    # Get payment address
    payment_address = get_address(name)

    # Get the beneficiary VerificationKeyHash (PubKeyHash)
    beneficiary_address = get_address(beneficiary)
    vkey_hash: VerificationKeyHash = beneficiary_address.payment_part

    # Create the vesting datum
    datum = VestingParams(
        beneficiary=bytes(vkey_hash),
        deadline=int(time.time() + wait_time) * 1000,  # must be in milliseconds
    )

    # Build the transaction
    builder = TransactionBuilder(context)
    builder.add_input_address(payment_address)
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
