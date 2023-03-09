# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import hypothesis
from hypothesis import given, strategies as st

from src.week03.lecture.interval import *

compare_extended_operands = st.one_of(
    st.builds(FinitePOSIXTime), st.builds(NegInfPOSIXTime), st.builds(PosInfPOSIXTime)
)


@given(
    a=compare_extended_operands,
    b=compare_extended_operands,
    c=compare_extended_operands,
)
def test_ordering_compare_extended(
    a: ExtendedPOSIXTime,
    b: ExtendedPOSIXTime,
    c: ExtendedPOSIXTime,
) -> None:
    left = compare_extended(a, b)
    right = compare_extended(b, c)
    hypothesis.assume(left == right)
    outer = compare_extended(a, c)
    assert outer == right, (left, outer, right)


@given(a=compare_extended_operands, b=compare_extended_operands)
def test_commutative_compare_extended(
    a: ExtendedPOSIXTime,
    b: ExtendedPOSIXTime,
) -> None:
    left = compare_extended(a, b)
    right = compare_extended(b, a)
    assert left == -right, (left, right)


compare_lower_bound_operands = st.builds(LowerBoundPOSIXTime)


@given(
    a=compare_lower_bound_operands,
    b=compare_lower_bound_operands,
    c=compare_lower_bound_operands,
)
def test_ordering_compare_lower_bound(
    a: LowerBoundPOSIXTime,
    b: LowerBoundPOSIXTime,
    c: LowerBoundPOSIXTime,
) -> None:
    left = compare_lower_bound(a, b)
    right = compare_lower_bound(b, c)
    hypothesis.assume(left == right)
    outer = compare_lower_bound(a, c)
    assert outer == right, (left, outer, right)


@given(a=compare_lower_bound_operands, b=compare_lower_bound_operands)
def test_commutative_lower_bound(
    a: LowerBoundPOSIXTime,
    b: LowerBoundPOSIXTime,
) -> None:
    left = compare_lower_bound(a, b)
    right = compare_lower_bound(b, a)
    assert left == -right, (left, right)


compare_upper_bound_operands = st.builds(UpperBoundPOSIXTime)


@given(
    a=compare_upper_bound_operands,
    b=compare_upper_bound_operands,
    c=compare_upper_bound_operands,
)
def test_ordering_compare_upper_bound(
    a: UpperBoundPOSIXTime,
    b: UpperBoundPOSIXTime,
    c: UpperBoundPOSIXTime,
) -> None:
    left = compare_upper_bound(a, b)
    right = compare_upper_bound(b, c)
    hypothesis.assume(left == right)
    outer = compare_upper_bound(a, c)
    assert outer == right, (left, outer, right)


@given(a=compare_upper_bound_operands, b=compare_upper_bound_operands)
def test_commutative_compare_upper_bound(
    a: UpperBoundPOSIXTime,
    b: UpperBoundPOSIXTime,
) -> None:
    left = compare_upper_bound(a, b)
    right = compare_upper_bound(b, a)
    assert left == -right, (left, right)


contains_operands = st.builds(POSIXTimeRange)


@given(a=contains_operands, b=contains_operands)
def test_contains(a: POSIXTimeRange, b: POSIXTimeRange):
    lower = compare_lower_bound(a.lower_bound, b.lower_bound)
    upper = compare_upper_bound(a.upper_bound, b.upper_bound)
    if contains(a, b):
        assert lower == 1 or lower == 0
        assert upper == 0 or upper == -1
    else:
        assert lower == -1 or upper == 1


@given(
    lower_bound=st.integers(),
    lower_closed=st.one_of(st.builds(FalseData), st.builds(TrueData)),
)
def test_fuzz_get_from(
    lower_bound: int,
    lower_closed: BoolData,
) -> None:
    get_from(lower_bound=lower_bound, lower_closed=lower_closed)


@given(
    lower_bound=st.integers(),
    upper_bound=st.integers(),
    lower_closed=st.one_of(st.builds(FalseData), st.builds(TrueData)),
    upper_closed=st.one_of(st.builds(FalseData), st.builds(TrueData)),
)
def test_fuzz_get_range(
    lower_bound: int,
    upper_bound: int,
    lower_closed: BoolData,
    upper_closed: BoolData,
) -> None:
    get_range(
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        lower_closed=lower_closed,
        upper_closed=upper_closed,
    )


@given(
    upper_bound=st.integers(),
    upper_closed=st.one_of(st.builds(FalseData), st.builds(TrueData)),
)
def test_fuzz_get_to(
    upper_bound: int,
    upper_closed: BoolData,
) -> None:
    get_to(upper_bound=upper_bound, upper_closed=upper_closed)
