<div align="center">
<img  src="https://github.com/OpShin/opshin-pioneer-program/blob/main/opshin-pioneer-program.png" width="200" />
<h1 > Opshin Pioneer Program </h1>
<img src="https://img.shields.io/badge/cohort-4-red">
<img src="https://img.shields.io/badge/language-python3-3670A0?logo=python&logoColor=959da5">
<img src="https://github.com/OpShin/opshin-pioneer-program/actions/workflows/test.yaml/badge.svg"/>
</div>
<br/>

This repository implements many educational Cardano Smart Contracts in Python using [opshin](https://github.com/OpShin/opshin).
It also comes with off-chain code using [PyCardano](https://github.com/Python-Cardano/pycardano) and a host of test cases to ensure high quality of the resulting contracts.
Most of the code is in a similar format to the [plutus-pioneer-program](https://github.com/input-output-hk/plutus-pioneer-program).

## Installation

1. Install Python 3.8, 3.9 or 3.10 (if it not already installed on your operating system).
Python3.10 Installer [download](https://www.python.org/downloads/release/python-31010/).

2. Install python poetry.
Follow the official documentation [here](https://python-poetry.org/docs/#installation).

3. Install a python virtual environment with poetry:
```bash
# Optional. Use a specific python version
# replace <version> with 3.8, 3.9, or 3.10
# for this to work, python<version> must be accessible in your command line
poetry env use <version>

# install python dependencies
poetry install

# run a shell with the virtual environment activated
poetry shell
```

4. Install Docker.
Follow the official documentation [here](https://docs.docker.com/get-docker/).

### Cardano Node

Start a [Cardano Node](https://github.com/input-output-hk/cardano-node) and [Ogmios API](https://ogmios.dev/) with docker-compose:
```bash
# starts a cardano node and ogmios api on the preview testnet
docker-compose up
```

You can then access the `cardano-cli` using the docker image:
```bash
docker run --rm -it \
  --entrypoint cardano-cli \
  -e CARDANO_NODE_SOCKET_PATH=/ipc/node.socket \
  -v opshin-pioneer-program_node-db:/data \
  -v opshin-pioneer-program_node-ipc:/ipc \
  inputoutput/cardano-node
```
