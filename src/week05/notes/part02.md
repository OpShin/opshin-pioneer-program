# Values

In this lecture, we delve into the `Value` type in Plutus, defined in `Plutus.V1.Ledger.Value`. Despite focusing on Plutus version 2 throughout the course, it's important to note that the `Value` type has remained unchanged from version 1, hence we still reference `V1` in this context.

A key takeaway is that a token or coin on Cardano is identified by a combination of a currency symbol and a token name. The `Value` type itself is a wrapper around a map from currency symbols to another map from token names to integers. This nested mapping structure might initially seem complex but is crucial for representing the diverse range of tokens, including ADA, within the Cardano ecosystem.

## Understanding Currency Symbols and Token Names

- Both currency symbols and token names are new type wrappers around built-in byte strings. 
- An asset class, which defines a native token, is essentially a pair consisting of a currency symbol and a token name. ADA, for example, is represented by a specific asset class, with both the currency symbol and token name being wrappers around the empty byte string.

## Constructing and Analyzing Values

- Values can be constructed using the `assetClassValue` function, which takes an asset class and an integer, creating a `Value` that contains a specified number of coins of that type.
- Analyzing a value to determine the number of coins of a given asset class it contains is achieved through the `assetClassValueOf` function.

## Combining and Subtracting Values

- `Value` implements the `Monoid` interface, allowing values to be combined using the `<>` operator. This addition is reflective of the ability to create values containing multiple types of tokens.
- The `Group` interface extends this functionality by introducing subtraction of values through the `gSub` function, enabling the calculation of differences between values.

## Currency Symbol Significance

- The currency symbol's importance is tied to minting policies. A transaction that aims to mint or burn native tokens must include the script (minting policy) corresponding to each native token's currency symbol. This script, hashed to generate the currency symbol, dictates whether the transaction is authorized to mint or burn the tokens in question.
- ADA fits into this schema, with its currency symbol being the empty byte string, indicating that no script exists that would allow for ADA to be minted or burnt outside of its initial allocation and monetary expansion processes.

This exploration of the `Value` type and its components provides a foundational understanding of how tokens, including ADA and native tokens, are represented and manipulated within the Cardano ecosystem through Plutus scripts.