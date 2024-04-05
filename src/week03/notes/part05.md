# Offchain Code with `pycardano`

In this lecture, we will show the `pycardano` off-chain code for interacting with the vesting (and parameterized vesting) example contract that we wrote using OpShin in the previous session. This will involve two steps: First, we show how to construct and submit a transaction for depositing funds into the vesting contract. Second, we show how to construct and submit the transaction for claiming the funds from the vesting contract that were locked in the previous step (after the deadline has passed).

## Building the Contracts

First, if we haven't done so already, we need to build our OpShin contract. We can do this by simply running:
```bash
cd src/week03/lecture
python scripts/build.py
```
<!-- [NOTES TO PRESENTER]
Briefly open the `build.py` script and show that it simply runs opshin on the contract. Also show the build directory and the generated files.
-->
Building the parameterized vesting contract actually additionally requires us to pass in the parameter, i.e., the `VestingParams`. We will see how to do this in a moment.

## Depositing Funds

Let's start by depositing funds into the vesting contract. This is done in `scripts/make_vest.py`.
<!-- [NOTES TO PRESENTER]
Go through the construction an submission of the vesting tx. Also mention here how the parameterized version is compiled by passing the `VestingParams` as an argument to `opshin`.
-->
Let's see this in action. Run
```bash
python scripts/make_vest.py
```
and inspect the generated transaction on CExplorer.

## Claiming Funds

The next step is of course to claim the funds. After we've waited for the deadline to pass, we can do so via `scripts/claim_vest.py`. It involves the following steps which we now go through in the code:
 - loading the script
 - finding the UTxO to spend
 - parsing the datum
 - adding a collateral input
 - constructing the transaction (using an empty redeemer)
 - signing and submitting the transaction
Let's run the script and inspect the resulting transaction on CExplorer.


## Conclusion:

In this lecture we have seen a practical example of how to both send funds to and claim funds from a contract using `pycardano`. This is an important step towards understanding the off-chain part of smart contract development on Cardano.
