<!-- [NOTES TO PRESENTER]
This is a brief contrast between OpShin (what we've been using all course) and
PlutusTx (what the original plutus-pioneer-program uses). Goal: students should
walk away knowing what PlutusTx *is*, why it looks the way it does, and where
it sits in the Cardano smart-contract landscape. We do NOT teach Haskell —
just enough to read the Vesting example in [part02.md](part02.md).
-->

# A Brief Introduction to PlutusTx

So far we have written every smart contract in this course in
[OpShin](https://github.com/OpShin/opshin), a Python eDSL. The original
[Plutus Pioneer Program](https://github.com/input-output-hk/plutus-pioneer-program)
uses a different toolchain — **PlutusTx** — embedded in Haskell. The
on-chain semantics (Plutus Core / UPLC) are identical; only the surface
language and tooling differ.

This week we take a short detour to look at PlutusTx itself, using the
same `vesting` example we already wrote in [week 3](../../week03/lecture/vesting.py)
so the comparison is direct.

## What is PlutusTx?

PlutusTx is a **subset of Haskell** that is compiled — by a GHC plugin —
into **Plutus Core**, the low-level UPLC bytecode that runs on Cardano.
Concretely you write Haskell, mark functions as `INLINABLE`, and wrap
them in a Template Haskell quote `[|| ... ||]` so the plugin can pick
them up and emit UPLC instead of native code.

A PlutusTx validator therefore looks roughly like this:

```haskell
{-# INLINABLE mkValidator #-}
mkValidator :: Datum -> Redeemer -> ScriptContext -> Bool
mkValidator d r ctx = ...      -- on-chain logic, just like OpShin's validator

validator :: Validator
validator = mkValidatorScript $$(compile [|| mkWrappedValidator ||])
--                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
--                                Template Haskell splice: the GHC plugin
--                                replaces this with the compiled UPLC.
```

In OpShin the equivalent is just a top-level `def validator(...)` and a
call to `opshin build`. There is no plugin, no Template Haskell, no
`INLINABLE` annotation — opshin compiles the Python AST directly.

## Why does PlutusTx look this way?

A few constraints leak into the surface language:

* **`PlutusTx.Prelude`, not `Prelude`.**  The plugin can only compile a
  subset of Haskell, so you import an alternative prelude with
  Plutus-Core-compatible versions of `Bool`, `($)`, `(&&)`, etc.
  `NoImplicitPrelude` keeps Haskell's normal `Prelude` out of scope on
  the on-chain side.
* **`INLINABLE` everywhere.**  The GHC plugin needs every on-chain
  function's body available so it can inline through to UPLC. Forgetting
  the pragma typically produces an inscrutable `GHC Core to PLC plugin`
  error at compile time.
* **Template Haskell + `$$(compile [|| ... ||])`.**  This is how the
  Haskell expression is *quoted* and handed to the plugin to compile.
  Parameterised validators add `liftCode` / `applyCode` on top — see
  [`ParameterizedVesting.hs`](../../../plutus-pioneer-program/code/Week03/lecture/ParameterizedVesting.hs).
* **A wrapper layer (`wrapValidator`).**  On-chain a validator's actual
  type is `BuiltinData -> BuiltinData -> BuiltinData -> ()`; the wrapper
  decodes those into the typed `Datum`/`Redeemer`/`ScriptContext` your
  logic operates on.

None of those exist in OpShin: types are decoded by the runtime, the
compiler walks the AST directly, and there is no separate "on-chain
prelude".

## Where PlutusTx sits

PlutusTx is the **reference** implementation — Cardano's ledger
specification is written in Haskell and PlutusTx is what the IOG team
maintains as the official path from a high-level language to UPLC.
Everything else — OpShin (Python), Aiken (its own ML-like language),
Plutarch (Haskell eDSL, closer to UPLC), plu-ts (TypeScript) — targets
the same UPLC and is verified against it.

For this lecture we are not switching languages: we are using PlutusTx
as a **point of comparison** to make explicit what OpShin saves us from,
and what the Cardano on-chain semantics actually require.

Move on to [part02.md](part02.md) for the vesting walkthrough.
