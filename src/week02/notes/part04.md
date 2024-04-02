# Summary of Typed and Untyped Validators

In this lecture, we have explored various examples of validators, both untyped and typed, ranging from a very simple "always-succeed" script to a slightly more complex validator that involves checking the redeemer's value. We hope this exploration has served as a foundation for understanding the mechanisms of smart contract validation in the Cardano's eUTxO model using OpShin on-chain code.

## Key Points

- **Always Succeeds Validator**: This initial example introduced a validator that unconditionally approves transactions, completely disregarding the provided arguments (Datum, Redeemer, and Context).
- **Always Fails Validator**: As a counterpart to the first example, this validator denies all transactions, again without considering its inputs.
- **Redeemer-Specific Validator**: Moving towards more practical applications, this validator inspects the Redeemer to check for a specific value, demonstrating how to conditionally validate transactions based on Redeemer data.
- **Transition to Typed Validators**: We progressed to a typed version of the validator that not only is more reflective of real-world applications but also facilitates the use of built-in and custom data types, enhancing code readability and maintainability.
    - **Built-in Data Types**: Initially, the focus was on leveraging Cardano's `BuiltinData` type to enforce type-specific validation logic.
    - **Custom Data Types**: Expanding further, the lecture demonstrated how to incorporate custom data types into validators.
- **Realistic Use Cases**: While the examples provided primarily focused on the Redeemer, real-world applications often necessitate examining the Datum and the Context to implement comprehensive validation logic. Future lectures will delve into these aspects in detail.
- **Interaction with Cardano CLI**: An overview of utilizing the Cardano CLI to engage with the validators was also provided, showing the off-chain aspects of interacting and testing Cardano smart contracts.
- **Interaction with `pycardno`**: TODO