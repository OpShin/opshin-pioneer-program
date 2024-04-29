# NFT's

The lecture focuses on the creation of Non-Fungible Tokens (NFTs) using a special minting policy written in OpShin. As the term "non-fungible" suggests, this means we need to describe how to mint tokens with a unique name, i.e., for which we can ensure that they will only ever be minted once.

## Non-Fungible Tokens (NFTs):

- **Definition**: NFTs are tokens that are unique and can only exist in a singular instance on the blockchain, unlike fungible tokens which can be minted in larger quantities.
- **Uniqueness**: To ensure the uniqueness of an NFT, a strategy is needed that guarantees only a single minting transaction (with minted amount 1) is possible for the token in question.

## Strategies for Minting NFTs:

When thinking about how to ensure the uniqueness of NFTs, several strategies may come to mind:

1. **Inspecting `TxInfo`'s `mint` Field**: A naive approach might involve ensuring that only one token is minted per transaction. However, this does not prevent multiple transactions from minting more tokens.
   
2. **Using Deadlines**: Implementing a policy that allows minting only before a certain deadline ensures that no new tokens can be minted post-deadline. This, however, requires external verification to confirm that only one token was minted before the deadline, making it a less robust method for creating true NFTs.

3. **Utilizing UTXOs**: The key to creating a true NFT lies in leveraging the uniqueness of UTxOs on the blockchain. By requiring the minting transaction to consume a specific UTXO, and given that a UTXO can only be consumed once, it ensures the policy script allows only one minting transaction, making it a genuine NFT.

## Implementation of NFT Minting Policy

Let's see how this last strategy can be implemented in OpShin.
<!-- [NOTES TO PRESENTER]
Go through `lecture/nft.py` and explain the script.
-->
The minting validator involves:
1. Checking that a `Minting` purpose is used and extracting the respective policy ID from it.
2. Checking that exactly one token with the specified (as parameter) token name is minted and no tokens with other names are minted.
3. Checking that the transaction consumes the specified (as parameter) UTxO.

Note that in this case we pass both the desired token name as well as the consumed UTxO reference as parameters to the script. An alternative option would be to provide the consumed UTxO via the redeemer. However, then it is important to have another way of ensuring unique token names, as in this case, the same policy script can be used for minting repeatedly with different UTxOs in the redeemer. A common option here is for example to enforce the token name to be a hash of the consudmed UTxO (i.e. it's transaction ID and output index). We leave making these modifactions as an exercise to the interested viewer.

## Off-chain Code for Minting an NFT

We again use the off-chain minting code in `scripts/mint.py`. This time, observe how the script is compiled with a reference to the `utxo_to_spend` (which is why we had to find a suitable UTxO in the first place) and the token name as parameters. Now let's mint our first NFT with the following command
```bash
python3 scripts/mint.py alice my_first_opshin_nft --script nft
```
and click on the generated link to check it out on CExplorer.

## Key Takeaways and Conclusion:

- **True NFTs**: By requiring a minting transaction to consume a unique UTXO, we can ensure that an NFT can only be minted once, thereby creating a "true" NFT whose uniqueness is guaranteed by the design of the minting policy, without the need for e.g. external verification of deadlines.

Apart from learning about NFTs, we've now seen yet another example of an OpShin minting policy. We you're now equipped with the necessary knowledge and tools to apply these concepts for creating your own minting scripts (and of course for solving the upcoming homework assignments!).