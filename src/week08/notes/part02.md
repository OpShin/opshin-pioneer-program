# Week 8 — Trying it on the Testnet

Unlike the original course, we use the **preview testnet** rather than a
local private testnet. The flow is otherwise the same.

## 0. Prerequisites

* Cardano node + Ogmios running locally (`docker compose up` from the
  repo root).
* `cardano-cli` available — the easiest way is to source
  [`scripts/alias_cardano_cli.sh`](../../../scripts/alias_cardano_cli.sh)
  (note: edit it to use `--network` instead of `--testnet-magic` if you
  prefer mainnet alignment).
* A wallet with some test ADA. Create one with
  [`scripts/create_key_pair.py`](../../../scripts/create_key_pair.py) and
  fund it from the [preview faucet](https://docs.cardano.org/cardano-testnet/tools/faucet/).

## 1. Build the staking validator

Pick the address that should receive half of all reward withdrawals
(typically a different wallet you control):

```bash
poetry run python src/week08/scripts/build.py --address <BECH32>
```

This writes `src/week08/assets/staking/script.cbor`.

## 2. Register the script stake credential and delegate

Pick a stake pool — `src/week08/scripts/query-stake-pools.sh` lists all
registered pools.

```bash
poetry run python src/week08/scripts/register-and-delegate.py <WALLET> <POOL_ID>
```

The script:

* derives the stake address from `script.cbor`,
* derives a payment address combining your wallet's payment key with the
  script as the staking credential,
* builds `StakeRegistration` + `StakeDelegation` certificates,
* submits a transaction carrying both certs, with the staking script and
  its (unit) redeemer attached.

After this, any ADA sent to the printed *script payment address*
contributes to the script's stake, and accumulates rewards.

The original `register-and-delegate.sh` (using `cardano-cli`) is kept
alongside as a reference.

## 3. Inspect rewards

```bash
src/week08/scripts/query-stake-info.sh
```

## 4. Withdraw rewards

Once the stake address has accumulated rewards (after a couple of
epochs):

```bash
src/week08/scripts/withdraw.sh <WALLET> <TXIN> <BECH32_PAYOUT_ADDR>
```

`<BECH32_PAYOUT_ADDR>` must match the `--address` argument from step 1,
otherwise the script will reject the withdrawal with
`insufficient reward sharing`.

## Notes on pycardano

Registration/delegation are driven by pycardano's
`TransactionBuilder.add_certificate_script` (see
`register-and-delegate.py`). The withdrawal step is still on
`cardano-cli` and porting it is left as an exercise.
