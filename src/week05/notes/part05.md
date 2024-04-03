# NFT's

The lecture focuses on the creation of Non-Fungible Tokens (NFTs) within the OpShin framework, detailing how unique tokens that exist only once on the blockchain can be minted. Here are the key points discussed:

## Non-Fungible Tokens (NFTs):

- **Definition**: NFTs are tokens that are unique and can only exist in a singular instance on the blockchain, unlike fungible tokens which can be minted in multiple quantities.
- **Uniqueness**: To ensure the uniqueness of an NFT, a strategy is needed that guarantees only a single minting transaction is possible for the token in question.

## Strategies for Minting NFTs:

1. **Inspecting `TxInfo`'s `mint` Field**: A naive approach might involve ensuring that only one token is minted per transaction. However, this does not prevent multiple transactions from minting more tokens.
   
2. **Using Deadlines**: Implementing a policy that allows minting only before a certain deadline ensures that no new tokens can be minted post-deadline. This, however, requires external verification to confirm that only one token was minted before the deadline, making it a less robust method for creating true NFTs.

3. **Utilizing UTXOs**: The key to creating a true NFT lies in leveraging the uniqueness of UTXOs (Unspent Transaction Outputs) on the blockchain. By requiring the minting transaction to consume a specific UTXO, and given that a UTXO can only be consumed once, it ensures the policy script allows only one minting transaction, making it a genuine NFT.

## Implementation of NFT Minting Policy:

- **Parameters**: The NFT minting policy script is parameterized by the token name and a specific UTXO (`txOutRef`). The policy mandates the minting of exactly one token and the consumption of the specified UTXO.
   
- **Validation**: The policy script checks that the minting transaction has indeed consumed the designated UTXO and that only one token with the specified name and amount is minted.
   
- **Lucid Framework**: (TODO: adjust to `pycardano`) The lecture demonstrates using the Lucid framework to interact with the parameterized minting policy script. By applying parameters like the token name and UTXO to the policy script via off-chain code, it enables the dynamic minting of NFTs.

### Key Takeaways:

- **True NFTs**: By requiring a minting transaction to consume a unique UTXO, it ensures that an NFT can only be minted once, thereby creating a "true NFT" whose uniqueness is guaranteed by the blockchain itself, without the need for external verification.
   
- **Flexibility and Security**: This approach offers a flexible yet secure method of minting NFTs, providing creators with the tools to issue unique digital assets on the Cardano blockchain through Plutus scripts.

This lecture highlights the innovative use of Plutus scripts to mint NFTs on the Cardano blockchain, showcasing the platform's capabilities for creating unique digital assets with verifiable ownership and authenticity.