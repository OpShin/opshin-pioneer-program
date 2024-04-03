# A Simple Minting Policy

In this lecture, we delve into minting policies, specifically creating a simple minting policy in Plutus, analogous to validation scripts we've explored previously. Unlike validation scripts, minting policies do not involve a datum and focus solely on the redeemer and context. This session outlines the process from policy creation to execution using an example minting policy that universally allows minting and burning actions.

## Overview of Validation and Minting Policies

Validation scripts are triggered when a transaction attempts to consume a UTXO at a script address, receiving three inputs: datum, redeemer, and context. In contrast, minting policies are invoked when the `txInfoMint` field in a transaction's context indicates a non-zero value, signifying an intention to mint or burn tokens. These policies are executed per currency symbol found within this field, receiving only two inputs: redeemer and context.

## Constructing a Simple Minting Policy

We introduce a minimal minting policy, essentially allowing unrestricted minting and burning for its associated currency symbol. The policy, defined through a Plutus script, requires conversion from a typed version to an untyped one, achieved through a utility function, `mkMintingPolicyScript`.

## Compiling and Deploying the Policy

Using Template Haskell, we compile the Plutus script to core, followed by serialization for storage and retrieval. This process also involves computing the currency symbol, representing the policy's unique identifier derived from the script's hash.

## Demonstration with `pycardano`

To test the policy, we use off-chain code written in Python with `pycardano` (TODO: describe, reference). The script prompts for an amount to mint or burn, constructs the transaction with the necessary policy script attached, and submits it to the Cardano blockchain. Through this demonstration, we successfully mint and then burn tokens, showcasing the minting policy in action.

## Conclusion

This lecture provides a foundational understanding of minting policies in Plutus, illustrating how they regulate the minting and burning of tokens on the Cardano blockchain. Through a straightforward example, we've seen how to create, compile, and enact a minting policy, along with off-chain code implementation using the Lucid framework. This framework enables practical interactions with the Cardano blockchain, from token creation to destruction, underscoring the flexibility and control afforded by Plutus scripts in decentralized applications.