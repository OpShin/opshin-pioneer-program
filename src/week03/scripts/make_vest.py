import subprocess
import time

import click
from pycardano import (
    Address,
    TransactionBuilder,
    TransactionOutput,
    VerificationKeyHash,
    PlutusData,
)

from src.utils import get_address, get_signing_info, get_chain_context
from src.utils.network import show_tx
from src.week03 import assets_dir, lecture_dir
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
@click.option(
    "--parameterized", is_flag=True, help="If set, use parameterized vesting script."
)
def main(name: str, beneficiary: str, amount: int, wait_time: int, parameterized: bool):
    # Load chain context
    context = get_chain_context()

    # Get payment address
    payment_address = get_address(name)

    # Get the beneficiary VerificationKeyHash (PubKeyHash)
    beneficiary_address = get_address(beneficiary)
    vkey_hash: VerificationKeyHash = beneficiary_address.payment_part

    # Create the vesting datum
    params = VestingParams(
        beneficiary=bytes(vkey_hash),
        deadline=int(time.time() + wait_time) * 1000,  # must be in milliseconds
    )

    if parameterized:
        # Build script
        save_path = assets_dir.joinpath(f"parameterized_vesting_{beneficiary}")
        script_path = lecture_dir.joinpath("parameterized_vesting.py")
        subprocess.run(
            [
                "opshin",
                "-o",
                str(save_path),
                "build",
                "spending",
                str(script_path),
                params.to_json(),
            ],
            check=True,
        )
        script_path = save_path.joinpath("testnet.addr")
    else:
        script_path = assets_dir.joinpath("vesting", "testnet.addr")

    # Load script info
    with open(script_path) as f:
        script_address = Address.from_primitive(f.read())

    # Make datum
    if parameterized:
        datum = PlutusData()
    else:
        datum = params

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
    context.submit_tx(signed_tx)

    show_tx(signed_tx)


if __name__ == "__main__":
    main()
