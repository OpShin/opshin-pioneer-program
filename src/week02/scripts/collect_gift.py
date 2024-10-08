import click
from pycardano import (
    Address,
    TransactionBuilder,
    UTxO,
    PlutusV2Script,
    plutus_script_hash,
    Redeemer,
)

from src.utils import get_address, get_signing_info, network, get_chain_context
from src.utils.network import show_tx
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
    """
    Obtain deposited funds (using make_gift) from a smart contract
    """
    # Load chain context
    context = get_chain_context()

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
    for utxo in context.utxos(script_address):
        if utxo.output.datum:
            utxo_to_spend = utxo
            break
    assert isinstance(utxo_to_spend, UTxO), f"No script UTxOs found! Execute make gift with --script {script} to deposit funds at the address."

    # Build the transaction
    # no output is specified since everything minus fees is sent to change address
    if script in ["fourty_two", "fourty_two_typed"]:
        redeemer = Redeemer(42)
    elif script == "custom_types":
        from src.week02.lecture.custom_types import MySillyRedeemer

        redeemer = Redeemer(MySillyRedeemer(42))
    else:
        redeemer = Redeemer(0)
    builder = TransactionBuilder(context)
    builder.add_script_input(utxo_to_spend, script=plutus_script, redeemer=redeemer)

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
