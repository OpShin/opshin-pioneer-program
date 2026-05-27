# Lecture 06 — Collateral & NFT (`onchain/collateral.py`, `onchain/nft.py`)

> Goal: finish the on‑chain story by walking through the two remaining scripts — the **collateral** validator and the **NFT** minting policy that the oracle relies on. This is content not given its own PPP video; PPP folds these into lectures 05 and 06.
> Cues: `[SHOW: …]`, `[POINT: …]` as before.

---

## 0. Where we are

In the previous video we read `minting.py` and saw how the three redeemers — `Mint`, `Burn`, `Liquidate` — work *from the minting policy's point of view*. But two things were still on the side. First, **the collateral validator**: whenever the minting policy burns or liquidates, the collateral UTxO is being **spent**, so the collateral validator runs too. We never read that script. Second, **the NFT minting policy** for the oracle: lecture 03 talked about "the NFT that pins the oracle's identity"; today we look at the script that mints it.

Both files are short. Let us start with collateral.

---

## 1. `onchain/collateral.py`

`[SHOW: open collateral.py top to bottom]`

### 1.1 Imports, redeemer, helpers

```python
from opshin.prelude import *
from src.week09.onchain.common import *

@dataclass()
class Redeem(PlutusData):
    CONSTR_ID = 1048

@dataclass()
class Liquidate(PlutusData):
    CONSTR_ID = 1049

CollateralRedeemer = Union[Redeem, Liquidate]
```

Two redeemers, exactly mirroring two of the three minting cases:

- `Redeem` ↔ `Burn` on the minting side — the collateral owner takes their ADA back by burning the coins.
- `Liquidate` ↔ `Liquidate` on the minting side — someone else takes the ADA by burning the corresponding coins.

There is no `Mint`‑equivalent here, because when we *mint* we are only *creating* a collateral UTxO — the collateral validator does not run.

```python
def check_signed_by_owner(datum: CollateralDatum, context: ScriptContext) -> bool:
    return datum.owner in context.tx_info.signatories
```

Standard owner‑signature pattern, this time pulling `owner` out of the collateral datum.

```python
def minted_amount(datum: CollateralDatum, context: ScriptContext) -> int:
    minted = context.tx_info.mint
    return minted.get(datum.minting_policy_id, {b"": 0}).get(STABLECOIN_TOKEN_NAME, 0)

def check_stablecoin_amount(datum: CollateralDatum, context: ScriptContext) -> bool:
    return -datum.stable_coin_amount == minted_amount(datum, context)
```

This is the most important helper in the file. Read the equality carefully — there is a sign flip:

- `datum.stable_coin_amount` is **positive**: it is the number of coins originally minted against this collateral.
- `minted_amount(...)` is **negative** when burning: the transaction's `mint` field reports a *change*, and burning is a negative change.
- So `-datum.stable_coin_amount == minted_amount(...)` says: "the burned amount in this transaction equals the positive amount recorded in the datum."

Note also that we look up the *minting policy id from the datum*, not the collateral validator's own context. This is what binds a collateral UTxO to a specific stablecoin policy id — the one recorded at mint time inside `check_datum` in `minting.py`. The collateral validator stays generic; it works for any stablecoin whose policy is recorded in the datum.

### 1.2 The validator

```python
def validator(datum: CollateralDatum, r: CollateralRedeemer, context: ScriptContext):
    if isinstance(r, Redeem):
        assert check_signed_by_owner(
            datum, context
        ), "collateral owner's signature missing"
        assert check_stablecoin_amount(
            datum, context
        ), "burned stablecoin amount mismatch"
    elif isinstance(r, Liquidate):
        assert check_stablecoin_amount(
            datum, context
        ), "burned stablecoin amount mismatch"
```

Two cases, both tiny:

- **`Redeem`**: the owner from the datum has signed, *and* the coins burned equal the coins originally minted against this UTxO. Two checks.
- **`Liquidate`**: just one check — the coins burned equal the coins originally minted. We do **not** check the signer, because the whole point of liquidation is that *someone else* is doing this. The check that the position is actually under‑collateralised is enforced on the *minting* side, by `check_liquidation`. We do not need to duplicate it here.

It is worth a moment to convince yourself this is safe. Why is the collateral validator OK with someone walking away with the locked ADA in the liquidate case, without checking the rate? Because the same transaction also runs the minting policy, and the minting policy *will* check the rate via `check_liquidation`. The two scripts cooperate.

### 1.3 So why even have a collateral validator?

If the minting policy already enforces all the interesting rules, why does the collateral validator exist at all? Because the collateral *UTxO* must be controlled by *some* script. If we used a public‑key address, anyone could spend the UTxO without burning anything. The collateral validator is the one that says: "you cannot take this ADA out unless coins are also being burned in the same transaction."

In particular, **the burn path needs the collateral validator** in addition to the minting policy. Without `check_stablecoin_amount` *here*, you could burn fewer coins than the datum says — only the minting side would notice (or wouldn't, depending on which redeemer was used). The two checks together make sure the books always balance.

---

## 2. `onchain/nft.py`

`[SHOW: open nft.py]`

This is the NFT used to identify the oracle. We already saw a similar one in week 06, but let us read this one because it ties the whole Dapp together.

### 2.1 Parameters

```python
def validator(oref: TxOutRef, tn: TokenName, _: None, context: ScriptContext):
    ...
```

Three compile‑time inputs:

- `oref: TxOutRef` — a specific UTxO reference. The policy is parameterised on it, so once we compile we get a policy hash that is bound to *this* UTxO. Nobody else can ever produce the same policy.
- `tn: TokenName` — the name of the NFT. We want each developer's oracle NFT to be readable on chain explorers (something like `"USDPOracle"`); making this a parameter lets the off‑chain choose it.
- `_: None` — the redeemer is unused.

### 2.2 The three checks

```python
def assert_minting_purpose(context: ScriptContext) -> None:
    purpose = context.purpose
    if isinstance(purpose, Minting):
        is_minting = True
    else:
        is_minting = False
    assert is_minting, "not minting purpose"
```

Sanity check: this script must be invoked as a minting policy, not as a spending validator. This protects against future composition mistakes.

```python
def has_utxo(oref: TxOutRef, context: ScriptContext) -> bool:
    return any([oref == i.out_ref for i in context.tx_info.inputs])
```

The transaction must consume the **specific** UTxO we parameterised on. That UTxO can only be spent once, so the policy can only run once. **This is what makes the token an NFT.**

```python
def check_minted_amount(tn: TokenName, context: ScriptContext) -> bool:
    mint_value = context.tx_info.mint
    valid = False
    count = 0
    for policy_id, v in mint_value.items():
        if len(v.keys()) == 1:
            for token_name, amount in v.items():
                valid = token_name == tn and amount == 1
                if amount != 0:
                    count += 1
    return valid and count == 1
```

This one is a little fiddly. We want to assert that

- exactly **one token** is minted under our policy id,
- with the right **token name** (`tn`), and
- in amount **1**.

The loop walks every policy id in the transaction's `mint` field. For each policy, it inspects how many distinct token names appear. The line `if len(v.keys()) == 1` ensures we only flip `valid` when looking at a policy that mints a single token name — including, importantly, our own. The `count` tally then ensures only one policy in the whole transaction is doing any non‑zero minting.

There is a subtle property here: this check rejects transactions that *also* mint something else under a *different* policy. Mostly that is fine — minting the NFT is a one‑off bootstrap step done in isolation. But if you ever want to bundle the NFT mint with another mint in the same transaction, you would have to relax this.

### 2.3 The validator body

```python
def validator(oref: TxOutRef, tn: TokenName, _: None, context: ScriptContext):
    assert_minting_purpose(context)
    assert has_utxo(oref, context), "UTxO not consumed"
    assert check_minted_amount(tn, context), "wrong amount minted"
```

Three asserts. That is the whole policy. Take a moment to admire how compact it is.

---

## 3. Recap

We now have all four on‑chain pieces in our heads:

| Script         | Purpose                              | Key checks                                                        |
|----------------|--------------------------------------|-------------------------------------------------------------------|
| `nft.py`       | Mint the unique oracle NFT           | minting purpose; specific UTxO is consumed; exactly one token     |
| `oracle.py`    | Hold / update / delete the rate      | NFT in and out; operator signs; valid datum                       |
| `minting.py`   | Mint, burn or liquidate stablecoins  | min‑collateral on mint; amount matches datum on burn/liquidate; under‑collateralised on liquidate |
| `collateral.py`| Guard the locked ADA                 | amount matches datum; owner signs on redeem                       |

Each script does as little as possible, and the system is safe because the minting policy and the collateral validator together cover every spending move.

In the next, final video we wrap up with a few words about testing — we already have `tests/test_on_chain.py` that compiles every script — and then move on to the homework.
