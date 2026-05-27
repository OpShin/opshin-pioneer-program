# Lecture 01 — Stablecoin Dapp Overview

> Goal of this video: explain the Dapp at a conceptual level — exactly as in PPP 04‑09‑01 — but in our own words, using equivalent diagrams. We do *not* touch code yet; that comes from Lecture 03 onward.
>
> While speaking, switch to the matching slides/diagrams from the PPP video (or recreate simple boxes-and-arrows on screen). Suggested cues marked `[DIAGRAM: …]`.

---

## 0. Intro

Welcome to week nine of the Opshin Pioneer Program. This is our final project — we are going to put together everything we have learnt and build our very own algorithmic stablecoin.

We will build:

- the on‑chain code: two validators and two minting policies, written in **opshin**;
- the off‑chain code: a fully functional Next.js web frontend that lets users mint, burn and liquidate stablecoins.

The Dapp we are building is conceptually **identical** to the one Plutus Pioneers build in week nine of the PPP. Same logic, same diagrams, same UI. Only the on‑chain language changes — Plutus → opshin. That makes this a great opportunity to compare the two side by side.

In this first video we will only talk about *how* the stablecoin works. We will leave the code for the following videos.

---

## 1. What kind of stablecoin are we building?

There are many ways to keep a stablecoin pegged to a fiat currency. We are going to build an **over‑collateralized, algorithmic stablecoin** that maintains its peg through a **liquidation mechanism**. It sounds complicated, but it is actually pretty simple.

The idea in a single sentence: anyone who wants to mint stablecoins has to lock more ADA than the coins are worth. If the value of the locked ADA ever drops too close to the value of the minted coins, anyone else is allowed to step in, burn the coins and take the collateral — at a profit.

Three on‑chain pieces will do this for us:

- a **collateral** validator — the script address where users lock their ADA;
- a **minting** policy — the policy that lets users mint and burn stablecoins;
- an **oracle** validator — a UTxO holding the current ADA/USD rate, controlled by the Dapp developer.

`[DIAGRAM: three boxes — Oracle, Collateral, Minting — with an "NFT" badge on Oracle]`

The collateral is paid in ADA, so without anything else we would just be tracking the ADA price. To peg to **US dollars** instead, we use the oracle: an on‑chain UTxO whose datum is the current price of ADA in USD cents, kept up to date by the developer.

---

## 2. Deploying the oracle

Let us walk through the transactions, starting with the oracle.

The developer first **mints an NFT**. This is the same NFT minting policy you have already seen — it consumes a specific UTxO so it can only ever run once, guaranteeing the token is unique.

`[DIAGRAM: tx-mint-NFT → wallet UTxO with NFT]`

Then the developer **deploys the oracle**: a transaction that sends a UTxO to the oracle script address. That UTxO carries

- the **NFT** in its value, and
- the **current ADA price** (in USD cents) as its inline datum.

`[DIAGRAM: wallet UTxO + NFT → Oracle script UTxO with datum=100]`

Why do we need an NFT? Because anyone can pay to any script address. The NFT is what lets us *identify* the genuine oracle UTxO among any impostors. Whenever another validator wants to consume the oracle's rate, it will look for the UTxO holding *this specific* NFT.

---

## 3. Updating and deleting the oracle

The oracle's value goes stale the moment we deploy it, so we need a way to refresh it.

`[DIAGRAM: Oracle UTxO (rate=100) → tx-update (signed by developer) → Oracle UTxO (rate=90), NFT carried through]`

In a real Dapp, a backend service would do this every block from a trusted price feed. In our example we update the rate **manually** from the UI, so we can reproduce edge cases like liquidation on demand.

To update, the developer simply consumes the old oracle UTxO and creates a new one at the same address, with the same NFT, but a new rate in the datum. The oracle validator checks that:

1. the input contains the NFT,
2. the output contains the NFT,
3. the transaction is signed by the operator (the developer), and
4. the output datum is well formed.

There is also a **delete** path: the developer can shut the Dapp down by burning… well, by spending the NFT and withdrawing it. Once the oracle is gone, no one can mint any more, and no one can liquidate; users can still burn their own coins and reclaim their collateral.

---

## 4. Deploying the other scripts

`[DIAGRAM: tx-deploy → two UTxOs containing collateral.py and minting.py as reference scripts]`

The collateral validator and the minting policy do not need to be re‑attached to every transaction; they are deployed once as **reference scripts**. In the PPP example they are attached to UTxOs at an *always‑false* address, so they live forever. In our example we send them to the developer's own wallet — convenient for testing because we can move them around or update them while iterating.

Either way, once deployed, users can refer to them by UTxO instead of having to embed the script bytes every time.

---

## 5. Minting stablecoins — the user side

Now we switch hats and become a user.

To mint, we need three ingredients in a single transaction:

- some **ADA** to lock as collateral,
- the **oracle UTxO** as a reference input (so the minting policy can read the current price), and
- the **minting policy** as a reference script.

`[DIAGRAM: user wallet ADA + Oracle (ref) + Minting (ref) → tx-mint → user wallet stablecoins + Collateral UTxO]`

The transaction produces two outputs:

- a UTxO **at the user's wallet** containing freshly‑minted stablecoins, and
- a UTxO **at the collateral validator's address** holding the locked ADA. Its inline datum stores who locked it (`owner`), which `minting_policy_id` produced the coins, and `stable_coin_amount` minted against it.

Let us run a concrete example. Suppose the oracle says **1 ADA = 1 USD**, and the developer chose a **150% minimum collateral**.

- The user wants to mint **100 USDP** (worth $100).
- They must therefore lock at least **150 ADA** (worth $150) as collateral.
- The collateral datum will record: `owner = user1`, `stable_coin_amount = 100`.

`[DIAGRAM: 100 USDP in wallet, 150 ADA locked, datum {owner=user1, amount=100}]`

The check the minting policy enforces is exactly:
**collateral value ≥ 150% × minted value, at the current oracle rate.**

We store the minted amount inside the datum because we will need it later, when burning or liquidating.

---

## 6. Burning your own coins

Sometime later, the same user wants to close their position. They want their ADA back.

`[DIAGRAM: user wallet 100 USDP + Collateral UTxO (input) + Collateral (ref script) + Minting (ref script) → tx-burn → user wallet (150 ADA, -100 USDP)]`

This time we run **two** validators in the same transaction:

- the **collateral** validator (because we are spending the collateral UTxO), and
- the **minting** policy (because we are burning coins).

We do **not** need the oracle here. Why? The collateral is already locked, and the datum already tells us how many coins were minted against it. There is nothing to look up.

The two scripts together check:

- the burn amount equals the `stable_coin_amount` recorded in the datum,
- the owner from the datum has signed the transaction.

The user gets their 150 ADA back, the 100 USDP are burned, and the collateral UTxO is gone.

---

## 7. Liquidating someone else's position

This is the most interesting case, and it is what keeps the peg.

`[DIAGRAM: user2 wallet stablecoins + user1's Collateral UTxO + Oracle (ref) + Collateral & Minting (ref scripts) → tx-liquidate → user2 gets the ADA]`

Suppose user 1 minted 100 USDP against 150 ADA — exactly at the 150% threshold. Then the ADA price drops, so 150 ADA is now worth, say, only $130. User 1 is **under‑collateralized**: there is less than 150% backing the 100 USDP.

Now user 2 can step in. User 2 must:

- burn **the same 100 USDP** that user 1 minted, and
- consume user 1's collateral UTxO.

In return, user 2 receives **all of user 1's locked ADA** — which, even at the new price, is still worth more than the 100 USDP they had to burn. That difference is user 2's profit. User 1 loses everything that was locked.

The trick is the check inside the minting policy: liquidation is only allowed if `max_mint(collateral, rate) < |minted|` — i.e. the position is actually below the threshold. As long as your collateral stays above 150%, no one can touch you.

This is exactly the mechanism that keeps the peg: if your position drifts, you have a strong incentive to **top up your collateral** or **burn coins** before someone else liquidates you. And on the other side, anyone with spare coins has a strong incentive to **hunt under‑collateralized positions** for profit. Both forces push the system back to a healthy state.

---

## 8. Shutting it down

Finally, what if the developer wants to call it quits?

`[DIAGRAM: Oracle UTxO + nft → tx-delete (signed by developer) → wallet (nft back)]`

The developer just spends the oracle UTxO with the `Delete` redeemer. From that moment on, no one can mint (the minting policy can't find the oracle) and no one can liquidate (same reason). But the **burn** path still works — it does not need the oracle. So every user can still reclaim their collateral by burning their own coins.

---

## 9. Recap and what comes next

We just covered the whole Dapp at a high level:

- An **NFT‑tagged Oracle** UTxO carries the ADA/USD rate.
- A **Collateral** validator locks ADA against minted stablecoins.
- A **Minting** policy enforces over‑collateralisation when minting, and the burn / liquidate rules when destroying coins.
- The **incentive to liquidate** keeps the peg.

A quick note about the next video: in the PPP series, lecture 04‑09‑02 walks through the Dapp's web UI — connecting a wallet, minting, burning, liquidating. **Our frontend is the same Next.js + Lucid frontend** that the PPP uses, so we are not re‑shooting that video. If you want a UI walkthrough, please watch **PPP 04‑09‑02** directly. From the *next* video onwards we will look at the on‑chain code, written in opshin instead of Plutus, and you will see it lines up very nicely with what we have just described.

See you in lecture 03 — where we go through `onchain/oracle.py` line by line.
