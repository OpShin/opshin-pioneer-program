# Homework

For the third week's homework in the OpShin Pioneer Program, we have two assignments for you:

### Assignment 1: Dual Beneficiary Vesting Contract

We ask you two implement a modified version of the vesting validator that has two beneficiaries and one deadline. The requirements are as follows:
- **First Beneficiary**: Should be allowed to withdraw from the UTxO before the specified deadline.
- **Second Beneficiary**: Permitted to withdraw after the deadline has passed.

This scenario is typical of a situation where a person (the creator of the vesting contract) wishes to gift funds to the first beneficiary, but if the funds are not claimed by a certain time, the creator wants the option to reclaim them. Thus, the second beneficiary would typically be the creator themselves.

### Assignment 2: Partially Parameterized Vesting Contract

For the second assignment, participants need to create a "partially" parameterized version of the vesting contract, as follows:
- **Parameter**: The contract should be parameterized by the beneficiary's public key hash.
- **Datum**: The deadline should be specified within the datum of the contract.

This design suggests a more flexible implementation of the "fully" parameterized vesting contract, where the deadline remains to flexible, i.e., to be chosen by the provider of the funds.

### Testing and Validation

You are encouraged to use the provided test suite to verify the correctness of your validator implementations. Here's how you can run the tests
```bash
pytest tests/test_homework.py
```
Once you have the validator logic implemented correctly, all tests should pass successfully.