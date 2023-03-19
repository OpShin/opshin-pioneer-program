import os

from pycardano import Network

ogmios_host = os.getenv("OGMIOS_API_HOST", "localhost")
ogmios_port = os.getenv("OGMIOS_API_PORT", "1337")
ogmios_url = f"ws://{ogmios_host}:{ogmios_port}"

network = Network.TESTNET
