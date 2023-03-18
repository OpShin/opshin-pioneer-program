#!/bin/bash
echo "alias cardano-cli='docker run --rm -it --entrypoint cardano-cli -e CARDANO_NODE_SOCKET_PATH=/ipc/node.socket -v opshin-pioneer-program_node-db:/data -v opshin-pioneer-program_node-ipc:/ipc inputoutput/cardano-node'" >>~/.bashrc
