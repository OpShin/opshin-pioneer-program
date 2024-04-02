# A Vesting Example

This lecture introduces a practical example of a vesting smart contract in Plutus, inspired by a real-world scenario where ADA is gifted to a child but is only accessible when they reach a certain age.

## Concept of Vesting

- **Vesting Scheme**: A mechanism that locks ADA (or any cryptocurrency) and only makes it available to the beneficiary after a specified deadline.
- **Use Case**: Gifting ADA to a child with the condition that the funds become accessible when they reach adulthood.

## Implementation Details

### Vesting Contract Components

- **Custom Data Type**: The contract uses a custom datum type called `VestingDatum`, comprising:
  - `beneficiary`: Identified by a public key hash.
  - `deadline`: Specified as a POSIX time.

- **Validation Logic**: The contract ensures that the ADA can only be unlocked after a predefined deadline and by a transaction signed by the beneficiary's key.

### High-Level Typed Validators

- The implementation leverages high-level typed validators with custom data types, showcasing how to build more complex and secure smart contracts in Plutus.
- Two main conditions are validated:
  1. **Transaction Signed by Beneficiary**: Utilizes the `txSignedBy` function to verify if the transaction is indeed signed by the beneficiary.
  2. **Deadline Reached**: Employs time handling to ascertain that the current time is after the specified deadline before unlocking the funds.

### Working with Time

- **Deterministic Validation**: Cardano's approach to handling time ensures deterministic validation. The transaction specifies a valid time range, checked before script execution.
- **Interval Contains Function**: The `contains` function is used to ensure the transaction's time interval falls entirely after the deadline, allowing for deterministic validation despite the flow of real time.

## Key Takeaways

- **Flexibility**: This vesting contract example illustrates the flexibility of smart contracts in handling complex conditions, such as time-based constraints.
- **Practical Use Cases**: Vesting scenarios are common in various contexts, making this example relevant for a wide range of applications.
- **Adaptability**: While the example focuses on unlocking by the beneficiary, the logic can be adapted to allow others to unlock the UTXO, provided the funds are directed to the beneficiary. This adaptability underlines the power of smart contracts to cater to diverse requirements.

## Conclusion

The vesting smart contract example provides a comprehensive look at how to implement time-based conditions and beneficiary-specific validations in Plutus. It demonstrates the utility of smart contracts in creating secure, flexible, and real-world applicable financial instruments on the Cardano blockchain.