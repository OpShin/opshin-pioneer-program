from src.week03.lecture.interval import *


@dataclass()
class VestingParams(PlutusData):
    beneficiary: PubKeyHash
    deadline: POSIXTime


def signed_by_beneficiary(params: VestingParams, context: ScriptContext) -> bool:
    return params.beneficiary in context.tx_info.signatories


def is_after(deadline: POSIXTime, valid_range: POSIXTimeRange) -> bool:
    # To ensure that the `valid_range` occurs after the `deadline`,
    # we construct an interval from `deadline` to infinity
    # then check whether that interval contains the `valid_range` interval.
    from_interval: POSIXTimeRange = make_from(deadline, TrueData())
    return contains(from_interval, valid_range)


def deadline_reached(params: VestingParams, context: ScriptContext) -> bool:
    # The current transaction can only execute in `valid_range`,
    # so the current execution time is always within `valid_range`.
    # Therefore, to make all possible execution times occur after the deadline,
    # we need to make sure the whole `valid_range` interval occurs after the `deadline`.
    deadline: POSIXTime = params.deadline
    valid_range: POSIXTimeRange = context.tx_info.valid_range
    return is_after(deadline, valid_range)


def validator(
    params: VestingParams, datum: None, redeemer: None, context: ScriptContext
) -> None:
    assert signed_by_beneficiary(params, context), "beneficiary's signature missing"
    assert deadline_reached(params, context), "deadline not reached"
