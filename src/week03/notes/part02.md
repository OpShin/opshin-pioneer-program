<!-- [NOTES TO PRESENTER]
For the first "thoery" part, one can show the [time chapter of OpShin Book](https://book.opshin.dev/smart_contract_tour/handling_time.html) as it has some pictures for time ranges.
-->

# Handling Time

In a lot of contracts, it is essential to have consider time for determining whether the transaction whould be valid or not. This lecture addresses the challenge of integrating time into the deterministic validation process of Cardano's Extended UTXO model, emphasizing the importance of handling time without sacrificing the advantages of validation occurring within the wallet.

## The Dilemma of Time

- **Deterministic Validation**: One of Cardano's strengths is ensuring that if validation succeeds in the wallet, it should also succeed on the blockchain, barring issues like input consumption by another transaction. This predictability is crucial for avoiding failed transactions and unnecessary fees.
- **The Role of Time**: Introducing time into this deterministic model poses a challenge. The validation logic might need to consider transactions valid only before or after certain times, but how can this be reconciled with the flow of real time and the need for deterministic validation?

## Cardano's Solution: POSIX Time Range

- Cardano resolves this dilemma with the `POSIXTimeRange` field in transactions, specifying the valid time interval for a transaction. This approach ensures that:
  1. Time-related validation checks occur before script execution.
  2. If a transaction's time range does not match the current time at validation, it fails immediately before any script runs.
  3. This mechanism enables deterministic validation by treating the time range as static data during script execution.

## Important Considerations

- **Slot vs. Real Time**: Cardano's consensus protocol operates on slots, while Plutus scripts use real time. The system must convert between these two, considering potential future changes in slot duration.
- **Future Time Bounds**: Transactions can specify time bounds, but due to potential changes in slot length, definite upper bounds must not be set too far in the future (typically no more than 36 hours ahead), ensuring compatibility with future protocol changes.

## Working with Intervals

- An interval in Plutus scripts is defined by its lower and upper bounds, which can be inclusive or exclusive, finite, or infinite. This flexibility allows scripts to define precise conditions based on time.
- The lecture provided examples of working with intervals using integers for simplicity, showcasing operations like membership tests, intersections, and containment checks.

<!-- [NOTES TO PRESENTER]
Open a terminal and walk viewers through the following example.
-->

## Hands-on Example

Let's see a hands-on example of working with time intervals in OpShin. For this, we open the Python shell in a terminal and import the `interval` package from `opshin.ledger` as follows:
```poetry
poetry shell
python
```

```python
from opshin.ledger import interval
```

Now, suppose our transaction is valid for the interval `[-3, 2]`. We can create this interval as follows:
```python
tx_valid = make_range(-3, 2)
```
If we now for example want to ensure that this transaction can only ever be valid before a certain deadline, say at time `4`, we can check this as follows:
```python
time_until_deadline = make_to(4)
contains(time_until_deadline, tx_valid)
```
whereas if the deadline was at time `1`, the `contains` would evaluate to `False`:
```python
time_until_deadline = make_to(1)
contains(time_until_deadline, tx_valid)
```

## Conclusion

Now that we know how to handle time in OpShin, we can write some more interesting contracts! In the next session we will apply our knowledge to a real-world example of a vesting contract.
