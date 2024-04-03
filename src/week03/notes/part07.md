# Homework

For the third week's homework in the OpShin Pioneer Program, participants are tasked with two assignments focusing on the implementation of variations and parameterizations in the vesting validator smart contract. Here's a summary of the assignments:

### Assignment 1: Dual Beneficiary Vesting Contract

Participants must implement a modified version of the vesting validator to accommodate two beneficiaries and one deadline. The requirements are as follows:

- **First Beneficiary**: Should be allowed to withdraw from the UTXO before the specified deadline.
- **Second Beneficiary**: Permitted to withdraw after the deadline has passed.

This scenario is typical of a situation where a person (the creator of the vesting contract) wishes to gift funds to the first beneficiary, but if the funds are not claimed by a certain time, the creator wants the option to reclaim them. Thus, the second beneficiary would typically be the creator themselves.

### Assignment 2: Parameterized Vesting Contract

For the second assignment, participants need to create a parameterized version of the vesting contract. In this variation:

- **Parameter**: The contract should be parameterized by the beneficiary's public key hash.
- **Datum**: The deadline should be specified within the datum of the contract.

This design suggests a more flexible implementation of the vesting contract, where the contract's logic is determined by a parameter (beneficiary) while the condition for releasing the funds (deadline) is stored within the contract's state (datum).

### Testing and Validation

- Participants are encouraged to utilize the provided test suite to verify the correctness of their implementation. Tests can be run using the command `cabal test` or specifically for this week's assignments with `cabal test week three homework`. Note the naming convention change, where homework tests are prefixed by the week number.
- Additionally, as an optional exercise, participants can enhance the DApp introduced in the lecture by implementing filters for UTXOs displayed to the beneficiary. Specifically, the DApp could be modified to only show vesting UTXOs where:
  - The connected wallet is the beneficiary.
  - The deadline has already been reached, making the funds available for claim.

These homework assignments are designed to deepen the participants' understanding of smart contract development on Cardano, focusing on conditionally releasing funds and the practical application of parameterized contracts.