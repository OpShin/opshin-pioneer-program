"""
Homework: a staking validator with two parameters, a `PubKeyHash` and an
`Address`. The validator should work as follows:

  1. The given `PubKeyHash` must sign every transaction involving this script.
  2. The given `Address` must receive at least half of all withdrawn rewards
     (paid in ADA / lovelace).

This is the OpShin equivalent of
`plutus-pioneer-program/code/Week08/homework/Homework.hs`.
"""

from opshin.prelude import *


def total_withdrawn(wdrl: Dict[StakingCredential, int]) -> int:
    total = 0
    for _, amount in wdrl.items():
        total += amount
    return total


def lovelace_paid_to(addr: Address, outputs: List[TxOut]) -> int:
    return sum(
        [o.value.get(b"", {b"": 0}).get(b"", 0) for o in outputs if o.address == addr]
    )


def validator(
    pkh: PubKeyHash,
    addr: Address,
    _r: None,
    context: ScriptContext,
) -> None:
    tx_info = context.tx_info
    assert pkh in tx_info.signatories, "required signature missing"

    purpose = context.purpose
    if isinstance(purpose, Rewarding):
        withdrawn = total_withdrawn(tx_info.wdrl)
        paid = lovelace_paid_to(addr, tx_info.outputs)
        assert 2 * paid >= withdrawn, "insufficient reward sharing"
    elif isinstance(purpose, Certifying):
        pass
    else:
        assert False, "unexpected script purpose"
