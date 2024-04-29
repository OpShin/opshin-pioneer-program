from pathlib import Path

import click
from pycardano import (
    Address,
    PlutusV2Script,
    plutus_script_hash,
    ChainContext,
    TransactionBuilder,
    TransactionOutput,
    Value,
    min_lovelace,
)
from src.utils import (
    get_address,
    get_signing_info,
    network,
    get_chain_context,
    get_ref_utxo,
)
from src.week03 import assets_dir
from src.week03.tests.test_lecture import script_paths


@click.command()
@click.argument("owner")
def main(owner):
    payment_vkey, payment_skey, payment_address = get_signing_info(owner)

    # Load chain context
    context = get_chain_context()

    assets_dir.mkdir(exist_ok=True)
    for script in script_paths:
        print("SCRIPT", script)
        build_dir = assets_dir.joinpath(Path(script).stem)

        with open(build_dir.joinpath("script.cbor")) as f:
            contract_cbor_hex = f.read().strip()
        contract_cbor = bytes.fromhex(contract_cbor_hex)

        contract_plutus_script = PlutusV2Script(contract_cbor)
        contract_script_hash = plutus_script_hash(contract_plutus_script)
        contract_script_address = Address(contract_script_hash, network=network)

        ref_utxo = get_ref_utxo(contract_plutus_script, context)
        if ref_utxo:
            print(f"reference script UTXO for {script} already exists")
            continue

        txbuilder = TransactionBuilder(context)
        output = TransactionOutput(
            contract_script_address, amount=1_000_000, script=contract_plutus_script
        )
        output.amount = Value(min_lovelace(context, output))
        txbuilder.add_output(output)
        txbuilder.add_input_address(payment_address)
        while True:
            try:
                signed_tx = txbuilder.build_and_sign(
                    signing_keys=[payment_skey], change_address=payment_address
                )
                context.submit_tx(signed_tx)
                print(
                    f"creating {script} reference script UTXO; transaction id: {signed_tx.id}"
                )
                print(f"transaction id: {signed_tx.id}")
                print(f"Cardanoscan: https://preview.cexplorer.io/tx/{signed_tx.id}")
                break
            except Exception as e:
                print(f"error: {e}")
                pass


if __name__ == "__main__":
    main()
