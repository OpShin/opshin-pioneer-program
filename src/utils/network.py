import os
import sys

import blockfrost
from dotenv import load_dotenv
from opshin.ledger.api_v2 import TxOut
from pycardano import Network, OgmiosChainContext, ChainContext, BlockFrostChainContext, KupoOgmiosV6ChainContext, \
    Transaction
import pathlib

if not load_dotenv(dotenv_path=pathlib.Path(__file__).parent.parent.parent / ".env"):
    print(
        "Failed to load .env file. If you are getting errors, please copy .env.example to .env and fill in the values.",
        file=sys.stderr,
    )

blockfrost_project_id = os.getenv("BLOCKFROST_PROJECT_ID", None)

ogmios_protocol = os.getenv("OGMIOS_API_PROTOCOL", "ws")
ogmios_host = os.getenv("OGMIOS_API_HOST", "localhost")
ogmios_port = int(os.getenv("OGMIOS_API_PORT", "1337"))
ogmios_url = f"{ogmios_protocol}://{ogmios_host}:{ogmios_port}"

kupo_protocol = os.getenv("KUPO_API_PROTOCOL", "http")
kupo_host = os.getenv("KUPO_API_HOST", "localhost")
kupo_port = os.getenv("KUPO_API_PORT", "1442")
kupo_url = f"{kupo_protocol}://{kupo_host}:{kupo_port}"

network_name = os.getenv("NETWORK", "preview")
if network_name == "mainnet":
    network = Network.MAINNET
else:
    network = Network.TESTNET
chain_explorer = os.getenv("CHAIN_EXPLORER", "cexplorer.io")


def get_chain_context() -> ChainContext:
    if blockfrost_project_id is not None:
        return BlockFrostChainContext(
            blockfrost_project_id,
            base_url=blockfrost.ApiUrls.preview.value
            if blockfrost_project_id.startswith("preview")
            else (
                blockfrost.ApiUrls.preprod.value
                if blockfrost_project_id.startswith("preprod")
                else blockfrost.ApiUrls.mainnet.value
            ),
        )
    chain_backend = os.getenv("CHAIN_BACKEND", "ogmios")
    if chain_backend == "ogmios":
        return OgmiosChainContext(host=ogmios_host, port=ogmios_port, secure=ogmios_protocol=="wss", network=network)
    elif chain_backend == "kupo":
        return KupoOgmiosV6ChainContext(host=ogmios_host, port=ogmios_port, secure=ogmios_protocol=="wss", network=network, kupo_url=kupo_url)
    else:
        raise ValueError(f"Chain backend not found: {chain_backend}")

def show_tx(tx: Transaction):
    print(f"transaction id: {tx.id}")
    if network_name == "mainnet":
        print(f"Cardanoscan: https://{chain_explorer}/tx/{tx.id}")
    else:
        print(f"Cardanoscan: https://{network_name}.{chain_explorer}/tx/{tx.id}")
