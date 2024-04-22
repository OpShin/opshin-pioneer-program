# Interacting with a Mock Environment

One way of testing a smart contract would be to deploy it e.g. on testnet. However, this takes quite some work:
1. setting up wallets containing the Ada / native token amounts needed for the test
2. constructing a transaction that sends funds (perhaps with a datum) to the script address
3. submitting the transaction
3. waiting until the UTxO is available onchain
5. constructing the transaction that spends the script UTxO (includes construction of redeemer)
6. submitting the transaction

But actually, most of the steps are unnecessary, since all we want to test is the validator itself. So ideally, we want a testing environment that saves us all the steps that are not related to the validator itself. The only thing that we should be doing is construct datum, redeemer, and the transaction spending from the script. This can be accomplished by having a mock environment simulating the blockchain state that the script gets to see, namely the `ScriptContext`, by providing a mock version of it. The respective addresses occuring in this mock context will belong to mock users.

## Mock Script Context and User

We now briefly show what this ...

## Simulating contract interactions

Talk about `test_mock.py`.