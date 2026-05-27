# Lecture 08 — Homework

> Goal: state the homework, mirroring PPP 04‑09‑08, but framed for the opshin codebase. Same two exercises Lars Brünjes gives at the end of PPP, plus a small opshin‑specific bonus.
> This is meant as a short, punchy outro video.

---

## 0. Setup

Before we hand things over to you, let us be honest about the limits of what we just built. The Dapp works, but it has some sharp edges. Recognising them is half the homework.

`[SHOW: minting.py with `max_mint` and `check_liquidation` visible side‑by‑side]`

A few obvious limitations:

- If the price of ADA *rises*, you would like to mint **more** stablecoins against the same locked collateral. Today, the only way to do that is to **burn everything and re‑mint** with a bigger amount — wasteful and slow. A nicer Dapp would let you bump up the `stable_coin_amount` in an *existing* collateral UTxO. This is doable, but it touches both the collateral validator and the minting policy, and it interacts with the burn/liquidate checks. We are **not** asking you to do this one; consider it stretch reading.
- There are **no fees** for the developer. The user that liquidates makes money; the operator who keeps the oracle fresh makes nothing. That is unsustainable.
- The **liquidation reward is "everything"**. The Liquidator takes the entire over‑collateralisation. A user who drifts even 1% below the threshold loses 50% of their collateral. That is wildly unfair and discourages people from minting in the first place.

The two homework exercises target the last two. They are exactly the ones Lars sets in PPP 04‑09‑08, and they are well within reach with what you have learnt over weeks 1–9.

---

## 1. Homework 1 — cap the liquidation reward

> *"Limit the rewards the Liquidator can get to e.g. 2 % of the over‑collateralisation, and send the rest back to the original collateral owner."*

What this looks like on chain:

- The `Liquidate` transaction must now produce **two outputs in addition to the burn** — one to the Liquidator and one back to the original owner.
- The split is `2 %` (a parameter — pick a value, or take it from `MintParams`) to the Liquidator's wallet, and `98 %` of the *excess collateral above the burned coins' value* back to the original owner.
- The position‑below‑threshold check stays the same.

Concretely, in `minting.py` you need to:

1. Compute the **value of the burned coins** in ADA, using the oracle rate and the formula already in `max_mint`.
2. Compute the **excess** = locked collateral − value of burned coins.
3. Assert there is an output paying `(1 − fee) × excess` back to `datum.owner`.

In `collateral.py`, you need to relax — or replace — the `Liquidate` check accordingly, because today the collateral validator implicitly allows the Liquidator to take *all* the ADA. You will probably want a small structural change here.

Tip: keep the cap parameterised. Drop a `liquidation_reward_percent: int` into `MintParams` instead of hard‑coding `2`.

---

## 2. Homework 2 — pay the developer

> *"Charge a small fee (e.g. 0.1 %) on every mint, burn and liquidate that goes to the stablecoin operator."*

What this looks like on chain:

- Add a `fee_per_mille: int` (or similar) to `MintParams`, and a `fee_recipient: PubKeyHash` (probably the same as the oracle's `operator`).
- In every redeemer branch of `minting.py`, assert that an output paying the right amount of ADA to `fee_recipient` exists.

A few things to think about:

- The **size** of the fee scales with what? The minted coin count? The collateral amount? Specifying this clearly is part of the exercise.
- For **liquidate**, who pays — the Liquidator, or out of the collateral being released? Think about incentives.
- This is the kind of change that needs **at least one new unit test** to stop you breaking it later. Adding a pycardano test for the fee transaction is a natural extension.

---

## 3. Bonus (opshin‑specific) — clean up the `TODO`s

A small bonus exercise tailored to our opshin port: in `minting.py` you can see two `TODO` comments asking to also look at `context.tx_info.reference_inputs` when searching for the oracle and the collateral inputs. The reason these still walk the spending inputs is historical — early versions of the prelude did not expose reference inputs uniformly. They are exposed now.

Refactor `get_oracle_input` and `collateral_input` to **also** search reference inputs (using list concatenation), and update the off‑chain code in `offchain/frontend` so that the oracle UTxO is actually passed as a reference input on mint and liquidate, not as a spending input. The Dapp should keep working, but transactions should be a little cheaper.

---

## 4. Where to ship your work

`[SHOW: README of the repo, or wherever you collect homework PRs]`

Open a pull request against the week 09 folder with:

- the modified `onchain/` files;
- a paragraph in your PR description explaining your choice for the reward percentage and the fee rate;
- if you also did the bonus, mention it; ditto if you ported PPP's `pycardano` end‑to‑end test to your changes.

That's a wrap on week 9, and on the Opshin Pioneer Program as a whole. You now have all the ingredients to design and ship an end‑to‑end Cardano Dapp in opshin. Have fun.
