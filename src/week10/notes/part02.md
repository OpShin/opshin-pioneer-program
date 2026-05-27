<!-- [NOTES TO PRESENTER]
This is the side-by-side: walk `lecture/Vesting.hs` next to
`src/week03/lecture/vesting.py` in the editor. Don't dwell on Haskell
syntax — students aren't expected to write any. Instead emphasise:
the on-chain *logic* is the same, only the surface language differs.
-->

# The Vesting Validator, in PlutusTx

We already wrote the vesting validator in OpShin in week 3
([`src/week03/lecture/vesting.py`](../../week03/lecture/vesting.py)).
Here is the same contract in PlutusTx — verbatim from the original
Plutus Pioneer Program — at [`lecture/Vesting.hs`](../lecture/Vesting.hs)
(canonical copy: `plutus-pioneer-program/code/Week03/lecture/Vesting.hs`).

Open both files side by side in your editor and follow along.

## The datum

**OpShin** (`vesting.py`):

```python
@dataclass()
class VestingParams(PlutusData):
    CONSTR_ID = 0
    beneficiary: PubKeyHash
    deadline: POSIXTime
```

**PlutusTx** (`Vesting.hs`):

```haskell
data VestingDatum = VestingDatum
    { beneficiary :: PubKeyHash
    , deadline    :: POSIXTime
    }

unstableMakeIsData ''VestingDatum
```

Same two fields. The Haskell version needs `unstableMakeIsData` — a
Template Haskell splice that **derives the `IsData` instance** so the
type can be serialised to/from Plutus Core `Data`. In OpShin the
serialisation is implicit: any `PlutusData`-derived dataclass gets it
for free.

(`unstable` here just means "constructor-order-sensitive" — if you
reorder the fields you change the on-chain encoding. There is a stable
variant, `makeIsDataIndexed`, used when on-chain compatibility matters.)

## The validator

**OpShin**:

```python
def validator(datum: VestingParams, redeemer: None, context: ScriptContext) -> None:
    assert signed_by_beneficiary(datum, context), "beneficiary's signature missing"
    assert deadline_reached(datum, context), "deadline not reached"
```

**PlutusTx**:

```haskell
{-# INLINABLE mkVestingValidator #-}
mkVestingValidator :: VestingDatum -> () -> ScriptContext -> Bool
mkVestingValidator dat () ctx =
    traceIfFalse "beneficiary's signature missing" signedByBeneficiary &&
    traceIfFalse "deadline not reached" deadlineReached
  where
    info = scriptContextTxInfo ctx
    signedByBeneficiary = txSignedBy info $ beneficiary dat
    deadlineReached     = contains (from $ deadline dat) $ txInfoValidRange info
```

The on-chain logic is identical:

* **Signed by beneficiary** — both versions check that
  `beneficiary` is in the transaction signatories
  (`txSignedBy` / `params.beneficiary in context.tx_info.signatories`).
* **Deadline reached** — both versions construct the interval
  `[deadline, +∞)` and check that the transaction's validity range
  is contained in it (`contains (from deadline) txInfoValidRange` /
  `contains(make_from(deadline), valid_range)`).

The differences are all surface-level:

| Concern               | PlutusTx                                  | OpShin                       |
|-----------------------|-------------------------------------------|------------------------------|
| failure on bad input  | `traceIfFalse "..." cond &&` returns `False` | `assert cond, "..."` throws |
| return type           | `Bool`                                    | `None` (errors are exceptions) |
| field access          | `beneficiary dat` (record selector fn)    | `params.beneficiary`         |
| INLINABLE pragma      | required for the GHC plugin               | not applicable               |

## The wrapper and compilation

PlutusTx has two extra steps you do not see in OpShin:

```haskell
{-# INLINABLE  mkWrappedVestingValidator #-}
mkWrappedVestingValidator :: BuiltinData -> BuiltinData -> BuiltinData -> ()
mkWrappedVestingValidator = wrapValidator mkVestingValidator

validator :: Validator
validator = mkValidatorScript $$(compile [|| mkWrappedVestingValidator ||])
```

* `wrapValidator` adapts the *typed* `mkVestingValidator` to the
  *untyped* `BuiltinData -> BuiltinData -> BuiltinData -> ()` signature
  Cardano actually invokes. On-chain, the ledger has no idea what a
  `VestingDatum` is — it just hands the script three `BuiltinData`
  blobs. The wrapper decodes them.
* `$$(compile [|| ... ||])` is the **Template Haskell splice** that
  hands the wrapped validator to the GHC PlutusTx plugin. The plugin
  emits UPLC at GHC compile time and the splice replaces itself with
  the compiled program.

OpShin collapses both steps: `opshin build` walks the Python AST and
emits UPLC directly, and the validator signature uses your typed
classes — the equivalent of `wrapValidator` is built into the
generated code.

## Compiling and using the script

In the dev container (which already has GHC, cabal, and the
plutus-pioneer-program project), build the validator with:

```bash
src/week10/scripts/build.sh
```

The script invokes `cabal repl week03` against the upstream project,
runs `Vesting.saveVal`, and copies the resulting `vesting.plutus` into
`src/week10/assets/`. That `.plutus` file is the same envelope format
opshin produces — you can hash it, derive an address from it, and
spend / lock UTxOs against it with `cardano-cli` or pycardano exactly
as you would for an opshin-built script.

Comparing the two `vesting.plutus` envelopes is a useful exercise: the
CBOR-encoded UPLC inside them is different (different compilers
produce different code), but both validators accept the *same* set of
transactions.
