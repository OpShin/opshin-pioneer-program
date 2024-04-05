# Reference Scripts

This lecture introduces the concept of reference scripts on the Cardano. After briefly explaining the purpose and benefits of reference scripts, we will demonstrate how to use them in practice by again modifying the vesting example.

## Reference Scripts Overview:

So what are reference scripts?

- **Reference Scripts**: Introduced in the Vasil hard fork, reference scripts allow a script to be stored in a UTxO and then referenced by other transactions without including the script itself in each transaction. This approach reduces blockchain bloat by avoiding the duplication of scripts across multiple transactions.
- **Deployment**: Reference scripts need to be deployed to the blockchain once, after which they can be referenced repeatedly. A common practice is to deploy reference scripts to a "burn" address—a special address from which tokens cannot be retrieved—ensuring the script remains accessible indefinitely.

Let's see how we can deploy a reference script for the vesting contract.

## Deplying a Reference Script using `pycardano`

Let's have a look at the `scripts/submit_ref_scripts.py` script that deploys our contracts as reference scripts. After running the script, we can inspect the created UTxO on CExplorer.

## Using the Reference Scipts

In the vesting example, the `make_vest.py` part remains unchanged as we just send the funds to the vesting script address which is of course the same independent of whether we want to use reference scripts or not.

For the `claim_vest.py` part, we need to modify the transaction to reference the deployed vesting script instead of including it directly. This is achieved by specifying the UTxO containing the reference script as an input to the transaction, as we will see in the code (`scripts/claim_vest_ref.py`).

<!-- [NOTES TO PRESENTER]
Go through the code `scripts/claim_vest_ref.py`, and point out difference between including the full script and using the reference UTxO.
-->

## Conclusion:

We have now learned what reference scripts are and how we can use them. Generally, during the development phase of a project, it might be easier to include the full script in each testnet transaction (as the contract is anyways still being adjusted). For the final deployment of a mainnet dApp's contracts, however, there is no reason not to use reference scripts in order to spend as many script UTxOs as possible and not be limited by bounds on the maximum transaction size.