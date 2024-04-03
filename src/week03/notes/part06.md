# Reference Scripts (TODO: adjust to `pycardano`)

This lecture introduces the concept and implementation of reference scripts on the Cardano blockchain, particularly focusing on their usage within a decentralized application (DApp) developed with Lucid, a JavaScript library for interacting with the Cardano blockchain.

### Reference Scripts Overview:

- **Reference Scripts**: Introduced in the Vasil hard fork, reference scripts allow a script to be stored in a UTXO (Unspent Transaction Output) and then referenced by other transactions without including the script itself in each transaction. This approach reduces blockchain bloat by avoiding the duplication of scripts across multiple transactions.
- **Deployment**: Reference scripts need to be deployed to the blockchain once, after which they can be referenced repeatedly. A common strategy is to deploy reference scripts to a "burn" address—a special address from which tokens cannot be retrieved—ensuring the script remains accessible indefinitely.

### Implementation Steps in Lucid DApp:

1. **Burn Script Deployment**: The lecture demonstrates deploying a vesting contract script as a reference script to a burn address. This ensures the script is permanently available on the blockchain for other transactions to reference.

2. **Lucid Initialization**: The DApp uses Lucid to interact with the Cardano blockchain, initializing the library and linking it to the Nami wallet for transaction signing and submission.

3. **Script Deployment**: The code includes functionality to deploy the vesting script to the burn address as a reference script. This involves constructing a transaction that includes the script and specifies the burn address as the recipient, ensuring the script cannot be spent.

4. **Creating and Claiming Vestings**: The DApp allows users to create new vesting contracts by specifying a beneficiary, amount, and deadline. Users can also claim vested funds after the deadline has passed. Transactions to claim funds reference the deployed vesting script using Lucid's `refFrom` function.

5. **Using Reference Scripts**: When claiming vested funds, the DApp constructs a transaction that references the deployed vesting script instead of including it directly. This is achieved by specifying the UTXO containing the reference script as an input to the transaction, reducing the transaction size and cost.

### Benefits of Reference Scripts:

- **Efficiency**: Reference scripts reduce the size and cost of transactions by eliminating the need to include the script in every transaction that interacts with it.
- **Permanence**: Deploying reference scripts to a burn address ensures they are always available and cannot be accidentally or maliciously removed.
- **Simplicity**: Lucid abstracts the complexity of referencing scripts in transactions, making it easier for developers to utilize this feature in their DApps.

### Conclusion:

The lecture highlights the practical application of reference scripts in Cardano DApps, using Lucid for seamless blockchain interaction. By deploying a vesting script as a reference script to a burn address, the DApp demonstrates an efficient, cost-effective, and developer-friendly approach to implementing smart contracts on Cardano.