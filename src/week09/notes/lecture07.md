# Lecture 07 — Wrap‑up: deployment, off‑chain & testing

> Goal: tie up loose ends. We have read all four validators; this short video closes the on‑chain story and points to where to look for everything we deliberately did *not* cover.
> Note: in PPP this slot is the pycardano‑style end‑to‑end test walkthrough (PPP 04‑09‑07). We are not re‑shooting that — we briefly tell viewers what testing in our opshin port looks like, and point them to PPP for the long version. If at some point we add a pycardano test suite, this video should be re‑recorded as a proper walkthrough.

---

## 0. Where we landed

We are done reading the on‑chain code. Let us briefly look back at the shape of the project, talk about deployment, off‑chain, and tests, and set up the homework video.

`[SHOW: project tree once more — src/week09/{onchain, offchain, assets, tests}]`

Three lecture videos covered the substance:

- Lecture 03 — `oracle.py`
- Lecture 05 — `minting.py`
- Lecture 06 — `collateral.py` and `nft.py`

Plus lecture 01 which gave the big picture. That is the whole on‑chain side. Anything else worth mentioning fits into this short wrap‑up.

---

## 1. Deploying the reference scripts

`[SHOW: assets/ folder, then optionally open the offchain frontend deploy component]`

We have not given deployment its own video, because in opshin the *story* is the same as in PPP — the only difference is that we compile with `opshin build …` instead of `cabal run`. PPP 04‑09‑04 walks through the off‑chain deploy transaction in detail; everything it says applies here unchanged. The brief reminder:

1. The developer mints the **oracle NFT** (running `nft.py`'s minting policy once against a specific UTxO).
2. The developer deploys the **oracle** UTxO at the oracle script address, with the NFT in its value and the initial rate as inline datum.
3. The developer deploys the **collateral validator** and the **minting policy** as **reference scripts**, attached to UTxOs at the developer's own wallet (in PPP these go to an "always‑false" address; we keep them in the wallet so we can move them while iterating).

Once those three transactions are done, users can mint, burn and liquidate.

If you want to compile the validators from scratch, the `assets/` folder is what `opshin build …` writes into. There is one subfolder per validator — `assets/oracle/`, `assets/minting/`, `assets/collateral/`, `assets/nft/` — each holding the CBOR bytecode and a script address. The frontend reads these directly.

---

## 2. Off‑chain — same code, same Lucid

`[SHOW: offchain/frontend/src/components/, scroll past Oracle / MintNftButton / StableCoin]`

A reminder of something I have said in every video: **our off‑chain code is the very same Next.js + Lucid frontend** that PPP uses in week 9. The on‑chain bytecode produced by opshin is consumed by Lucid in exactly the same way as Plutus bytecode — both end up as CBOR, both are parameter‑applied with `applyParamsToScript`, both run inside Cardano's PlutusV2 interpreter.

What that means in practice:

- the **transaction shapes** (which inputs are reference inputs, which scripts are reference scripts, which redeemers are used) are 1:1 with PPP;
- the **datum and redeemer encodings** match, because we kept the same `dataclass` field orders and pinned the `CONSTR_ID`s of our redeemers;
- the **PPP off‑chain videos** — 04‑09‑02, 03 (from minute 16), 04, 05 (from minute 11), 06 (from minute 8) — are the canonical reference for the front‑end side and we do not duplicate them.

If you ever want a `pycardano` version of the same transactions, the building blocks are all there and the structure is the same; that is a homework‑adjacent exercise.

---

## 3. Tests

`[SHOW: tests/test_on_chain.py]`

```python
import pytest
from opshin import compiler
from src.week09 import onchain_dir

python_files = [
    "collateral.py",
    "minting.py",
    "nft.py",
    "oracle.py",
]
script_paths = [str(onchain_dir.joinpath(f)) for f in python_files]

@pytest.mark.parametrize("path", script_paths)
def test_lecture_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())
```

What we ship today is a **smoke test** — every validator parses and compiles. That catches typos, missing imports, type errors and other regressions during refactors. Run it with `pytest src/week09/tests/`.

That is intentionally less ambitious than the PPP test suite. PPP 04‑09‑07 walks through a **pycardano end‑to‑end test** that:

- deploys the oracle, then updates it;
- locks collateral and mints stablecoins from three users;
- updates the oracle's rate downwards;
- attempts to liquidate two of the three users, asserting that the *correctly* collateralised one cannot be liquidated and the *under*-collateralised one can.

Watch that video for a great mental model of what a thorough test of this Dapp looks like. Translating it to `pycardano` against our opshin scripts is a straight forward port — the script CBOR is interchangeable. Doing that properly is one of the natural homework extensions; if you want to do it for credit, mention it in your homework write‑up.

---

## 4. Anything else?

A few small things that did not get their own video but are worth saying once:

- **`STABLECOIN_TOKEN_NAME = b"USDP"` is hard‑coded** in `common.py`. If you want to mint a *differently named* stablecoin under the same Dapp, change it there and recompile. Both `minting.py` and `collateral.py` pick it up automatically.
- **Reference inputs are a Vasil feature.** The Dapp depends on them — without reference inputs we would need a third redeemer on the oracle ("Use") and a much more expensive transaction every time we mint or liquidate. The opshin `# TODO` comments in `minting.py` are about extending `get_oracle_input` and `collateral_input` to also look at `context.tx_info.reference_inputs`. Once that landed in the prelude, please drop those comments and switch the off‑chain to truly use reference inputs for the oracle.
- **The collateral validator is *not* parameterised.** It is the same script for every stablecoin you may deploy on top of this Dapp — that is why the frontend hard‑codes a single collateral script and the minting policy carries the link via `MintParams.collateral_validator` (the *hash*, which *is* fixed once compiled).

That is it. Up next: homework.
