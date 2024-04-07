# A More Realistic Minting Policy

In this lecture, we'll extend the "trivial" minting policy from last session a bit by introducing some specific ownership controls into the script. In practice, this could for example simulates a "central bank" model within blockchain projects, where only the owner of a particular public key hash has the authorization to mint or burn tokens, a bit like in traditional financial systems where central banks control fiat currency issuance.

## The modified minting policy

<!-- [NOTES TO PRESENTER]
Briefly show the code `lecture/signed.py` pointing out the below differences.
-->
There are only two differences compared to the `free` policy from last session:
1. Using the `assert_signed` function, we check whether a specific public key hash has signed the transaction.
2. This specific public key hash is introduced as a parameter to the script. See additional first argument in the `validator` function, meaning we must remember to pass in the public key hash when compiling the script.

## Building the parameterized minting policy

<!-- [NOTES TO PRESENTER]
Point out how we re-build the script with e.g. `alice`'s public key hash as the parameter in `scripts/mint.py` using the `build` function imported from `opshin`.
-->

## Constructing and submitting a minting transaction

Apart from re-building the parameterized policy script, and adding the issuer to the `required_signers` when building the transaction, we use exactly the same off-chain code as in the previous session to mint tokens, i.e., we run:
```bash
python3 scripts/mint.py alice signed_token --script signed
```

## Conclusion:

In this session we've built upon the previous simple minting script to show a slightly more realistic example of a minting policy, basically implementing token control mechanisms akin to central banks' currency issuance in traditional finance.