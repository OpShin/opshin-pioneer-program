from src.week03.lecture.interval import *


def validator(
    beneficiary: PubKeyHash, deadline: POSIXTime, redeemer: None, context: ScriptContext
) -> None:
    signed = beneficiary in context.tx_info.signatories
    deadline_met = contains(get_from(deadline, TrueData()), context.tx_info.valid_range)
    assert signed and deadline_met
