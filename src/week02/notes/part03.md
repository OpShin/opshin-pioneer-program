# High-Level, Typed Validation Scripts

This lecture delves into writing slightly more sophisticated validation scripts that don't discard all input arguments. We introduce the contract `forty_two.py` which checks if the Redeemer equals the integer 42. Moreover, we discuss the benefits of using typed scripts (as in `forty_two_typed.py`) and custom data types (as in `custom_types.py`).

## Recap of Validation Scripts

Recall that validation scripts in Cardano smart contracts are pivotal for verifying transactions. They consist of three primary components which we quickly recap here in the context of the `forty_two.py` contract:

- **Datum**: Ignored in this example.
- **Redeemer**: The focus of this lecture, checked to see if it equals 42.
- **Script Context**: Also ignored in this example.

## Building a Typed Validation Script

The core idea is to transition from using low-level, untyped data representations to more specific, high-level types that accurately reflect the business logic of the smart contract.

### Implementing the Validation Logic

In the provided example, the validation logic checks if the Redeemer is precisely the integer 42, employing a simple comparison operation.

### The Role of `BuiltinData`

While the low-level approach treats all inputs as `BuiltinData`, it's advantageous to use specific types for each argument to leverage the benefits of strong typing, like compile-time error checking.

## Benefits of Typed Scripts

Using typed scripts allows for clearer, more maintainable code by ensuring that each component of the script—Datum, Redeemer, and Script Context—is accurately typed. This clarity benefits developers by making the code more intuitive and easier to debug.

## Serialization and Compilation

The lecture also covers the serialization and compilation of these typed scripts into Plutus core, which is necessary for deploying them to the Cardano blockchain. It mentions the use of utility functions for serialization, demonstrating how to prepare data for on-chain execution.

## Performance Considerations

Although typed validation scripts offer many advantages, they also introduce a performance overhead due to the need for data type conversions. The lecture hints at optimization tools and techniques that can mitigate these performance costs while maintaining type safety.

## Custom Data Types

A significant part of the lecture is dedicated to demonstrating how custom data types can be used within validation scripts. Using Template Haskell, developers can automatically generate necessary instances for custom types, simplifying the process of incorporating complex data structures into smart contracts.

### Utility for Data Serialization

The lecture introduces a utility function that facilitates the serialization of complex data types into JSON format, suitable for on-chain execution. This utility simplifies the process of preparing data for use with the Cardano CLI and other tools.

## Conclusion

This lecture provides a comprehensive overview of writing high-level, typed validation scripts for Cardano smart contracts. By emphasizing the importance of strong typing and demonstrating practical examples, it equips participants of the OpShin Pioneer Program with the knowledge to develop more sophisticated and maintainable smart contracts using Python.