"""
Build the week 8 staking validator(s) to UPLC artefacts in `src/week08/assets/`.

By default, the lecture validator is built with a *placeholder* address (all
zero payment key hash, no staking credential). Pass `--address <bech32>` to
parameterise it with a real address — typically the wallet that should receive
half of the stake rewards.

Usage:
    poetry run python src/week08/scripts/build.py
    poetry run python src/week08/scripts/build.py --address <bech32>
"""

import click
from pathlib import Path
import sys
import subprocess
from opshin import build
from pycardano import Address

from src.utils import to_address
from src.week08 import assets_dir, lecture_dir



@click.command()
@click.option(
    "--address",
    "addr",
    help="Bech32 address to receive half of withdrawn rewards.",
)
def main(addr: str):
    assets_dir.mkdir(exist_ok=True)

    address = Address.from_primitive(addr)

    script_path = lecture_dir.joinpath("staking.py")
    print(script_path)
    out_dir = assets_dir.joinpath("staking")
    out_dir.mkdir(exist_ok=True)
    args = (to_address(address).to_json(),)
#    args = ()

    script = Path(script_path)
    command = [
        sys.executable,
        "-m",
        "opshin",
        "--cf",
        "build",
        "rewarding",
        str(script),
        *args,
        "--recursion-limit",
        "4000",
        "-O2",
    ]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
