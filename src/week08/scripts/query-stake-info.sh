#!/usr/bin/env bash
# Query reward / delegation info for the script-controlled stake address.

set -euo pipefail

testnet_magic=${TESTNET_MAGIC:-2}
root=$(git rev-parse --show-toplevel)
stake_addr=$root/src/week08/tmp/script-stake.addr

[ -f "$stake_addr" ] || {
    echo "Missing $stake_addr. Run register-and-delegate.sh first." >&2
    exit 1
}

cardano-cli query stake-address-info \
    --testnet-magic "$testnet_magic" \
    --address "$(cat "$stake_addr")"
