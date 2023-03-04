#!/bin/bash
path=$(readlink -f "$0")
network=$1
if [ "$network" == "" ]; then
  echo >&2 "expected network as argument"
  exit 1
fi
network_dir=$(dirname "$path")/network/$network
echo "Downloading configuration files to $network_dir"
mkdir -p "$network_dir"
wget "https://book.world.dev.cardano.org/environments/${network}/config.json" -O "$network_dir/config.json"
wget "https://book.world.dev.cardano.org/environments/${network}/topology.json" -O "$network_dir/topology.json"
wget "https://book.world.dev.cardano.org/environments/${network}/byron-genesis.json" -O "$network_dir/byron-genesis.json"
wget "https://book.world.dev.cardano.org/environments/${network}/shelley-genesis.json" -O "$network_dir/shelley-genesis.json"
wget "https://book.world.dev.cardano.org/environments/${network}/alonzo-genesis.json" -O "$network_dir/alonzo-genesis.json"
