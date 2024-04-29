# Homework

As always, we conclude the week with some homework assignments.

## Assignment 1: Extending the Signed Example

- **Objective**: Enhance the signed minting policy example by incorporating an additional condition based on time.

- **Details**:
  - The existing signed example features a minting policy that requires transactions to be signed by the owner of a specified public key hash (`PubKeyHash`).
  - **Task**: Introduce a second parameter of type `POSIXTime` to the minting policy. The new minting policy should ensure that minting or burning actions are permissible only if:
    1. The transaction is signed by the owner of the `PubKeyHash`.
    2. The action occurs before the specified `POSIXTime` deadline.
  - This creates a realistic minting policy that allows for a fixed minting period followed by a permanent prohibition of minting or burning actions.
  - **Optional**: Modify the corresponding `pycardano` off-chain code to mint from this new policy. This will involve passing the deadline parameter similarly to how we did things in the vesting example's off-chain code.

## Assignment 2: Modifying the NFT Policy

- **Objective**: Adjust the NFT minting policy to restrict the token name selection.

- **Details**:
  - The current NFT policy allows for the arbitrary selection of token names.
  - **Task**: Modify the NFT minting policy to enforce that the token name must always be the empty byte string. This restriction implies that the NFTs minted under this policy will have a predefined token name, removing the option for customization.
  - **Optional**: Again, in `pycardano` construct and submit a transaction to mint an NFT under this new policy.
