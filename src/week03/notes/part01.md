<!-- [NOTES TO PRESENTER]
This lecture is mostly about having a look at the `ScriptContext` and `TxInfo` types. Probably best to open the [OpShin docs](https://opshin.opshin.dev/opshin/ledger/api_v2.html#opshin.ledger.api_v2.ScriptContext) and click around there while going through the content.
-->

# Script Contexts

This lecture delves into the third component that validator script receives: the **script context**, which plays a critical role in the functioning of smart contracts within the Cardano's eUTxO model.

## Overview of `ScriptContext`

Recall that the validator script is fed with three key pieces of information:
1. **Datum**: Originates from the transaction producing the UTXO intended for consumption.
2. **Redeemer**: Comes from the consuming transaction.
3. **Context**: Encompasses the transaction being validated, including all its inputs and outputs.

Previously, we've seen datum and redeemer in action, but the context has not been thoroughly examined until now. Unlike Bitcoin, which offers a minimal context, and Ethereum, which provides a global view of the blockchain, Cardano adopts a middle ground approach where the context is the transaction being validated. The `ScriptContext` contains a lot of useful information such as:
- When is the transaction (valid)?
- What will be the inputs of the transactions?
- What will be the outputs of the transaction?

## The Script Context Data Type

The `ScriptContext` is defined as:
```python
@dataclass()
class ScriptContext(PlutusData):
    """
    Auxiliary information about the transaction and reason for invocation of the called script.
    """

    tx_info: TxInfo
    purpose: ScriptPurpose
```
- **txInfo**: Contains all transaction information accessible from within a Plutus script.
- **Purpose**: Indicates the context or purpose for which the Plutus script is being used, such as spending, minting, rewarding, or certifying.

### Understanding `txInfo`

The most important field in the ScriptContext is the `tx_info` field which is of type `TxInfo`. It has various fields providing a comprehensive view of the transaction, including its inputs, outputs, transaction fee, certificates, and more. Here's the definition of `TxInfo`:
```python
@dataclass()
class TxInfo(PlutusData):
    """
    A complex agglomeration of everything that could be of interest to the executed script, regarding the transaction
    that invoked the script
    """

    # The input UTXOs of the transaction.
    inputs: List[TxInInfo]
    # The reference UTXOs of the transaction.
    reference_inputs: List[TxInInfo]
    # The output UTXOs created by the transaction.
    outputs: List[TxOut]
    # Transaction fee to be payed for the transaction.
    fee: Value
    # The value minted in the transaction.
    mint: Value
    dcert: List[DCert]
    wdrl: Dict[StakingCredential, int]
    valid_range: POSIXTimeRange
    # The signatures for the transaction.
    signatories: List[PubKeyHash]
    redeemers: Dict[ScriptPurpose, Redeemer]
    data: Dict[DatumHash, Datum]
    # The ID of the transaction.
    id: TxId
```
Notable fields include:
- **Inputs**: Lists all the inputs of the transaction, pointing to the outputs they intend to consume.
- **Reference Inputs**: Introduced with the Vasil hard fork, allow transactions to reference UTXOs without consuming them, mitigating bottlenecks and enabling multiple transactions to use the same UTXO within the same block for reading state.
- **Outputs**: Lists the outputs of the transaction, describing where the output sits, its value, and associated datum.
- **Fee**: The transaction fee in lovelace.
- **Minting**: Details about minting or burning of native tokens.
- **Certificates**: Related to staking actions such as delegating to a stake pool.
- **Withdrawals**: For withdrawing staking rewards.
- **Validity Range**: The time range within which the transaction is valid.
- **Signatures**: Pub key hashes that have signed the transaction.
- **Redeemers**: Mapping from script purpose to redeemer.
- **Data Map**: For datums included in the transaction body.

For completeness, we also have a quick look at the `TxInInfo` and `TxOut` types, without going into detail here:
```python
@dataclass()
class TxInInfo(PlutusData):
    """
    The plutus representation of an transaction output, that is consumed by the transaction.
    """

    out_ref: TxOutRef
    resolved: TxOut
```
```python
@dataclass()
class TxOut(PlutusData):
    """
    The plutus representation of an transaction output, consisting of
    - address: address owning this output
    - value: tokens associated with this output
    - datum: datum associated with this output
    - reference_script: reference script associated with this output
    """

    address: Address
    value: Value
    datum: OutputDatum
    reference_script: Union[NoScriptHash, SomeScriptHash]
```

### Practical Implications

Understanding `ScriptContext` and its components like `tx_info` is crucial for writing effective smart contracts. It allows for nuanced contract logic that can inspect the broader context of a transaction, including its inputs, outputs, and other critical metadata. This level of detail enhances the versatility and power of smart contracts on Cardano.

## Conclusion

The script context provides a rich source of information that smart contracts can utilize to make informed decisions. By offering a detailed view of the transaction being validated, Cardano's eUTxO model enables developers to craft sophisticated and flexible smart contract logic depite not being able to access the blockchains global state.
