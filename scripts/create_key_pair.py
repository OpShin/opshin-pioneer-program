from pathlib import Path

import click
from pycardano import Address, Network, PaymentSigningKey, PaymentVerificationKey

keys_dir = Path(__file__).parent.parent.joinpath("keys")


@click.command()
@click.argument("name")
def main(name):
    """
    Creates a testnet signing key, verification key, and address.
    """
    keys_dir.mkdir(exist_ok=True)
    skey_path = keys_dir.joinpath(f"{name}.skey")
    vkey_path = keys_dir.joinpath(f"{name}.vkey")
    addr_path = keys_dir.joinpath(f"{name}.addr")

    if skey_path.exists():
        raise FileExistsError(f"signing key file ${skey_path} already exists")
    if vkey_path.exists():
        raise FileExistsError(f"verification key file ${vkey_path} already exists")
    if addr_path.exists():
        raise FileExistsError(f"address file ${addr_path} already exists")

    signing_key = PaymentSigningKey.generate()
    signing_key.save(str(skey_path))

    verification_key = PaymentVerificationKey.from_signing_key(signing_key)
    verification_key.save(str(vkey_path))

    network = Network.TESTNET
    address = Address(payment_part=verification_key.hash(), network=network)
    with open(addr_path, mode="w") as f:
        f.write(str(address))

    print(f"wrote signing key to: {skey_path}")
    print(f"wrote verification key to: {vkey_path}")
    print(f"wrote address to: {addr_path}")


if __name__ == "__main__":
    main()
