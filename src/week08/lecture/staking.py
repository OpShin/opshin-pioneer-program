"""
The validator is parameterized by an `Address`. It controls a stake credential
and allows:

  * any certification action (registering/deregistering the credential,
    delegating it to a pool), and
  * withdrawing rewards, **provided at least half of the withdrawn amount is
    paid out (in ADA) to the parameter address in the same transaction**.

It is invoked under either the `Certifying` or `Rewarding` script purpose.
Spending-purpose invocations are rejected (this script is not meant to be used
as a spending validator).
"""

from opshin.prelude import *


def withdrawal_amount(
    cred: StakingCredential, wdrl: Dict[StakingCredential, int]
) -> int:
    """Return the amount withdrawn for `cred`, failing if no entry exists."""
    amount = wdrl.get(cred, -1)
    assert amount >= 0, "withdrawal not found"
    return amount


def lovelace_paid_to(addr: Address, outputs: List[TxOut]) -> int:
    """Sum of ADA (in lovelace) sent to `addr` across all transaction outputs."""
    return sum(
        [o.value.get(b"", {b"": 0}).get(b"", 0) for o in outputs if o.address == addr]
    )


def validator(addr: Address, redeemer: None, context: ScriptContext) -> None:
    purpose = context.purpose
    if isinstance(purpose, Certifying):
        # Anything goes for registration / de-registration / delegation.
        pass
    elif isinstance(purpose, Rewarding):
        amount = withdrawal_amount(
            purpose.staking_credential, context.tx_info.wdrl
        )
        paid = lovelace_paid_to(addr, context.tx_info.outputs)
        assert 2 * paid >= amount, "insufficient reward sharing"
    else:
        assert False, "unexpected script purpose"
