"""
Homework: a staking validator with two parameters, a `PubKeyHash` and an
`Address`. The validator should work as follows:

  1. The given `PubKeyHash` must sign every transaction involving this script.
  2. The given `Address` must receive at least half of all withdrawn rewards
     (paid in ADA / lovelace).

This is the OpShin equivalent of
`plutus-pioneer-program/code/Week08/homework/Homework.hs`.

Replace the body of `validator` with your solution.
"""

from opshin.prelude import *


def validator(
    pkh: PubKeyHash,
    addr: Address,
    _r: None,
    context: ScriptContext,
) -> None:
    # TODO: implement
    assert False, "not implemented"
