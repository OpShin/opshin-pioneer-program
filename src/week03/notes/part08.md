# Summary

- **Script Context and `TxInfo`**: In the third lecture, we started by examining the script context type, particularly focusing on the `TxInfo` type, which provides all information about a transaction visible to OpShin. This was an introduction to understanding how transactions are validated and interacted with in OpShin.

- **Handling Time in OpShin**: We then discussed how time is handled in OpShin, enabling the maintenance of determinism in contracts while considering the current time. An example was provided to demonstrate how time can be effectively managed within smart contracts.

- **Parameterized Scripts**: Following this, the concept of parameterized scripts was introduced. We've seen how to "hard-code" parameters into a  contract at compile time as an alternative to passing those parameters as part of the datum.

- **Off-chain code in `pycardano`**: Switching to off-chain code, we saw how to use `pycardano` for interacting with the blockchain, constructing, and submitting transactions. We've successfully interacted with our vesting contract and could inspect the resulting transaction via a blockchain explorer.

- **Reference Scripts**: Finally, we explored reference scripts, introduced by the Vasil hard fork, which optimize transaction sizes by allowing scripts to reference existing scripts on the blockchain rather than including them in every transaction. Again, we've seen this in action for the vesting example demonstrating the deployment and usage of reference scripts.

- **Conclusion**: In summary, this lecture covered the script context, time handling in OpShin, parameterized scripts, and off-chain code with `pycardano`. This combination of topics provided a comprehensive overview of developing smart contracts on Cardano, from the on-chain logic to off-chain interaction as well as more advanced optimizations like reference scripts. We've covered a lot of ground this week!