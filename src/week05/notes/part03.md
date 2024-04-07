# A Simple Minting Policy

In this lecture, we delve into minting policies, specifically creating a simple minting policy in OpShin, analogous to validation scripts we've explored previously. Unlike validation scripts, minting policies do not involve a datum (because there is no script UTxO we're trying to spend) and focus solely on the redeemer and context. This session outlines the process from policy creation to execution using an example minting policy that universally allows minting and burning actions.

## Overview of Validation and Minting Policies

Validation scripts are triggered when a transaction attempts to consume a UTXO at a script address, receiving three inputs: datum, redeemer, and script context. In contrast, minting policies are invoked when the `mint` field in `TxInfo` is set to a non-zero value, signifying an intention to mint or burn tokens. To see this let's revisit the definition of [`TxInfo`](https://github.com/OpShin/opshin/blob/6aa79592ef59718feabd147ef3379b4b6b9c366f/opshin/ledger/api_v2.py#L463). If we're not simultaneously spending a script UTxO, the `purpose` field in `ScriptContext` would be set to `Minting` (instead of `Spending`) -- recall the different `ScriptPurpose`s [here](https://github.com/OpShin/opshin/blob/6aa79592ef59718feabd147ef3379b4b6b9c366f/opshin/ledger/api_v2.py#L448). If the purpose is `Minting`, the validator is exectuted receiving only two inputs: redeemer and context (and no datum).

## Constructing a Simple Minting Policy

We introduce a minimal minting policy in `lecture/free.py`, essentially allowing unrestricted minting and burning of tokens with its associated policy ID.
<!-- [NOTES TO PRESENTER]
Briefly show the code `lecture/free.py` pointing out that validator has only two arguments now, and all we check in this case is that the purpose is `Minting` (is this even needed?).
-->

## Compiling and Deploying the Policy

As before, we can easily compile the script using `opshin build lecture/free.py` and as a result obtain the respective policy ID and CBOR encoded script. Since in our case we have our python build script, we just run `python3 scripts/build.py`.

## Demonstration with `pycardano`

To test the policy, we again use off-chain code written in Python with `pycardano`, see `scripts/mint.py`. The script requires a wallet name, token name (of the tokens to be minted from our policy ID), and a minting script (in our case `free`). So we run for example:
```bash
python3 scripts/mint.py alice free_token --script free
```
Check the transcaction on CExplorer and see how the tokens were minted.

<!-- [NOTES TO PRESENTER]
Go through the code of `scripts/mint.py` and explain how it works.
-->
The off-chain minting code involves the following steps:
1. Finding a suitable UTxO in `alice`'s wallet to spend. (Actually, in the case of the `free` policy, we would not have to do this and could just use `builder.add_input_address(payment_address)` to let `pycardano` automatically find a suitable UTxO. However, having a specific UTxO will become necessary when we get to minting NFTs in the next lecture, so we anticipate a bit here and already write the code in a way that works for both cases.)
2. Load the script and add it to the transaction using `add_minting_script`.
3. Set the value to be minted as `MultiAsset`.
4. Sign and submit the transaction.

## Conclusion

This lecture has introduced custom minting policies. Via the simple example of an "always-suceeds" policy, we've gone through the full process of writing the script in OpShin, compiling it, and constructing a minting transaction using `pycardano`. This provides a good base for moving on to more complex minting policies in the next lectures.