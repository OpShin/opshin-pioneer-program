# Week 8 — Plutus & Staking

This week mirrors *Week 8* of the Plutus Pioneer Program but rewrites the
staking validator in OpShin. The goal is to understand how **stake
credentials can be controlled by a Plutus script**, so that the on-chain
logic decides what to do with the rewards (or how the credential is
delegated / deregistered).

## Concepts

* On Cardano, an address has two parts: a **payment credential** and an
  optional **staking credential**. Funds are spent under the payment
  credential, but ADA in an address contributes to the *stake* of its
  staking credential.
* A staking credential can be a public-key hash *or* a script hash. When
  it is a script hash, any action involving the credential
  (registration, delegation, withdrawal) must be authorised by running
  that script.
* A *staking validator* is invoked under one of two purposes:
  * `Certifying(dcert)` — for `RegStakeCert`, `DeRegStakeCert`,
    `DelegateCert`, etc.
  * `Rewarding(staking_credential)` — when rewards are being withdrawn.

## The lecture validator

[`lecture/staking.py`](../lecture/staking.py) is parameterised by an
`Address`. It always approves certification actions and only approves
withdrawals if at least *half* of the withdrawn lovelace is paid (in
ADA) to that address in the same transaction.

The Haskell original is in
[`plutus-pioneer-program/code/Week08/lecture/Staking.hs`](../../../plutus-pioneer-program/code/Week08/lecture/Staking.hs).

## The homework

[`homework/homework.py`](../homework/homework.py) asks you to write a
similar validator parameterised by *two* values: a `PubKeyHash` that must
sign every transaction involving the script, and an `Address` that must
receive at least half of every withdrawal. See
[`plutus-pioneer-program/code/Week08/homework/Homework.hs`](../../../plutus-pioneer-program/code/Week08/homework/Homework.hs)
for the Haskell skeleton.

Hint: `context.tx_info.signatories` is a `List[PubKeyHash]`.
