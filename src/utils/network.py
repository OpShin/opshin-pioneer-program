import os

from pycardano import Network, OgmiosChainContext, ChainContext, BlockFrostChainContext

ogmios_host = os.getenv("OGMIOS_API_HOST", "localhost")
ogmios_port = os.getenv("OGMIOS_API_PORT", "1337")
ogmios_url = f"ws://{ogmios_host}:{ogmios_port}"

kupo_host = os.getenv("KUPO_API_HOST", "localhost")
kupo_port = os.getenv("KUPO_API_PORT", "1442")
kupo_url = f"http://{kupo_host}:{kupo_port}"

blockfrost_project_id = os.getenv("BLOCKFROST_PROJECT_ID", None)

network_name = os.getenv("NETWORK", "preview")
if network_name == "mainnet":
    network = Network.MAINNET
else:
    network = Network.TESTNET


def get_chain_context() -> ChainContext:
    chain_backend = os.getenv("CHAIN_BACKEND", "ogmios")
    if chain_backend == "ogmios":
        return OgmiosChainContext(ws_url=ogmios_url, network=network)
    elif chain_backend == "kupo":
        return OgmiosChainContext(ws_url=ogmios_url, network=network, kupo_url=kupo_url)
    elif chain_backend == "blockfrost":
        return BlockFrostChainContext(blockfrost_project_id, network=network)
    else:
        raise ValueError(f"Chain backend not found: {chain_backend}")
