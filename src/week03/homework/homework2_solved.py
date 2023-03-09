from src.week03.lecture.range import *


def validator(
    beneficiary: PubKeyHash, deadline: POSIXTime, redeemer: None, context: ScriptContext
) -> None:
    signed = beneficiary in context.tx_info.signatories
    deadline_met = contains(deadline, context.tx_info.valid_range)
    assert signed and deadline_met
