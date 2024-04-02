# Parameterized Contracts

This lecture introduces the concept of parameterized contracts, moving away from the simpler examples of validators previously discussed. In the context of a vesting contract, where ADA is gifted with constraints on when it can be accessed, this approach offers an alternative to using the datum to include variability, such as the beneficiary and deadline. Instead, these variables are "hard-coded" into the contract, creating a family of scripts parameterized by these variables.

### Key Concepts:
- **Parameterized Contracts**: Unlike earlier examples that relied on datum for introducing variability, parameterized contracts incorporate variability directly into the contract itself. This is achieved by defining a family of scripts that can be initialized with specific parameter values.
- **Vesting Contract Example**: A practical example provided is a vesting contract, where ADA can only be accessed by a child when they reach a certain age, say 18 or 21. This smart contract specifies a beneficiary and a deadline, enforcing that the ADA can only be unlocked after the deadline and if the transaction is signed by the beneficiary's key.
- **Implementation Changes**: To adapt the vesting contract to a parameterized approach, changes include:
  - Modifying the datum type to include the parameters directly.
  - Adjusting the validator function to take an additional parameter for the contract parameters.
  - Utilizing the `applyCode` and `liftCode` functions to handle the parameter at runtime, as template Haskell operates at compile time and cannot directly compile runtime-known parameters into Plutus Core.

### Challenges and Solutions: (TODO review)
- **Template Haskell Limitations**: One significant challenge is that template Haskell, used for compiling Haskell to Plutus Core, operates at compile time. Since the parameters (e.g., beneficiary's public key hash and deadline) are known only at runtime, the direct approach of compiling these parameters into the contract is not feasible. The solution involves using `liftCode` to compile these parameters at runtime and `applyCode` to apply the compiled parameters to the Plutus Core function representing the contract.
- **Parameter Instances**: For the approach to work, the parameter types must be instances of the `Lift` class, which is possible for data-like types but not for function-like types. The lecture demonstrates using Template Haskell to automatically derive these instances for custom data types.

### Trade-offs and Considerations:
- **Discoverability vs. Separation**: Parameterizing contracts alters how they are discovered and interacted with on the blockchain. With parameters in the datum, all instances of a contract might sit at one script address, making them easily discoverable but potentially cluttered. Parameterizing the contract itself results in different script addresses for different parameter values, offering separation but potentially making discovery harder for users without specific knowledge of the parameters.
- **Homework Assignment**: The lecture concludes with a homework assignment asking participants to modify the vesting contract. This modification involves making the beneficiary a parameter of the contract but leaving the deadline within the datum, aiming to balance discoverability and organization of vesting contracts on the blockchain.

This parameterized approach provides a more flexible and scalable way to design smart contracts, allowing for a broad range of applications beyond the vesting example provided.