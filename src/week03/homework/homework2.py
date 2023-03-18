from opshin.prelude import *


# This should validate if the transaction has a signature from the parameterized beneficiary
# and the deadline has passed.
def validator(
    beneficiary: PubKeyHash, deadline: POSIXTime, redeemer: None, context: ScriptContext
) -> None:
    assert False  # FIX ME!
