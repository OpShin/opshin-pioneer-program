<!-- [NOTES TO PRESENTER]
Extremely short lecture, first showing `forty_two.py` and then `forty_two_typed.py` to show 1) how to use the redeemer to write a "non-trivial" validator, and 2) how to use types to make the code more robust and readable.
-->

# High-Level, Typed Validation Scripts

This lecture delves into writing slightly more sophisticated validation scripts that don't discard all input arguments. We introduce the contract `forty_two.py` which checks if the Redeemer equals the integer 42. Moreover, we discuss the benefits of using typed scripts (as in `forty_two_typed.py`) and custom data types (as in `custom_types.py`).

## Recap of Validation Scripts

Recall that validation scripts in Cardano smart contracts are pivotal for verifying transactions. They consist of three primary components which we quickly recap here in the context of the `forty_two.py` contract:

- **Datum**: Ignored in this example.
- **Redeemer**: The focus of this lecture, checked to see if it equals 42.
- **Script Context**: Also ignored in this example.

### Implementing the Validation Logic

In the provided example, the validation logic checks if the Redeemer is precisely the integer 42, employing a simple comparison operation.

### From `BuiltinData` to typed validation scripts

While the low-level approach treats all inputs as `BuiltinData`, it's advantageous to use specific types for each argument to leverage the benefits of strong typing, like compile-time type checking. Let's compare `forty_two.py` with the typed version `forty_two_typed.py` and observe how `BuiltinData` is replaced with more specific types, making the code more readable and robust. The additional information introduced through types will make your code more intuitive and easier to debug.

## Conclusion

This was a short but nevertheless important lecture on how to turn a simple untyped validation script into a typed one. From now one, we will always stick to using types for Datum, Redeemer, and Context. This will be important to keep an overview, especially when the validation logic becomes more complex.
