# Homework

As always, we conclude the week with some homework assignments.

## Assignment 1: Extending the Signed Example

- **Objective**: Enhance the signed minting policy example by incorporating an additional condition based on time.

- **Details**:
  - The existing signed example features a minting policy that requires transactions to be signed by the owner of a specified public key hash (`PubKeyHash`).
  - **Task**: Introduce a second parameter of type `POSIXTime` to the minting policy. The new condition should mandate that minting or burning actions are permissible only if:
    1. The transaction is signed by the owner of the `PubKeyHash`.
    2. The action occurs before the specified `POSIXTime` deadline.
  - This creates a realistic minting policy, allowing for a fixed minting period followed by a permanent cessation of minting or burning actions.
  - **Optional**: Modify the corresponding off-chain code, presumably using the Lucid framework, to accommodate this new minting policy. This will involve handling the deadline condition similarly to how time constraints were managed in the vesting example's off-chain code.

## Assignment 2: Modifying the NFT Policy

- **Objective**: Adjust the NFT minting policy to restrict the token name selection.

- **Details**:
  - The current NFT policy allows for the arbitrary selection of token names.
  - **Task**: Amend the NFT minting policy to enforce that the token name must always be the empty byte string. This restriction implies that the NFTs minted under this policy will have a predefined token name, removing the option for customization.
  - Note that the lecture's approach uses the `TxOutRef` as a parameter in both the typed and untyped versions of the policy script, a common practice for parameter handling in Plutus scripts.
  - **Optional for Lucid Users**: For those using the Lucid framework for off-chain code, this modification might pose a challenge due to the initial setup, where parameters are managed differently. The task hints at possibly adopting an approach similar to the signed example, suggesting a method to align with Lucid's handling of parameters and off-chain code execution.

These assignments encourage exploration into time-based conditions within minting policies and restrictions on token naming conventions, providing practical experience with OpShin's Cardano smart contracts capabilities.