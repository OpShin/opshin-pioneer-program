# Homework

For this week's homework, you are tasked with working on two validators provided in `homework/homework1.py` and `homework/homework2.py`. The process for both is identical, and it involves two main steps:

1. **Understand the Validator**: Utilize all the resources and tools available to you, such as tests, source code, and examples from previous validators, to determine the function of the validator. These tools should provide sufficient information for you to comprehend what each validator is designed to do.

2. **Write Off-Chain Code**: Once you have a clear understanding of the validator's purpose and functionality, you are to write the necessary off-chain code to interact with the validator. This code should enable all possible interactions with the validator. You have the freedom to use any tool of your choice for this task.

The key difference between the two validators you will be working with is that one is parameterized, and the other is not. This distinction influences how you approach writing the off-chain code for each validator but the fundamental task remains the same for both.

## Testing

As in last week's homework, you can run some tests to check the logic of your validator implementations by running
```bash
pytest tests/test_homework.py
```