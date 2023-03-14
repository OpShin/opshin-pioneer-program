import time

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
    VerificationKeyHash,
)

from src.utils import get_address, get_signing_info
from src.week03 import assets_dir
from src.week03.lecture.vesting import VestingParams


@click.command()
@click.argument("name")
@click.option(
    "--script",
    type=str,
    default="vesting",
    help="Which script address to attempt to spend",
)
def main(name: str, script):
    # Load chain context
    context = OgmiosChainContext("ws://localhost:1337", network=Network.TESTNET)

    # Load script info
    with open(assets_dir.joinpath(script, "script.cbor"), "r") as f:
        cbor_hex = f.read()

    cbor = bytes.fromhex(cbor_hex)

    plutus_script = PlutusV2Script(cbor)
    script_hash = plutus_script_hash(plutus_script)
    script_address = Address(script_hash, network=Network.TESTNET)

    # Get payment address
    payment_address = get_address(name)

    # Find a script UTxO
    utxo_to_spend = None
    params = None
    for utxo in context.utxos(str(script_address)):
        if utxo.output.datum:
            try:
                params = VestingParams.from_cbor(utxo.output.datum.cbor)
                if (
                    params.beneficiary == bytes(payment_address.payment_part)
                    and params.deadline < time.time() * 1000
                ):
                    utxo_to_spend = utxo
                    break
            except Exception:
                pass
    assert isinstance(utxo_to_spend, UTxO), "No script UTxOs found!"

    # Find a collateral UTxO
    non_nft_utxo = None
    for utxo in context.utxos(str(payment_address)):
        # multi_asset should be empty for collateral utxo
        if not utxo.output.amount.multi_asset and utxo.output.amount.coin > 5000000:
            non_nft_utxo = utxo
            break
    assert isinstance(non_nft_utxo, UTxO), "No collateral UTxOs found!"

    # Make redeemer
    redeemer = Redeemer(RedeemerTag.SPEND, 0)

    # Build the transaction
    builder = TransactionBuilder(context)
    builder.add_script_input(utxo_to_spend, script=plutus_script, redeemer=redeemer)
    builder.collaterals.append(non_nft_utxo)
    # This tells pycardano to add vkey_hash to the witness set when calculating the transaction cost
    vkey_hash: VerificationKeyHash = payment_address.payment_part
    builder.required_signers = [vkey_hash]
    # we must specify at least the start of the tx valid range in slots
    builder.validity_start = context.last_block_slot
    # This specifies the end of tx valid range in slots
    builder.ttl = builder.validity_start + 100

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
