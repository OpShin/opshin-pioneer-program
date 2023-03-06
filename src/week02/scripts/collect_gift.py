import json

import click
from pycardano import (
    OgmiosChainContext,
    Network,
    Address,
    TransactionBuilder,
    UTxO,
    PlutusV2Script,
    plutus_script_hash,
    Redeemer,
    RedeemerTag,
)

from src.utils import get_address, get_signing_info
from src.week02 import assets_dir


@click.command()
@click.argument("name")
def main(name):
    # Load chain context
    context = OgmiosChainContext("ws://localhost:1337", network=Network.TESTNET)

    # Load script info
    with open(assets_dir.joinpath("gift", "script.plutus"), "r") as f:
        script_plutus = json.load(f)
        script_hex = script_plutus["cborHex"]
    with open(assets_dir.joinpath("gift", "script.cbor"), "r") as f:
        assert script_hex == f.read()
    gift_script = PlutusV2Script(bytes.fromhex(script_hex))
    script_hash = plutus_script_hash(gift_script)
    script_address = Address(script_hash, network=Network.TESTNET)
    with open(assets_dir.joinpath("gift", "testnet.addr")) as f:
        assert script_address == Address.from_primitive(f.read())

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
    builder = TransactionBuilder(context)
    builder.add_script_input(
        utxo_to_spend, script=gift_script, redeemer=Redeemer(RedeemerTag.SPEND, 0)
    )
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
