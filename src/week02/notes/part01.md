# Low-Level, Untyped Validation Scripts

This lecture focuses on the on-chain part of smart contracts, specifically the validation scripts in Cardano's extended UTXO (EUTxO) model. First, we briefly discuss the difference between on-chain and off-chain components of smart contracts. Then, we introduce the EUTxO model and its key elements: datum, redeemer, and context. As these concepts are independent of the smart contract language, for more in-depth explanations, we refer to the respective [section of the Plutus Pioneer Program](https://www.youtube.com/watch?v=3tcWCZV6L_w). Moreover, this lecture explores the data representation in OpShin. Finally, we present a simple validation script and, following this `gift.py` script as an example, walk you through the compilation process for on-chain scripts.

## On-Chain vs. Off-Chain

Smart contracts on Cardano consist of two main components:
- **On-Chain**: Involves validation scripts that determine the legitimacy of transactions.
- **Off-Chain**: Exists within the user's wallet, crafting and submitting transactions.

Both elements are crucial for the development and execution of smart contracts.

## Extended UTXO Model

The EUTxO model introduces script addresses alongside traditional public key addresses. These script addresses allow for the execution of arbitrary logic to validate transactions. The model extends traditional UTXO concepts with:
- **Datum**: A piece of data attached to a UTXO, acting as a state.
- **Redeemer**: Arbitrary data provided by the consuming transaction.
- **Context**: The transaction being validated, including all its inputs and outputs.

## Data Representation

In OpShin (and similarly in Plutus), these elements are represented by a unified data type (called `BuiltinData`) at a low level, ensuring uniformity across different components of the smart contract. However, as we will see in later lectures, higher levels of abstraction permit custom data types for the datum and redeemer, trading off between convenience and performance.

## Practical Examples

### Simple Validation Script

A basic validation script (`gift.py`) is introduced, demonstrating a script that always validates successfully. This script is agnostic to the datum, redeemer, and context, essentially allowing any transaction to consume the UTxO it guards.

### Serialization and Compilation

The process of converting Haskell (or in the case of OpShin, Python) functions into on-chain scripts involves compilation and serialization. This procedure is essential for deploying and interacting with smart contracts on the Cardano blockchain.

### TODO

Walk through compilation process of `gift.py`.

## Conclusion

Understanding low-level, untyped validation scripts is fundamental for Cardano smart contract development. This lecture provides the groundwork for these concepts, preparing participants for more complex topics in the upcoming sessions.
