# How to Interact with Smart Contracts

In this lecture, we will learn how to interact with the basic `gift` contract that we looked at and compiled in the previous session. Actually, we want to point out two different ways of doing so:

## Using the Cardano CLI

In the original Plutus Pioneer Program, the Cardano CLI was used to interact with their `gift` contract. As contracts written in OpShin can be interacted with in just the same way as with the ones written in Plutus, we refer to the corresponding [lecture of the Plutus Pioneer Program](https://www.youtube.com/watch?v=2MbzKzoBiak) to learn how to use the Cardano CLI.

## Using `pycardano`

Another way to interact with Cardano smart contracts is via the `pycardano` python library. In the following lectures, off-chain components will mostly be written in python and using `pycardano`. Therefore, we use the `gift` example here to demonstrate how to recreate the same functionality as in the CLI version with `pycardano`. Let's together go through the following steps:

1. Set up the environment by going to the root directory of the `opshin-pioneer-program` repository and running:
```bash
poetry install
poetry shell
```
2. Make sure you have the `.env` file in the root directory of the repository and check that it contains a valid blockfrost preprod project API key (as described in part 2 of week 1): `BLOCKFROST_PROJECT_ID=<your_project_id>`.
3. Create a new key-pair and address using
```bash
python scripts/create_key_pair.py alice
```
the result of which is then stored in `keys`.
4. Fund `alice.addr` with some `tAda` via the preprod [testnet faucet](https://docs.cardano.org/cardano-testnet/tools/faucet/).
5. Now, we create a transaction that sends funds to the `gift` contract's address. Let's go through the respective `pycardano` code in `src/week02/scripts/make_gift.py` and then run it:
```bash
cd src/week02
python scripts/make_gift.py
```
Let's inspect the resulting transaction on [Cexplorer](https://preprod.cexplorer.io).
6. Similarly, go through the `src/week02/scripts/collect_gift.py` script,
```bash
python scripts/collect_gift.py
```
and look at the transaction on [Cexplorer](https://preprod.cexplorer.io).

## Conclusion

That's it for today. We have seen two different ways (via Cardano CLI, and `pycardano`) to construct the "make_gift" and "collect_gift" transactions for interacting with our simple contract. Especially for bigger projects it will be very useful to have the off-chain part written in `pycardano` since Python is a powerful and popular language that we can then use to build all the necessary logic for our dApp. Moreover, having both off-chain and on-chain code written in the same language will often spare us some work as it avoids recreating the same logic in two different languages.