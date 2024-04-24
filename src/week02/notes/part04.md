<!-- [NOTES TO PRESENTER]
This is just a summary of parts 1-3. So it can also be quite short.
-->

# Summary of Typed and Untyped Validators

This week, we have explored various examples of validators, both untyped and typed, ranging from a very simple "always-succeed" script to a slightly more complex validator that involves checking the redeemer's value. We hope this exploration has served as a foundation for understanding the mechanisms of smart contract validation in the Cardano's eUTxO model using OpShin on-chain code.

## Key Points

- **Always Succeeds Validator**: This initial example introduced a validator that unconditionally approves transactions, completely disregarding the provided arguments (Datum, Redeemer, and Context).
- **Always Fails Validator**: As a counterpart to the first example, this validator denies all transactions, again without considering its inputs.
- **Redeemer-Specific Validator**: Moving towards more practical applications, this validator inspects the Redeemer to check for a specific value, demonstrating how to conditionally validate transactions based on Redeemer data.
- **Transition to Typed Validators**: We progressed to a typed version of the validator that not only is more reflective of real-world applications but also facilitates the use of built-in and custom data types, enhancing code readability and maintainability.
    - **Built-in Data Types**: Initially, the focus was on leveraging Cardano's `BuiltinData` type to enforce type-specific validation logic.
    - **Custom Data Types**: Expanding further, the lecture demonstrated how to incorporate custom data types into validators.
- **Realistic Use Cases**: While the examples provided primarily focused on the Redeemer, real-world applications often necessitate examining the Datum and the Context to implement comprehensive validation logic. Future lectures will delve into these aspects in detail.
- **Interaction with Cardano CLI**: An overview of utilizing the Cardano CLI to engage with the validators was already provided in the original Plutus Pioneer Program. The lessons learned there apply directly to OpShin smart contracts.
- **Interaction with `pycardno`**: We have written our first small `pycardano` off-chain script that lets us interact with our simple gift contract. The interaction involved two transactions: First sending funds to the gift contract and then collecting them back by spending the script UTxO.

Exciting content is to come next week as we will dive into building more complex validators and exploring the interaction between on-chain and off-chain components in greater detail. But first, we encourage you to take a look at this weeks homework assignment which is presented in the next and lest section of week 2.