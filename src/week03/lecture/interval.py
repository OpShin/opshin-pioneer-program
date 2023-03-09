from eopsin.prelude import *


def compare_extended(a: ExtendedPOSIXTime, b: ExtendedPOSIXTime) -> int:
    # a < b: 1
    # a == b: 0
    # a > b: -1
    result = 0
    if isinstance(a, NegInfPOSIXTime):
        if isinstance(b, NegInfPOSIXTime):
            result = 0
        else:
            result = 1
    elif isinstance(a, PosInfPOSIXTime):
        if isinstance(b, PosInfPOSIXTime):
            result = 0
        else:
            result = -1
    elif isinstance(a, FinitePOSIXTime):
        if isinstance(b, NegInfPOSIXTime):
            result = -1
        elif isinstance(b, PosInfPOSIXTime):
            result = 1
        elif isinstance(b, FinitePOSIXTime):
            if a.time < b.time:
                result = 1
            elif a.time == b.time:
                result = 0
            else:
                result = -1
    return result


def compare_upper_bound(a: UpperBoundPOSIXTime, b: UpperBoundPOSIXTime) -> int:
    # a < b: 1
    # a == b: 0
    # a > b: -1
    a_closed = a.closed
    b_closed = b.closed
    result = compare_extended(a.limit, b.limit)
    if result == 0:
        if isinstance(a_closed, TrueData):
            a_val = 1
        else:
            a_val = 0
        if isinstance(b_closed, TrueData):
            b_val = 1
        else:
            b_val = 0
        if a_val < b_val:
            result = 1
        elif a_val == b_val:
            result = 0
        else:
            result = -1
    return result


def compare_lower_bound(a: LowerBoundPOSIXTime, b: LowerBoundPOSIXTime) -> int:
    # a < b: 1
    # a == b: 0
    # a > b: -1
    a_closed = a.closed
    b_closed = b.closed
    result = compare_extended(a.limit, b.limit)
    if result == 0:
        if isinstance(a_closed, TrueData):
            a_val = 1
        else:
            a_val = 0
        if isinstance(b_closed, TrueData):
            b_val = 1
        else:
            b_val = 0
        if a_val > b_val:
            result = 1
        elif a_val == b_val:
            result = 0
        else:
            result = -1
    return result


def contains(a: POSIXTimeRange, b: POSIXTimeRange) -> bool:
    # Returns True if the interval `b` is entirely contained in `a`.
    lower = compare_lower_bound(a.lower_bound, b.lower_bound)
    upper = compare_upper_bound(a.upper_bound, b.upper_bound)
    return (lower == 1 or lower == 0) and (upper == 0 or upper == -1)


def get_range(
    lower_bound: POSIXTime,
    upper_bound: POSIXTime,
    lower_closed: BoolData,
    upper_closed: BoolData,
) -> POSIXTimeRange:
    return POSIXTimeRange(
        LowerBoundPOSIXTime(FinitePOSIXTime(lower_bound), lower_closed),
        UpperBoundPOSIXTime(FinitePOSIXTime(upper_bound), upper_closed),
    )


def get_from(lower_bound: POSIXTime, lower_closed: BoolData) -> POSIXTimeRange:
    return POSIXTimeRange(
        LowerBoundPOSIXTime(FinitePOSIXTime(lower_bound), lower_closed),
        UpperBoundPOSIXTime(PosInfPOSIXTime(), TrueData()),
    )


def get_to(upper_bound: POSIXTime, upper_closed: BoolData) -> POSIXTimeRange:
    return POSIXTimeRange(
        LowerBoundPOSIXTime(NegInfPOSIXTime(), TrueData()),
        UpperBoundPOSIXTime(FinitePOSIXTime(upper_bound), upper_closed),
    )
