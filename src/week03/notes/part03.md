<!-- [NOTES TO PRESENTER]
This entire content of this lecture is to walk people through `src/week03/lecture/vesting.py`. Here are some general things that can be mentioned while going through the code.
-->

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
  1. **Transaction Signed by Beneficiary**: We write a custom `signed_by_beneficiary` function which checks whether the required signer is in `context.tx_info.signatories`.
  2. **Deadline Reached**: Employs time handling as introduced in the previous lecture to make sure that the current time is after the specified deadline before unlocking the funds.

### Working with Time

- **Deterministic Validation**: Cardano's approach to handling time ensures deterministic validation. The transaction specifies a valid time range, checked before script execution.
- **Interval Contains Function**: The `contains` function is used to ensure the transaction's time interval falls entirely after the deadline, allowing for deterministic validation despite the flow of real time.

## Conclusion

The vesting smart contract example provides a comprehensive look at how to implement time-based conditions and beneficiary-specific validations in OpShin. We have just made a big step towards understanding smart contracts that can actually power real-world applicable financial instruments on Cardano.