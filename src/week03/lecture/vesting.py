from eopsin.prelude import *


@dataclass()
class VestingParams(PlutusData):
    beneficiary: PubKeyHash
    deadline: POSIXTime


def signed_by_beneficiary(params: VestingParams, context: ScriptContext) -> bool:
    return params.beneficiary in context.tx_info.signatories


def contains(time: POSIXTime, time_range: POSIXTimeRange) -> bool:
    # Lower bound
    lower_comparison = False
    lower_limit = time_range.lower_bound.limit
    lower_closed = time_range.lower_bound.closed
    if isinstance(lower_limit, FinitePOSIXTime):
        lower_time = lower_limit.time
        if isinstance(lower_closed, TrueData):
            lower_comparison = lower_time < time
        else:
            lower_comparison = lower_time <= time
    if isinstance(lower_limit, NegInfPOSIXTime):
        lower_comparison = True
    # Upper bound
    upper_comparison = False
    upper_limit = time_range.upper_bound.limit
    upper_closed = time_range.upper_bound.closed
    if isinstance(upper_limit, FinitePOSIXTime):
        upper_time = upper_limit.time
        if isinstance(upper_closed, TrueData):
            upper_comparison = time < upper_time
        else:
            upper_comparison = time <= upper_time
    if isinstance(upper_limit, PosInfPOSIXTime):
        upper_comparison = True
    return lower_comparison and upper_comparison


def deadline_reached(params: VestingParams, context: ScriptContext) -> bool:
    deadline: POSIXTime = params.deadline
    valid_range: POSIXTimeRange = context.tx_info.valid_range
    return contains(deadline, valid_range)


def validator(datum: VestingParams, redeemer: None, context: ScriptContext) -> bool:
    assert signed_by_beneficiary(datum, context), "beneficiary's signature missing"
    assert deadline_reached(datum, context), "deadline not reached"
    return True
