# Homework

## Introduction to Swap Contracts
In this session, we explore the use of swap contracts in scenarios such as selling tokens or trading NFTs securely. The traditional method of two separate transactions (one sending the asset and the other sending the payment) exposes the seller to the risk of non-payment. To mitigate this risk, a swap contract can be used.

## Swap Contract Structure
- **Purpose**: Securely trade tokens or NFTs by ensuring that the seller receives the agreed-upon payment in the same transaction as the asset transfer.
- **Mechanism**:
  1. **Locking Assets**: The seller locks the tokens or NFT into a validator script.
  2. **Setting Terms**: The script includes a custom datum specifying the beneficiary (seller) and the price.
  3. **Executing Trade**: To retrieve the locked assets, the buyer must send the correct payment to the beneficiary as part of the transaction.

## Validator Logic
- **Custom Datum**: Includes the beneficiary's public key hash and the price.
- **Redeemer**: Typically a simple unit value is used for redeeming.
- **Validation Check**: Ensures that an output exists in the transaction sending the specified price in ADA to the beneficiary. This is achieved by:
  - Checking all transaction outputs to see how much is paid to the beneficiary’s public key hash.
  - Confirming the amount matches the price listed in the datum.

## Vulnerability and Testing
- **Identified Vulnerability**: If multiple UTXOs are created with the same beneficiary and price, a buyer could satisfy multiple contracts with a single payment equal to one contract’s price. This is due to the validator only checking for the presence of a payment matching the price, not tying the payment to a specific UTXO.
- **Homework Assignment**:
  1. **Write Tests**:
     - **Normal Spending Test**: Validate that a transaction where a buyer pays the correct amount for one NFT works as expected.
     - **Double Spending Test**: Test the scenario where a buyer tries to acquire two NFTs (from two separate UTXOs with the same price) with a single payment meant for one. This should fail but will initially pass due to the vulnerability.
  2. **Fix the Validator**: Modify the validator script to prevent this double spending by either:
     - Adding a unique identifier to each datum to differentiate each contract.
     - Ensuring the transaction consumes only one output per payment.
  3. **Re-test**: After modifying the validator, run the tests again to confirm that the vulnerability is addressed.

## Additional Resources and Support
- Participants are encouraged to engage with the community on Discord for discussions and queries.
- The solution to the homework will be posted in the solutions branch after one week to provide further guidance.

## Conclusion
This homework exercise not only teaches the implementation of a swap contract but also highlights the importance of comprehensive testing to uncover and fix potential vulnerabilities in smart contract design. Happy coding, and remember to verify thoroughly to ensure your smart contracts are secure and function as intended.