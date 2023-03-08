from eopsin.prelude import *


def in_lower_bound(time: POSIXTime, lower: LowerBoundPOSIXTime) -> bool:
    lower_limit = lower.limit
    lower_closed = lower.closed
    if isinstance(lower_limit, FinitePOSIXTime):
        lower_time = lower_limit.time
        if isinstance(lower_closed, TrueData):
            result = lower_time <= time
        else:
            result = lower_time < time
    elif isinstance(lower_limit, NegInfPOSIXTime):
        result = True
    else:
        result = False
    return result


def in_upper_bound(time: POSIXTime, upper: UpperBoundPOSIXTime) -> bool:
    upper_limit = upper.limit
    upper_closed = upper.closed
    if isinstance(upper_limit, FinitePOSIXTime):
        upper_time = upper_limit.time
        if isinstance(upper_closed, TrueData):
            result = time <= upper_time
        else:
            result = time < upper_time
    elif isinstance(upper_limit, PosInfPOSIXTime):
        result = True
    else:
        result = False
    return result


def contains(time: POSIXTime, time_range: POSIXTimeRange) -> bool:
    lower_comparison = in_lower_bound(time, time_range.lower_bound)
    upper_comparison = in_upper_bound(time, time_range.upper_bound)
    return lower_comparison and upper_comparison
