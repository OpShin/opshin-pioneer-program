#!/bin/bash
cardano_cli="docker run --rm -it \
  --entrypoint cardano-cli \
  -e CARDANO_NODE_SOCKET_PATH=/ipc/node.socket \
  -v eopsin-pioneer-program_node-db:/data \
  -v eopsin-pioneer-program_node-ipc:/ipc \
  inputoutput/cardano-node"
$cardano_cli query utxo --address "$1" --testnet-magic 2
