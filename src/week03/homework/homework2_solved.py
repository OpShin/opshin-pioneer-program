from opshin.ledger.interval import *


# This should validate if the transaction has a signature from the parameterized beneficiary
# and the deadline has passed.
def validator(
    beneficiary: PubKeyHash, deadline: POSIXTime, redeemer: None, context: ScriptContext
) -> None:
    signed = beneficiary in context.tx_info.signatories
    deadline_met = contains(
        make_from(deadline, TrueData()), context.tx_info.valid_range
    )
    assert signed and deadline_met
