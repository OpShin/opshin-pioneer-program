# Values

In this lecture, we delve into the `Value` type in OpShin, defined in [opshin.ledger.api_v2](https://github.com/OpShin/opshin/blob/6aa79592ef59718feabd147ef3379b4b6b9c366f/opshin/ledger/api_v2.py#L181).

<!-- [NOTES TO PRESENTER]
Open the link above and explain definition of `Value`.
-->
A key takeaway is that a native token or coin on Cardano is identified by a combination of a policy ID and a token name. The `Value` type itself is a wrapper around a map from `PolicyId` to a map from `TokenName` to `int`.

## Understanding Policy IDs and Token Names

- Both policy IDs token names are type wrappers around byte strings. 
- The `Token` class (show it [here](https://github.com/OpShin/opshin/blob/6aa79592ef59718feabd147ef3379b4b6b9c366f/opshin/prelude.py#L17)), which defines a native token, consists of a policy ID and a token name. Ada, as a special case, is represented by a specific asset class where both the policy ID and token name are the empty byte string.

## Hands-On with `Value`

Next, we'll see some hands-on examples of how to work with values in OpShin. For this, we'll use a couple of utility functions defined in `lecture/value_utils.py`. We will have a look at how those functions are implemented afterwards. Let's first open a Python shell, import the value utils and also the OpShin prelude.

```python
from src.week05.lecture import token_value, amount_of_token_in_value, add_value, subtract_value
from opshin.prelude import *
```

### Constructing and Analyzing Values

We go throught the following examples in the Python shell:
1. Define a token and construct a value with it.
```python
t1 = Token(b"p1", b"t1")
v1 = token_value(t1, 7)
```
2. Inspect using `amount_of_token_in_value`.
```python
amount_of_token_in_value(t1, v1)
```

### Combining and Subtracting Values

Here are some examples:
1. Define a second token and value.
```python
t2 = Token(b"p2", b"t2")
v2 = token_value(t2, 42)
```
2. Combine the two values and inspect the result.
```python
v3 = add_value(v1, v2)
v3
```
3. Another addition.
```python
v4 = add_value(v1, v3)
amount_of_token_in_value(t1, v4)
```
4. Similarly, we can subtract values.
```python
v5 = subtract_value(v4, v2)
amount_of_token_in_value(t2, v5)
```

### Combining and Subtracting Values

A look at the utility functions in `lecture/value_utils.py` reveals how these operations are implemented.
<!-- [NOTES TO PRESENTER]
Go through the code and explain a bit.
-->

## Policy ID Significance

- One important thing to note about the policy ID is that it is actually a hash of a minting policy. A transaction that aims to mint or burn native tokens must include the script, i.e. minting policy, corresponding to each native token's policy ID. This script, hashed to generate the policy ID, dictates whether the transaction is authorized to mint or burn the tokens in question.
- Ada fits into this schema, with its policy ID being the empty byte string, indicating that no script exists that would allow for Ada to be minted or burnt outside of its initial allocation and monetary expansion processes.

We hope that today's exploration of the `Value` type and its components provides you with a fundamental understanding of how tokens, including Ada and native tokens, are represented and manipulated within the Cardano ecosystem and through OpShin scripts. Next, we'll see how to define our own minting policies and how to actually mint native tokens.