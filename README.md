<div align="center">
  <a href="https://github.com/OpShin/opshin-pioneer-program">
    <img src="https://github.com/OpShin/opshin-pioneer-program/blob/main/opshin-pioneer-program.png" width="200" />
  </a>
  <h1> Opshin Pioneer Program </h1>
  <a href="https://github.com/input-output-hk/plutus-pioneer-program">
    <img src="https://img.shields.io/badge/cohort-4-red">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/language-python3-3670A0?logo=python&logoColor=959da5">
  </a>
  <a href="https://github.com/OpShin/opshin-pioneer-program/actions/workflows/test.yaml">
    <img src="https://github.com/OpShin/opshin-pioneer-program/actions/workflows/test.yaml/badge.svg"/>
  </a>
  <a href="https://discord.com/invite/umR3A2g4uw">
    <img src="https://dcbadge.vercel.app/api/server/umR3A2g4uw?style=flat&theme=default-inverted&compact=true"/>
  </a>
</div>


This repository implements many educational Cardano Smart Contracts in Python using [opshin](https://github.com/OpShin/opshin).
It also comes with off-chain code using [PyCardano](https://github.com/Python-Cardano/pycardano) and a host of test cases to ensure high quality of the resulting contracts.
Most of the code is in a similar format to the [plutus-pioneer-program](https://github.com/input-output-hk/plutus-pioneer-program).
Join the opshin [discord server](https://discord.com/invite/umR3A2g4uw) for Q/A and interact with other opshin pioneers!

## Installation

1. Install Python 3.8, 3.9, 3.10 or 3.11 (if it not already installed on your operating system).
Python3.11 Installer [download](https://www.python.org/downloads/release/python-3112/).

2. Install python poetry.
Follow the official documentation [here](https://python-poetry.org/docs/#installation).

3. Install a python virtual environment with poetry:
```bash
# Optional. Use a specific python version
# replace <version> with 3.8, 3.9, 3.10, or 3.11
# for this to work, python<version> must be accessible in your command line
# alternatively provide the path to your python executable
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

## How to Follow the Pioneer Lectures and Code
Here's a rough mapping of the lecture videos and what parts of this repository you can work on for each week.
Some files may not be documented thoroughly so try to infer the purpose by referring the structure of the lectures.

### [Lecture 1](https://www.youtube.com/playlist?list=PLNEK_Ejlx3x3xFHJJKdyfo9eB0Iw-OQDd)

- [Welcome and Introduction](https://youtu.be/g4fBo4QPir0)
- [Setting up Our Development Environment](https://youtu.be/-cmIqKCzzOU)
- [Kuber Marketplace Demo](https://youtu.be/ZaB-7ZYBi3g)
- [Hashing & Digital Signatures](https://youtu.be/f-WKPWbk9Jg)
- [The EUTxO-Model](https://youtu.be/ulYDNaEKf4g)
- [Homework](https://youtu.be/Ey903I-R1KY)
  - Follow the above installation instructions and get this repository set up locally.
  - Test your node synchronization with `scripts/query_tip.sh`

### [Lecture 2](https://www.youtube.com/playlist?list=PLNEK_Ejlx3x1-oF7NDy0MhXxG7k5O6ZOA)

- [Low-Level, Untyped Validation Scripts](https://youtu.be/3tcWCZV6L_w)
  - Study and compare the gift contract in opshin to plutus.
  - `src/week02/lecture/gift.py`
- [Using the Cardano CLI to Interact with Plutus](https://youtu.be/2MbzKzoBiak)
  - We use PyCardano to create off-chain scripts for our opshin contracts.
    Run the following python scripts with `poetry run python <script-path>`.
    The bash scripts using the dockerized Cardano CLI are also provided for reference.
  - Look here for offchain code: `src/week02/scripts/`
  - Look here for helper scripts (such as creating a test wallet): `scripts/`
- [High-Level, Typed Validation Scripts](https://youtu.be/GT8OjOzsOb4)
  - Review the rest of the opshin scripts.
  - `src/week02/lecture/fourty_two.py`
  - `src/week02/lecture/fourty_two_typed.py`
  - `src/week02/lecture/custom_types.py`
  - `src/week02/lecture/burn.py`
- [Summary](https://youtu.be/F5ewN65Mn4I)
- [Homework](https://youtu.be/OR2IfD4oDjw)
  - Complete the following homework files:
  - `src/week02/homework/homework1.py`
  - `src/week02/homework/homework2.py`
  - You can test your solution with:
  - `pytest src/week02/tests/test_homework.py`
  - The solutions are availble at:
  - `src/week02/homework/homework1_solved.py`
  - `src/week02/homework/homework2_solved.py`

### [Lecture 3](https://www.youtube.com/playlist?list=PLNEK_Ejlx3x2zXSjHRKLSc5Jn9vJFA3_O)

- [Script Contexts](https://youtu.be/dcoYrIyEI4o)
- [Handling Time](https://youtu.be/LPzwMqOnWvk)
- [A Vesting Example](https://youtu.be/5D0O7q9UPJA)
  - `src/week03/lecture/vesting.py`
- [Parameterized Contracts](https://youtu.be/ZSKVu32c5eA)
  - `src/week03/lecture/parameterized_vesting.py`
- [Offchain Code with Lucid](https://youtu.be/C8TuGSzhqXU)
  - We implement the same in pycardano instead in `src/week03/scripts`.
- [Reference Scripts](https://youtu.be/Rnyc5YXVXew)
  - To be implemented...
- [Homework](https://youtu.be/hdt4XqFeEyg)
  - Complete the following homework files:
  - `src/week03/homework/homework1.py`
  - `src/week03/homework/homework2.py`
  - Like before, you can run tests from `src/week03/tests`
- [Summary](https://youtu.be/gxan_u2pStE)

### [Lecture 4](https://www.youtube.com/playlist?list=PLNEK_Ejlx3x2j587Ox_nwEzmCO-elk8BG)
This lecture is about alternative offchain solutions.
We use pycardano, but you can compare and contrast alternatives.

- [On-chain VS Off-chain](https://youtu.be/pTc_BJby5GU)
- [Off-chain Code with Cardano CLI and GUI](https://youtu.be/gsgQ-xmzbpA)
- [Off-chain Code with Kuber](https://youtu.be/fzib9ALlL2M)
- [Off-chain Code with Lucid](https://youtu.be/BXz5V2rjbiE)
- [Homework](https://youtu.be/2Qm2xgmtbk4)
  - Implement the offchain code for the files in `src/week04/homework`.
  - Although the contracts are implemented in opshin, you can use offchain code other than pycardano to complete this.
  - There is no correct solution for this week as solutions can very widely.
    So make sure to test your code!
  - We will continue to implement off-chain code in pycardano for this repository.

### [Lecture 5](https://www.youtube.com/playlist?list=PLNEK_Ejlx3x2T1lIR4XnDILKukj3rPapi)

- [Introduction](https://youtu.be/HgXYsMFqnb4)
- [Values](https://youtu.be/ThYByMLC0EI)
- [A Simple Minting Policy](https://youtu.be/g_VoKPK-tk0)
- [A More Realistic Minting Policy](https://youtu.be/Faru8_Br2Xg)
- [NFT's](https://youtu.be/9kW-z_RuwEY)
- [Homework](https://youtu.be/nQC_GNPIRT8)
