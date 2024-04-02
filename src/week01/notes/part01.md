# Welcome & Introduction

Welcome to the OpShin Pioneer Program, an introductory lecture series into writing Cardano Smart Contracts using OpShin, an alternative smart contract language based on Python. This program is inspired by Lars Brünjes' Plutus Pioneer Program and funded by Project Catalyst Fund 9. Led by OpShin creator Niels, this course is designed to equip you with all the knowledge needed to develop your own smart contracts on Cardano using OpShin.

# Lectures

- All lectures are pre-recorded and published on the OpShin YouTube channel.
- The lecures' structure closely follow the Plutus Pioneer Program. Whenever, the covered content is independent of the smart contract language, instead of providing a duplicate lecture, a link to the corresponding Plutus Pioneer lecture will be given. Otherwise, we recreate the content in the context of OpShin.
- All code examples and homework assignments, including solutions, are available via the opshin-pioneer-program repository on GitHub.

# EUTxO Model

- One major goal of the program is to understand the Extended Unspent Transaction Output (EUTxO) model, which is the underlying model for Cardano smart contracts.
- Understanding the EUTxO model is crucial for successfully developing in Cardano, and often requires taking a different approach from what is done in account-based models like Ethereum's.
- The EUTxO model provides security and deterministic transactions, enabling more predictable and secure contract designs.

# OpShin

- OpShin is an implementation of smart contracts for Cardano, written in a strict subset of valid Python. It aims to ensure that if a program compiles, it is not only a valid Python program but also behaves identically when executed on-chain and off-chain.
- Why choose OpShin for Cardano smart contract development?
    - **100% Valid Python**: Leverage the full stack of Python development tools, including syntax highlighting, linting, debugging, unit testing, property-based testing, and verification.
    - **Intuitive**: OpShin maintains the simplicity and readability of Python, making smart contract development accessible and straightforward.
    - **Flexible**: Whether you prefer an imperative or functional style, OpShin accommodates various programming paradigms.
    - **Efficient & Secure**: With static type inference, OpShin ensures strict typing and optimized code, enhancing both performance and security.
- For this program, familiarity with Python is recommended but not stricly required. We will start with simple examples and since Python syntax is often straightforward and intuitive, you should be able to follow along even if you are new to Python.

# Setup (TODO: Update)

Setting up for OpShin development has been made straightforward with two primary options:

1. A browser-based environment, enabling you to start developing with just one click, without worrying about local dependencies.
2. A Dev container for Visual Studio Code, for those who prefer working locally, designed to simplify setup and align with existing Python development practices.

# Conclusion

The OpShin Pioneer Program offers an exciting opportunity to explore and innovate on the Cardano blockchain using Python. Despite the challenges associated with learning a new smart contract model, the program aims to simplify the learning process and setup. This series sets the stage for you to contribute to the growing ecosystem of Cardano smart contracts, fostering innovation and development in this emerging field.
