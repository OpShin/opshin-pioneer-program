# Offchain Code (for the vesting example) with `pycardano` (TODO: adjust)

This lecture introduces the use of Lucid, a JavaScript-based library for interacting with the Cardano blockchain, to handle off-chain code—activities related to querying the blockchain and constructing and submitting transactions. Lucid simplifies these processes, allowing developers to work with smart contracts and blockchain data more efficiently.

### Key Concepts and Steps:

- **Off-chain Code**: Refers to interactions with the blockchain that don't occur on the blockchain itself, such as constructing transactions or querying blockchain data.
- **Lucid**: A tool that enables writing off-chain code in JavaScript or TypeScript, facilitating interactions with the Cardano blockchain without the need for manual labor involved in using command-line interfaces like the Cardano CLI.
- **Vesting Contract DApp**: The lecture demonstrates building a DApp (Decentralized Application) to interact with a vesting contract using Lucid. The contract allows locking ADA until a certain deadline, after which a specified beneficiary can unlock it.
- **Setting Up Lucid**: The process involves installing the Lucid package via npm, initializing it, and linking it with a Cardano wallet (e.g., Nami wallet) to interact with the blockchain.
- **Constructing Transactions with Lucid**: Lucid's API provides functions for constructing transactions, including specifying the recipient, amount, datum, and validity interval. It automatically handles aspects like coin selection and change outputs.
- **Querying the Blockchain**: Lucid allows querying the blockchain for specific UTXOs (Unspent Transaction Outputs) at a script address, filtering by criteria such as datum content to identify relevant UTXOs for the DApp.
- **Handling Time in Transactions**: The lecture emphasizes the importance of specifying validity intervals in transactions to ensure they are processed at the appropriate time, particularly when interacting with time-sensitive contracts like vesting contracts.
- **Example DApp**: The provided DApp demonstrates creating and claiming vestings. It showcases how to construct transactions to lock ADA in a vesting contract and how beneficiaries can claim the ADA after the vesting period has ended, all facilitated through Lucid.

### Benefits of Using Lucid:

- **Simplified Interaction**: Lucid abstracts away the complexity of directly interacting with the blockchain, providing a higher-level interface for common tasks.
- **Flexible and Powerful**: Supports constructing complex transactions, querying blockchain data, and integrating with Cardano wallets.
- **Broad Accessibility**: By leveraging JavaScript, Lucid makes blockchain development accessible to a wider range of developers familiar with web development.

### Conclusion:

The lecture effectively demonstrates the power and flexibility of using Lucid for off-chain Cardano blockchain interactions. By building a DApp to interact with a vesting contract, it showcases how developers can create user-friendly blockchain applications with reduced complexity and increased efficiency.