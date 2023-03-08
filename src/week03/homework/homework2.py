from eopsin.prelude import *


def validator(
    beneficiary: PubKeyHash, deadline: POSIXTime, redeemer: None, context: ScriptContext
) -> bool:
    return False  # FIX ME!
