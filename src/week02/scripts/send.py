import click
from pycardano import TransactionBuilder, TransactionOutput

from src.utils import get_address, get_signing_info, get_chain_context


@click.command()
@click.argument("name")
@click.argument("recipient")
@click.option("--amount", type=int, default=5000000)
def main(name, recipient, amount):
    context = get_chain_context()

    payment_address = get_address(name)

    recipient_address = get_address(recipient)

    builder = TransactionBuilder(context)
    builder.add_input_address(payment_address)
    builder.add_output(TransactionOutput(address=recipient_address, amount=amount))

    payment_vkey, payment_skey, payment_address = get_signing_info(name)
    signed_tx = builder.build_and_sign(
        signing_keys=[payment_skey],
        change_address=payment_address,
    )

    context.submit_tx(signed_tx)
    print(f"transaction id: {signed_tx.id}")
    print(f"Cardanoscan: https://preprod.cexplorer.io/tx/{signed_tx.id}")


if __name__ == "__main__":
    main()
