# Setting up Our Development Environment

Today, we will guide you through setting up your development environment which is of course important to have in place before we can start with the actual OpShin smart contract development. Today we will show the primary/recommended setup option that we will be using throughout the program. The development environment itself will be a local setup. However, for interacting with the Cardano testnet, we will be using API services provided by [Blockfrost](https://blockfrost.io/) which for the testnet are offered on a free plan.

There are also other potential setup that may be of interest to some of you. For example, in the original Plutus Pioneer Program, it was shown how to develop in a completely remote environment via infrastructure provided by [Demeter.run](https://demeter.run). It is also easy to setup and can be a good option if you prefer to work in a fully browser-based environment.

Alternatively, for those who prefer a fully local setup, the Plutus Pioneer Program also briefly showed how to set up a local node that can be used for interacting with the Cardano testnet. If you are interested in either of these two alternative setups, feel free to check out Part 2 of the first week of the Plutus Pioneer Program (which we will link below).

<!-- [NOTES TO PRESENTER]
For the following part, go through the steps on screen.
-->

## Walking through the Setup

Let's have a look at how to setup a blockfrost testnet project and obtain the API key that we will need to use their API for interacting with the Cardano testnet. Let's together go through the following steps:
1. Make a new account (if you don't have one already) on [Blockfrost](https://blockfrost.io/).
2. Go to the dashboard.
3. Create a new project by clicking on `Add Project`, giving it a name, selecting the Cardano preprod testnet, and clicking `Save Project`.
4. Click on the project you just created and copy the project ID. This is our API key that we will need to use the Blockfrost API.

Now we want to setup the OpShin pioneer program repository and check if the setup with the API key we just obtained works as expected.
1. Clone the repository from [GitHub](https://github.com/OpShin/opshin-pioneer-program).
2. Install poetry using `curl -sSL https://install.python-poetry.org | python3 -`.
3. Install the dependencies using `poetry install`.
4. Create a `.env` file in the root directory of the repository and add the following line: `BLOCKFROST_PROJECT_ID=<your_project_id>`.
5. Enter the virtual environment using `poetry shell`.
6. Run the test script by navigating to `src/week01` and running `python scripts/check_setup.py`. If everything is set up correctly, the latest block's slot number should be printed. We can compare this to what's shown on [CExplorer](https://preprod.cexplorer.io/block).

## Conclusion

We hope that you now all have a working setup. With the "boring" part out of the way, we are already looking forward to welcoming you again in next week's lecture where we will dive into the smart contract development itself. As mentioned before, we also recommend you to watch the alternative setup options presented in the Plutus Pioneer Program. As these things are mostly the same for OpShin and Plutus development, we do not provide duplicate lectures for this here. Remains to conlude this week with a last part on homework. See you there!
