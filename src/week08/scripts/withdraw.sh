#!/usr/bin/env bash
#
# Withdraw all rewards accumulated at the script-controlled stake address,
# paying at least half of the withdrawn amount back to the address the
# staking validator was parameterised with (`--address` of build.py).
#
# Mirrors `withdraw-user1-script.sh` from Plutus Pioneer Program Week 8.
#
# Usage:
#     src/week08/scripts/withdraw.sh <WALLET_NAME> <TXIN> <BECH32_PAYOUT_ADDR>
#
# `TXIN` pays fees and acts as collateral. `BECH32_PAYOUT_ADDR` is the
# address that will receive half (rounded up) of the withdrawn rewards —
# it must match the address `build.py` was parameterised with, otherwise
# the validator will reject the withdrawal.

set -euo pipefail

if [ $# -ne 3 ]; then
    echo "usage: $0 <WALLET_NAME> <TXIN> <BECH32_PAYOUT_ADDR>" >&2
    exit 1
fi

wallet=$1
txin=$2
payout_addr=$3

testnet_magic=${TESTNET_MAGIC:-2}
root=$(git rev-parse --show-toplevel)
week=$root/src/week08
tmp=$week/tmp
mkdir -p "$tmp"

script_plutus=$week/assets/staking/script.plutus
stake_addr=$tmp/script-stake.addr
payment_addr=$tmp/script-payment.addr
pp=$tmp/protocol-params.json
body=$tmp/tx.txbody
signed=$tmp/tx.tx

[ -f "$script_plutus" ] || {
    echo "Missing $script_plutus. Run register-and-delegate.sh first." >&2
    exit 1
}
[ -f "$stake_addr" ] || {
    echo "Missing $stake_addr. Run register-and-delegate.sh first." >&2
    exit 1
}

# Query reward balance.
amt1=$(cardano-cli query stake-address-info \
    --testnet-magic "$testnet_magic" \
    --address "$(cat "$stake_addr")" | jq '.[0].rewardAccountBalance')
amt2=$(( amt1 / 2 + 1 ))
echo "rewards available : $amt1"
echo "paying to address : $amt2"

cardano-cli query protocol-parameters \
    --testnet-magic "$testnet_magic" \
    --out-file "$pp"

cardano-cli transaction build \
    --babbage-era \
    --testnet-magic "$testnet_magic" \
    --change-address "$(cat "$payment_addr")" \
    --out-file "$body" \
    --tx-in "$txin" \
    --tx-in-collateral "$txin" \
    --tx-out "$payout_addr+$amt2 lovelace" \
    --withdrawal "$(cat "$stake_addr")+$amt1" \
    --withdrawal-script-file "$script_plutus" \
    --withdrawal-redeemer-file "$week/assets/unit.json" \
    --protocol-params-file "$pp"

cardano-cli transaction sign \
    --testnet-magic "$testnet_magic" \
    --tx-body-file "$body" \
    --out-file "$signed" \
    --signing-key-file "$root/keys/$wallet.skey"

cardano-cli transaction submit \
    --testnet-magic "$testnet_magic" \
    --tx-file "$signed"
