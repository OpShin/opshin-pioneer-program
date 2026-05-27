# Lecture 03 — The Oracle (`onchain/oracle.py`)

> Goal: walk through `src/week09/onchain/oracle.py` line by line, mirroring PPP 04‑09‑03 but with the opshin code on screen.
> While speaking, scroll through the file in the order indicated. Cues: `[SHOW: …]` switch to a section, `[POINT: …]` highlight a specific identifier.

---

## 0. Where are we?

Welcome back. In the previous video we walked through the Dapp at a conceptual level. From now on we will read the on‑chain code together. Today's video is about the **oracle** — the script that holds the current ADA / USD rate.

`[SHOW: project tree, then open src/week09/onchain/oracle.py at the top]`

Quick reminder about the project layout. Under `src/week09` we have:

- `onchain/` — our validators in opshin (this is where we are);
- `offchain/` — the Next.js / Lucid frontend (same as PPP);
- `assets/` — the compiled validators, one folder per script;
- `tests/` — pytest tests that at minimum compile every validator.

In `onchain/` you can already see the four files we are going to touch over the next few lectures: `oracle.py`, `minting.py`, `collateral.py`, `nft.py`, plus a small `common.py` shared across them. Today we open **`oracle.py`**.

---

## 1. Imports and shared helpers

`[SHOW: line 1 — from src.week09.onchain.common import *]`

Everything we need from opshin's prelude (`PlutusData`, `ScriptContext`, `TxOut`, `Address`, …) is re‑exported through `common.py`. Let me quickly switch to that file so you see what is being imported.

`[SHOW: onchain/common.py]`

Two things to note in `common.py`:

- We hard‑code the stablecoin token name once, `STABLECOIN_TOKEN_NAME = b"USDP"`. Both the minting policy and the collateral validator will use it, so we factor it out here to keep them in sync. You could pass it as a parameter instead, but then both scripts must receive exactly the same value, which is more error‑prone.
- We define `CollateralDatum` and two helpers — `parse_collateral_datum_unsafe` and `parse_oracle_datum_unsafe` — that resolve a `TxOut`'s datum into a typed value. The `_unsafe` suffix is the opshin convention: these helpers will *crash* the script if the datum is missing or has the wrong shape, which is exactly what we want — failure here means the transaction is invalid anyway.

`[POINT: parse_oracle_datum_unsafe returns int]`

Notice the oracle datum is literally an `int` — the rate, in USD cents. No wrapper struct. Simpler is better.

Back to `oracle.py`.

---

## 2. The parameters: `AssetClass` and `OracleParams`

`[SHOW: oracle.py — AssetClass and OracleParams]`

```python
@dataclass()
class AssetClass(PlutusData):
    policy_id: bytes
    token_name: bytes

@dataclass()
class OracleParams(PlutusData):
    nft: AssetClass
    operator: PubKeyHash
```

The oracle validator takes two parameters baked in at compile time:

- the **NFT** that uniquely identifies the oracle UTxO, expressed as an `AssetClass` (policy + token name); and
- the **operator** — the public key hash of the developer running the oracle. Only this key can update or delete it.

Once the script is compiled with these two parameters, the resulting validator hash is unique to this NFT and this operator. Nobody else can produce the same script address.

---

## 3. The redeemer: `Update` vs `Delete`

`[SHOW: Update, Delete, OracleRedeemer]`

```python
@dataclass()
class Update(PlutusData):
    CONSTR_ID = 1046

@dataclass()
class Delete(PlutusData):
    CONSTR_ID = 1047

OracleRedeemer = Union[Update, Delete]
```

Two redeemer constructors. `Update` rewrites the rate, `Delete` shuts the oracle down. The numeric `CONSTR_ID`s pin down the Plutus constructor tag so we don't depend on Python's class ordering — this matters because the off‑chain code in Lucid builds the redeemer by tag.

Note something important: in Vasil and later, there is no longer a separate "Use" redeemer. When another validator just wants to *read* the rate, it pulls the oracle UTxO in as a **reference input**, not as a spending input — so the oracle script doesn't run at all. The only times it runs are when we genuinely want to *update* or *delete* the UTxO.

---

## 4. The validator signature

`[SHOW: validator(...) at the bottom of the file]`

```python
def validator(oracle: OracleParams, _: Rate, r: OracleRedeemer, context: ScriptContext):
    if isinstance(r, Update):
        ...
    elif isinstance(r, Delete):
        ...
```

The function called `validator` is the entry point opshin compiles. Its signature reads:

- `oracle: OracleParams` — the compile‑time parameters we just discussed;
- `_: Rate` — the current datum, which is just an integer. We deliberately ignore it (hence `_`): the oracle validator does not care what the *old* rate was, it only cares that the *new* one is well formed.
- `r: OracleRedeemer` — `Update` or `Delete`;
- `context: ScriptContext` — the usual transaction context.

The body just dispatches on the redeemer. Let us look at each case.

---

## 5. The `Update` case — four checks

`[SHOW: the body of `if isinstance(r, Update):`]`

```python
if isinstance(r, Update):
    own_tx_out = own_output(context)
    assert input_has_token(oracle, context), "token missing from input"
    assert output_has_token(oracle, own_tx_out), "token missing from output"
    assert check_operator_signature(oracle, context), "operator signature missing"
    assert check_output_datum(own_tx_out, context), "invalid output datum"
```

Four asserts. Each maps directly to one of the requirements we drew up in lecture 01. Let me go through them in order.

### 5.1  `input_has_token` — "the NFT must come in"

`[SHOW: own_input, input_has_token]`

```python
def own_input(context: ScriptContext) -> TxOut:
    purpose: Spending = context.purpose
    ref = purpose.tx_out_ref
    outputs = [i.resolved for i in context.tx_info.inputs if ref == i.out_ref]
    assert len(outputs) == 1, "oracle input missing"
    return outputs[0]

def input_has_token(oracle: OracleParams, context: ScriptContext) -> bool:
    tx_out = own_input(context)
    return tx_out.value[oracle.nft.policy_id][oracle.nft.token_name] == 1
```

`own_input` finds the UTxO the script is currently spending. In opshin, `context.purpose` for a spending validator is a `Spending` value carrying the `tx_out_ref` being spent; we filter the inputs by that reference and assert exactly one match.

Then `input_has_token` looks at that input's `value` and reads the amount of the NFT — `value[policy_id][token_name]`. It must be exactly `1`. If somebody tries to update an oracle UTxO that does not actually hold the NFT, we abort.

This is what nails down identity. There can be many UTxOs at the oracle's address — anyone can pay to it — but only the one carrying the NFT is the real oracle.

### 5.2  `output_has_token` — "the NFT must go out"

`[SHOW: get_continuing_outputs, own_output, output_has_token]`

```python
def get_continuing_outputs(context: ScriptContext) -> List[TxOut]:
    inputs = context.tx_info.inputs
    assert len(inputs) == 1, "Can't get any continuing outputs"
    addr = inputs[0].resolved.address
    return [o for o in context.tx_info.outputs if o.address == addr]
```

`get_continuing_outputs` returns the outputs that pay back to the *same script address* we are spending from. We assert there is only one input — this keeps the validator simple and prevents people from batching multiple oracle inputs into one transaction.

`own_output` then takes exactly one such continuing output, and `output_has_token` checks that the NFT is in *its* value as well. So the NFT comes in, and the NFT goes out: the oracle still exists after the update.

### 5.3  `check_operator_signature` — "only the operator may update"

```python
def check_operator_signature(oracle: OracleParams, context: ScriptContext) -> bool:
    return oracle.operator in context.tx_info.signatories
```

The standard pattern: read the operator's `PubKeyHash` from the parameters, check it appears in the transaction's signatories. Nothing more to say.

### 5.4  `check_output_datum` — "the new rate must be a valid integer"

```python
def check_output_datum(own_tx_out: TxOut, context: ScriptContext) -> bool:
    datum: Rate = parse_oracle_datum_unsafe(own_tx_out, context.tx_info)
    return True
```

This is the subtle one. We call our typed parser `parse_oracle_datum_unsafe` on the *output's* datum, asking it to give us back a `Rate`, which is an `int`. If the datum is missing, or is not an integer, the parser will crash — and that crash *is* the rejection. If it succeeds, we already know the new datum is structurally a valid rate, and we return `True`.

We deliberately don't check anything about the value of the rate (whether it went up or down, whether it is positive, etc.). That is a policy decision: the operator is trusted to put in a real number; in a production system you would back that trust up with off‑chain monitoring.

---

## 6. The `Delete` case — one check

`[SHOW: the body of elif isinstance(r, Delete):]`

```python
elif isinstance(r, Delete):
    assert check_operator_signature(oracle, context), "operator signature missing"
```

That is it. To shut the oracle down, the operator simply signs a transaction that spends the oracle UTxO and walks away with the NFT. No continuing output, no datum check.

This is what allows the Dapp to wind down gracefully — minting and liquidation both depend on reading the oracle, so they stop working immediately; but burning your own coins does not need the oracle, so users can still get their collateral back.

---

## 7. Recap

Let us zoom out. The whole oracle validator boils down to one line of off‑chain trust ("the operator chooses the rate") plus four on‑chain invariants for updates:

1. NFT comes in.
2. NFT goes out.
3. Operator signs.
4. New datum parses as an integer.

…and one invariant for deletion: operator signs.

Notice how short this is — about 80 lines, including helpers. The whole point of pushing rate freshness onto an off‑chain operator (as opposed to, say, taking a weighted median of several signed oracles) is to keep this script tiny.

---

## 8. Off‑chain pointer

We are not going to re‑shoot the off‑chain video. The Lucid code that deploys, updates and deletes the oracle is the *same* Next.js component shown in **PPP 04‑09‑03** from roughly minute 16 onwards — the only Plutus‑specific bit is how the parameters are applied to the validator hash, and that mechanism does not change between Plutus and opshin (Lucid just sees a CBOR‑encoded script either way).

In the next video, lecture 05, we move on to the heart of the Dapp: the **minting policy**.
