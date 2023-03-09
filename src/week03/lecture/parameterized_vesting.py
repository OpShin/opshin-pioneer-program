from src.week03.lecture.interval import *


@dataclass()
class VestingParams(PlutusData):
    beneficiary: PubKeyHash
    deadline: POSIXTime


def signed_by_beneficiary(params: VestingParams, context: ScriptContext) -> bool:
    return params.beneficiary in context.tx_info.signatories


def deadline_reached(params: VestingParams, context: ScriptContext) -> bool:
    deadline: POSIXTime = params.deadline
    valid_range: POSIXTimeRange = context.tx_info.valid_range
    return contains(make_from(deadline, TrueData()), valid_range)


def validator(
    params: VestingParams, datum: None, redeemer: None, context: ScriptContext
) -> None:
    assert signed_by_beneficiary(params, context), "beneficiary's signature missing"
    assert deadline_reached(params, context), "deadline not reached"
