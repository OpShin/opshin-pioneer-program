# Lecture 05 — The Minting Policy (`onchain/minting.py`)

> Goal: walk through `src/week09/onchain/minting.py` line by line, mirroring PPP 04‑09‑05 and 04‑09‑06 (we combine the two — the minting policy carries both the mint and the burn/liquidate paths).
> Cues: `[SHOW: …]` switch to a section in the editor, `[POINT: …]` highlight an identifier.

---

## 0. Where we are

Welcome back. In the last video we read the oracle validator end‑to‑end. The oracle gives us a trustworthy on‑chain price of ADA in USD cents. Today we look at the script that *uses* that price: the **minting policy** for our stablecoin. This is the longest file in week 09 — `src/week09/onchain/minting.py` — but it is also the heart of the Dapp. Open it in your editor and follow along.

The minting policy has three redeemers:

- `Mint` — create stablecoins, locking ADA as collateral;
- `Burn` — destroy stablecoins, unlocking the owner's collateral;
- `Liquidate` — destroy stablecoins minted by someone *else*, taking their under‑collateralised position.

We will deal with `Mint` first, then `Burn`, then `Liquidate`.

---

## 1. Parameters and redeemer

`[SHOW: top of minting.py — MintParams, Mint, Burn, Liquidate, MintRedeemer]`

```python
@dataclass()
class MintParams(PlutusData):
    oracle_validator: ValidatorHash
    collateral_validator: ValidatorHash
    collateral_min_percent: int
```

Three compile‑time parameters baked in:

- `oracle_validator` — the script hash of the oracle we trust. This pins our minting policy to *one specific* oracle. If somebody deploys their own oracle, our policy will not look at it.
- `collateral_validator` — the script hash of the collateral validator we pair with.
- `collateral_min_percent` — the minimum over‑collateralisation, e.g. `150` for "150 %". This is also a compile‑time parameter: once deployed, this value is locked.

```python
MintRedeemer = Union[Mint, Burn, Liquidate]
```

The redeemer is just the three‑way tag. Each constructor has its own `CONSTR_ID`, which the Lucid off‑chain uses to build the redeemer.

---

## 2. Helpers, grouped by concern

I split the helpers into three blocks: oracle‑related, collateral‑related, and minting‑related. We will skim each group, and we will refer back to them as we read the validator at the bottom.

### 2.1 Oracle helpers

`[SHOW: script_hash_address, get_oracle_input, rate]`

```python
def script_hash_address(vh: PubKeyHash) -> Address:
    return Address(PubKeyCredential(vh), NoStakingCredential())
```

Tiny helper: turn a script hash into an `Address` with no staking credential. We use it twice — once for the oracle, once for the collateral — to compare addresses on inputs and outputs.

```python
def get_oracle_input(mp: MintParams, context: ScriptContext) -> TxOut:
    outputs = [
        i.resolved
        for i in context.tx_info.inputs
        if i.resolved.address == script_hash_address(mp.oracle_validator)
    ]
    assert len(outputs) == 1, "expected exactly one oracle input"
    return outputs[0]
```

Look through all inputs (spending or reference), keep those whose address matches the oracle's script address, and assert exactly one match. In PPP this was done by filtering reference inputs; in our opshin version we walk the regular inputs, but there is a small `TODO` you can see in the comment — once the prelude is updated, this should also concatenate `context.tx_info.reference_inputs`, so the oracle UTxO can be passed as a reference input instead of a spending input.

```python
def rate(mp: MintParams, context: ScriptContext) -> int:
    return parse_oracle_datum_unsafe(get_oracle_input(mp, context), context.tx_info)
```

`rate` is a one‑liner: find the oracle input, parse its datum as an integer, return it. Compare this to the PPP code that has to thread `Maybe` values explicitly — opshin's `_unsafe` helpers make this a lot shorter.

### 2.2 Collateral helpers

`[SHOW: CollateralOutput, is_collateral_addr, collateral_output, collateral_output_datum, collateral_output_amount]`

```python
@dataclass()
class CollateralOutput(PlutusData):
    datum: CollateralDatum
    value: Value
```

A small bag holding the parsed datum together with the raw value, so we can pass both around without recomputing.

```python
def is_collateral_addr(addr: Address, collateral_validator: ValidatorHash) -> bool:
    staking_cred = addr.staking_credential
    result = False
    if isinstance(staking_cred, NoStakingCredential):
        payment_cred = addr.payment_credential
        if payment_cred.credential_hash == collateral_validator:
            result = True
    return result
```

Note this is stricter than just comparing `Address` objects directly: it also requires `NoStakingCredential`. Why? Because in opshin (and in Plutus) the same payment credential with different staking credentials gives a *different* `Address` value. We want to be sure that the collateral UTxO we create has no staking credential, so we explicitly check that here.

```python
def collateral_output(mp: MintParams, context: ScriptContext) -> CollateralOutput:
    def get_collateral_output(output: TxOut) -> CollateralOutput:
        datum = parse_collateral_datum_unsafe(output, context.tx_info)
        return CollateralOutput(datum, output.value)

    outputs = [
        get_collateral_output(output)
        for output in context.tx_info.outputs
        if is_collateral_addr(output.address, mp.collateral_validator)
    ]
    assert len(outputs) == 1, "expected exactly one collateral output"
    return outputs[0]
```

Same pattern as for the oracle — but on the outputs side. We find the (single) output paying to the collateral address, parse its datum, and package it with its value.

```python
def collateral_output_amount(output: CollateralOutput) -> int:
    return output.value[b""][b""]
```

`b""[b""]` is the standard idiom for "lovelace amount": the empty‑bytes policy id with the empty‑bytes token name is ADA. We need this as an integer because we are about to do arithmetic with it.

There are mirror‑image helpers `collateral_input` and `collateral_input_datum` — same logic, but on the input side. We will use those for `Burn` and `Liquidate`.

### 2.3 Minting helpers

`[SHOW: minted_amount, check_mint_positive, check_burn_negative]`

```python
def minted_amount(context: ScriptContext) -> int:
    minted = context.tx_info.mint
    purpose: Minting = context.purpose
    return minted.get(purpose.policy_id, {b"": 0}).get(STABLECOIN_TOKEN_NAME, 0)
```

We read the transaction's `mint` field. `purpose.policy_id` is our own policy id (we are *the* minting purpose for this script run). Drill into the nested map for our token name — defaulting to zero if it is absent — and we get the amount as a signed integer. Positive means we are minting; negative means we are burning.

`check_mint_positive` and `check_burn_negative` are then trivial sanity checks, but they matter — keep them in mind, we will come back to why `check_burn_negative` is *security‑critical*.

### 2.4 The `max_mint` formula

`[SHOW: max_mint with the docstring]`

```python
def max_mint(mp: MintParams, context: ScriptContext, collateral_amount: int) -> int:
    return (
        collateral_amount // mp.collateral_min_percent * rate(mp, context)
    ) // 1_000_000
```

This is the only piece of real maths in the whole Dapp, so let us read the docstring slowly.

- `collateral_amount` is in **lovelace** (i.e. ADA × 1 000 000).
- `rate` from the oracle is in **USD cents per ADA**.
- `collateral_min_percent` is, well, a percentage (e.g. 150).

The full chain of units is in the comment in the file; the upshot is

```
max_mint [USD]  =  (collateral_amount [L] // CMP) * rate [USD cents per ADA]  //  1_000_000
```

There is a hidden cancellation: the 100 in the percent and the 100 in "cents per dollar" cancel each other out, which is why the formula does not have an explicit `/ 100`. If you ever change one of those constants — say, switch the oracle to USD instead of cents — you will have to update this formula. There is no test that catches that for you, so be careful.

`check_max_mint_out` and `check_liquidation` are both wrappers that compute `max_mint(...)` and compare against the minted amount.

### 2.5 Datum check

`[SHOW: check_datum]`

```python
def check_datum(
    minted_amt: int, context: ScriptContext, collateral_out: CollateralOutput
) -> bool:
    datum = collateral_output_datum(collateral_out)
    purpose: Minting = context.purpose
    own_currency_symbol = purpose.policy_id
    return (
        datum.minting_policy_id == own_currency_symbol
        and datum.stable_coin_amount == minted_amt
        and datum.owner in context.tx_info.signatories
    )
```

Three things to verify on the collateral output's datum:

1. The recorded `minting_policy_id` is **our** policy id. This stops someone using our oracle and our collateral validator to back a *different* stablecoin and trick our burn path.
2. The `stable_coin_amount` matches what we are minting in this transaction. This is the value we will read later, on burn or liquidation, to know how many coins must be destroyed.
3. The `owner` recorded in the datum signs this transaction. Without this, you could lock collateral on behalf of someone else and steal it back later — see PPP burn case.

---

## 3. The validator

`[SHOW: def validator(...): at the bottom]`

```python
def validator(mp: MintParams, r: MintRedeemer, context: ScriptContext):
    minted_amt = minted_amount(context)
    if isinstance(r, Mint):
        ...
    elif isinstance(r, Burn):
        ...
    elif isinstance(r, Liquidate):
        ...
```

A minting policy in opshin takes parameters, a redeemer, and the context — no datum (there is no UTxO at the minting policy). We compute the minted amount once at the top and then dispatch.

### 3.1  `Mint`

```python
if isinstance(r, Mint):
    collateral_out = collateral_output(mp, context)
    assert check_mint_positive(minted_amt), "minted amount must be positive"
    assert check_max_mint_out(
        mp, context, collateral_out, minted_amt
    ), "minted amount exceeds max"
    assert check_datum(
        minted_amt, context, collateral_out
    ), "invalid datum at collateral output"
```

Three checks, exactly as the PPP video lists them:

1. **`check_mint_positive`** — you cannot use the `Mint` redeemer to burn.
2. **`check_max_mint_out`** — the new collateral UTxO holds enough ADA, at the current oracle rate, to back the coins we just minted. (Recall: this is the only place we *read* the oracle.)
3. **`check_datum`** — the collateral output's datum has the right policy id, the right amount, and the owner has signed.

Notice we are not consuming any collateral input here. Minting is a one‑way street: we just *create* a new collateral UTxO and walk away with the coins. That is why we do not need to run the collateral validator during minting.

### 3.2  `Burn`

```python
elif isinstance(r, Burn):
    datum = collateral_input_datum(context, collateral_input(mp, context))
    assert check_burn_amount_matches_col_datum(
        datum, minted_amt
    ), "invalid burning amount"
    assert check_col_owner(datum, context), "owner's signature missing"
    assert check_burn_negative(minted_amt), "Minting instead of burning!"
```

Three checks, again mirroring the PPP video:

1. **`check_burn_amount_matches_col_datum`** — the number of coins we are destroying matches the `stable_coin_amount` recorded in the datum of the collateral input. We negate one side because `minted_amt` is negative when burning.
2. **`check_col_owner`** — the owner from the datum signs.
3. **`check_burn_negative`** — `minted_amt` is actually negative.

Why is the third check there even though the first one already compares signs? PPP calls this out and it is worth repeating: without `check_burn_negative`, an attacker could send a transaction that *creates* a collateral UTxO with a datum like `stable_coin_amount = -N` and a *positive* mint of `N` — burn‑shaped on paper, mint‑shaped in practice. They would walk away with `N` coins, no collateral lost. Locking in the sign of `minted_amt` plugs that hole.

Notice we do not consult the oracle in the burn case. As in lecture 01: when burning your own coins, all the information you need is already encoded in the datum of the collateral UTxO. This is also what lets the burn path keep working after the developer deletes the oracle.

### 3.3  `Liquidate`

```python
elif isinstance(r, Liquidate):
    collateral_inp = collateral_input(mp, context)
    datum = collateral_input_datum(context, collateral_inp)
    assert check_burn_amount_matches_col_datum(
        datum, minted_amt
    ), "invalid liquidating amount"
    assert check_liquidation(
        mp, context, collateral_inp, minted_amt
    ), "liquidation threshold not reached"
    assert check_burn_negative(minted_amt), "Minting instead of burning!"
```

Liquidation reuses two of the burn checks — same amount as in the datum, and `minted_amt` is negative — but replaces the owner signature check with `check_liquidation`:

```python
def check_liquidation(
    mp: MintParams, context: ScriptContext, collateral_inp: TxOut, minted_amt: int
) -> bool:
    return max_mint(mp, context, collateral_input_amount(collateral_inp)) < -minted_amt
```

Read this carefully. `max_mint(collateral, rate)` tells us how many coins the locked ADA *could legitimately back* at the current price. `-minted_amt` is the positive number of coins we are burning, which by check 1 equals what was originally minted against this collateral. So this check says:

> the collateral is no longer enough to back the coins minted against it.

Or, equivalently, the position has dropped under the threshold. As long as my collateral is still good enough — `max_mint(...) >= -minted_amt` — `check_liquidation` returns `False` and the transaction fails. Only when my position is genuinely under‑collateralised can someone liquidate me.

And note we do *not* check the signer here. Anyone who can supply the coins to burn is allowed to liquidate.

---

## 4. How it all comes together in a transaction

`[SHOW: at most a brief diagram or sketch on screen]`

To put this in context, when a user mints:

- the transaction has the **oracle UTxO** as a reference input,
- the **minting policy** as a reference script,
- a freshly created **collateral UTxO** as one of its outputs,
- and the **minted coins** going to the user's wallet.

When they burn (their own coins):

- the **collateral UTxO** is now a *spending* input,
- the **minting policy** runs because we are burning (negative mint),
- the **collateral validator** also runs because we are spending its UTxO — we will see that script in the next video,
- the oracle is *not* present.

When user2 liquidates user1:

- user1's **collateral UTxO** is the spending input,
- both the **minting** and the **collateral** scripts run,
- the **oracle UTxO** is back, as a reference input, because `check_liquidation` needs the current rate.

The collateral validator does the symmetric checks on the spending side, so that this policy and that validator together cover both the mint and the burn‑or‑liquidate sides without trusting each other. We see that in the next video.

---

## 5. Off‑chain pointer

The Lucid off‑chain code for minting, burning and liquidating is the same Next.js component shown in **PPP 04‑09‑05** and **04‑09‑06**. The transactions are structurally identical to what we just described; we are not re‑recording that part. Watch those two PPP videos for the `mintStableCoin` and `burnOrLiquidate` functions — they work as‑is against our opshin‑compiled scripts.

In the next video we'll look at the **collateral validator** (`collateral.py`) and the **NFT minting policy** (`nft.py`) — the two smaller scripts that round out the on‑chain side.
