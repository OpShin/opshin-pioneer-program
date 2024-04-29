# Homework Assignment

This week, you are tasked with implementing two simple validators. You will find the starter code in `homework/homework1.py` and `homework/homework2.py`, respectively.

## Assignment 1: Boolean Pair Validator

- **Redeemer type**: The validator will be passed a list of two booleans (i.e. you can assume it will always be exactly two).
- **Desired validation logic**: The validator should approve the transaction if and only if both booleans in the pair are `True`.

**Instructions**:
1. Identify the incorrect implementation provided in the module.
2. Replace the current (wrong) logic with the correct validation logic as described.
3. Once your solution is implemented, use the provided `tests` to verify its correctness. You can run the tests using
```bash
cd src/week02
pytest tests/test_homework.py
```
Once the logic is implemented correctly, the first test which is meant to check homework 1 should pass sucessfully. (Note that we will get to how to write such tests yourself later on in week 6.)

## Assignment 2: Custom Data Type Validator

- **Redeemer type**: A custom data type named `MyRedeemer`, which essentially is a record with two fields (`flag1` and `flag2`), both of type `bool`.
- **Desired validation logic**: A UTxO locked with this validator should be spendable if and only if `flag1` and `flag2` are not equal.

**Instructions**:
1. Similar to Assignment 1, locate the placeholder logic meant to be replaced.
2. Implement the validation logic ensuring that it checks for the flags to be different for a transaction to be validated successfully.
3. Test your implementation using `pytest tests/test_homework.py`. Once the logic is correctly implemented, all tests should pass.

## Additional Exercise: Interacting with Smart Contracts

After completing the above tasks, you are encouraged to interact with your smart contracts using `pycardano` or the Cardano CLI. Experiment with providing incorrect redeemers to observe the resulting behavior and error messages. For instance:
- In Assignment 2, try submitting a redeemer where `flag1` and `flag2` are the same, contrary to the validation logic, and note the error message received.

This exercise will give you hands-on experience with deploying and testing smart contracts on the Cardano blockchain and familiarize you with the error handling mechanisms in place.
