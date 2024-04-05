<!-- [NOTES TO PRESENTER]
Another code walk-through lecture, this time for `src/week03/lecture/parameterized_vesting.py`. Should be a short one since the issues with Template Haskell that come up when parameterizing contracts in Plutus are not really a thing in OpShin. Still, good to show how to pass parameters as arguments when compiling the contract. Here are some things to mention while going through the code.
-->

# Parameterized Contracts

This lecture introduces the concept of parameterized contracts. In the previously seen `vesting.py` example, the validator was in a sense parameterized via the datum. There's also another way to parameterize contracts, which is to include the parameters directly into the validator itself at compile time. In other words, Instead, the parameters are "hard-coded" into the contract, creating a family of scripts parameterized by these parameters. We show this approach here by going through a parameterized version (`parameterized_vesting.py`) of the vesting contract.

While in Plutus, compiling contracts with parameters comes with some challenges arising from the use of Template Haskel, in OpShin, things are actually quite simple. Nevertheless, we defer compiling the parameterized contract to the next lecture, as it fits better with the discussion of the off-chain code.

<!-- [NOTES TO PRESENTER]
Now, briefly show `parameterized_vesting.py` and point out the minor differences to `vesting.py`.
-->

## Trade-offs and Considerations:

Finally, let's discuss why one might actually choose one approach over the other. Here are some trade-offs to consider:
- **Discoverability vs. Separation**: Parameterizing contracts alters how they are discovered and interacted with on the blockchain. With parameters in the datum, all instances of a contract might sit at one script address, making them easily discoverable but potentially cluttered. Parameterizing the contract itself results in different script addresses for different parameter values, offering separation but potentially making discovery harder for users without specific knowledge of the parameters.
- **Constants vs. Variables**: Certain parameters of a contract may be considered constants, for example some contracts may require license tokens to be presented which are supposed to be the same for all instances of the contract. In such cases, it make sense to include these parameters directly in the contract rather than the datum. On the other hand, parameters that depend e.g. on the user currently interacting with the contract (such as the beneficiary in our vesting example) might be better placed in the datum.

## Homework

Lastly, here's a small homework assignment for you: Modify the `parameterized_vesting.py` contract to make the beneficiary a parameter of the contract, while keeping the deadline in the datum.
