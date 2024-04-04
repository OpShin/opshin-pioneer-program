<!-- [NOTES TO PRESENTER]
Show `imgs/utxo_diagram.png` while going through first 3 sections.
-->

# Low-Level, Untyped Validation Scripts

This lecture focuses on the on-chain part of smart contracts, specifically the validation scripts in Cardano's extended UTXO (EUTxO) model. First, we briefly discuss the difference between on-chain and off-chain components of smart contracts. Then, we recap the EUTxO model and its key elements: datum, redeemer, and context. As these concepts are independent of the smart contract language, for more in-depth explanations, we refer to the respective [section of the Plutus Pioneer Program](https://www.youtube.com/watch?v=3tcWCZV6L_w). Moreover, this lecture explores the data representation in OpShin. Finally, we present a simple validation script and, following this `gift.py` script as an example, we walk you through the compilation process for such on-chain scripts.

## On-Chain vs. Off-Chain

Smart contracts on Cardano consist of two main components:
- **On-Chain**: Involves validation scripts that determine the legitimacy of transactions.
- **Off-Chain**: Runs on the user's side, crafting and submitting transactions.
Both elements are crucial for the development and execution of smart contracts.

## Extended UTXO Model

Recall that compared to the standard UTxO model (e.g. used in Bitcoin), the Cardano's extended UTxO model introduces script addresses alongside traditional public key addresses. These script addresses allow for the execution of arbitrary logic to validate transactions. Moreover, the traditional UTxO concept is extended with:
- **Datum**: A piece of data attached to a UTxO, acting as a state.
- **Redeemer**: Arbitrary data provided by the consuming transaction.
- **Script Context**: The transaction being validated, including all its inputs and outputs.

<!-- [NOTES TO PRESENTER]
Next, open `lecture/gift.py`. The following sections are meant to walk through the script and show how to compile it.
-->

## Hands-on Part

### Data Representation

In OpShin (like in Plutus), the datum, redeemer and script context are represented by a unified data type called `BuiltinData` at a low level, ensuring uniformity across different components of the smart contract. However, as we will see in later lectures, higher levels of abstraction permit custom data types for the datum and redeemer.

### Simple Validation Script

The `gift.py` validation script we see here is very basic. As you can see, it completely ignores the datum, redeemer, and context, and always returns `None` without throwing any errors. This means that any transaction can consume the UTxO guarded by this script.

### Serialization and Compilation

The process of converting this human-readable OpShin function into code that can be validated on-chain involves compilation and serialization. This procedure is essentially the first step of deploying a smart contracts on the Cardano. How to then interact with these contracts will be covered in the following lectures.

We now go through compilation process of `gift.py`. For this, simply open a terminal and do
```bash
cd src/week02/lecture
opshin build gift.py
```
As a result, in the `build/gift` directory, we will obtain the compiled and serialized version of the script in CBOR encoding in `script.cbor`. Moreover, the `mainnet.addr` and `testnet.addr` files contain the addresses of the script on the respective networks.

## Conclusion

Understanding low-level, untyped validation scripts, and how to compile the respective OpShin code is of course fundamental for smart contract development. We hope this lecture has provided the basics, preparing you for seeing some more interesting contracts in the upcoming sessions.
