import os

import blockfrost
from dotenv import load_dotenv
from pycardano import Network, OgmiosChainContext, ChainContext, BlockFrostChainContext
import pathlib

assert load_dotenv(
    dotenv_path=pathlib.Path(__file__).parent.parent.parent / ".env"
), "Failed to load .env file"

blockfrost_project_id = os.getenv("BLOCKFROST_PROJECT_ID", None)

ogmios_protocol = os.getenv("OGMIOS_API_PROTOCOL", "ws")
ogmios_host = os.getenv("OGMIOS_API_HOST", "localhost")
ogmios_port = os.getenv("OGMIOS_API_PORT", "1337")
ogmios_url = f"{ogmios_protocol}://{ogmios_host}:{ogmios_port}"

kupo_protocol = os.getenv("KUPO_API_PROTOCOL", "http")
kupo_host = os.getenv("KUPO_API_HOST", "localhost")
kupo_port = os.getenv("KUPO_API_PORT", "1442")
kupo_url = f"{kupo_protocol}://{kupo_host}:{kupo_port}"

network_name = os.getenv("NETWORK", "preprod")
if network_name == "mainnet":
    network = Network.MAINNET
else:
    network = Network.TESTNET


def get_chain_context() -> ChainContext:
    if blockfrost_project_id is not None:
        return BlockFrostChainContext(
            blockfrost_project_id,
            base_url=blockfrost.ApiUrls.preview.value
            if blockfrost_project_id.startswith("preview")
            else blockfrost.ApiUrls.mainnet.value,
        )
    chain_backend = os.getenv("CHAIN_BACKEND", "ogmios")
    if chain_backend == "ogmios":
        return OgmiosChainContext(ws_url=ogmios_url, network=network)
    elif chain_backend == "kupo":
        return OgmiosChainContext(ws_url=ogmios_url, network=network, kupo_url=kupo_url)
    else:
        raise ValueError(f"Chain backend not found: {chain_backend}")
