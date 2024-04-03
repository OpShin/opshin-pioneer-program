# Summary

- **Script Context and `TxInfo`**: In the third lecture, we started by examining the script context type, particularly focusing on the `TxInfo` type, which provides all information about a transaction visible to OpShin. This was an introduction to understanding how transactions are validated and interacted with in OpShin.

- **Handling Time in OpShin**: We then discussed how time is handled in OpShin, enabling the maintenance of determinism in contracts while considering the current time. An example was provided to demonstrate how time can be effectively managed within smart contracts.

- **Parameterized Scripts**: Following this, the concept of parameterized scripts was introduced. These are scripts that depend on parameters, allowing for a more dynamic and versatile approach to smart contract development. 

- **Off-chain code in `pycardano`**: Switching to off-chain code, we saw how to use Lucid for interacting with the blockchain, constructing, and submitting transactions. A DApp example was given for interacting with the previously mentioned vesting contract, showcasing practical application of off-chain code.

- **Reference Scripts**: Finally, we explored reference scripts, introduced by the Vasil hard fork, which optimize transaction sizes by allowing scripts to reference existing scripts on the blockchain rather than including them in every transaction. An example DApp utilizing reference scripts was shown, demonstrating their deployment and usage.

- **Conclusion**: In summary, this lecture covered the script context, time handling in OpShin, parameterized scripts, off-chain code with Lucid, and the use of reference scripts. This combination of topics provided a comprehensive overview of developing smart contracts on Cardano, from the on-chain logic to off-chain interaction and optimization strategies.