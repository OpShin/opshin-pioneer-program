import math

import pytest
from eopsin import compiler
from eopsin.prelude import (
    POSIXTime,
    POSIXTimeRange,
    LowerBoundPOSIXTime,
    UpperBoundPOSIXTime,
    TrueData,
    FalseData,
    FinitePOSIXTime,
    PosInfPOSIXTime,
    NegInfPOSIXTime,
)
from hypothesis import given, strategies as st

from src.week03 import lecture_dir
from src.week03.lecture import parameterized_vesting, vesting


def get_bool(b):
    return TrueData() if b else FalseData()


def get_posix_time_type(lower):
    if -math.inf < lower < math.inf:
        time = FinitePOSIXTime(lower)
    elif lower == -math.inf:
        time = NegInfPOSIXTime()
    else:
        time = PosInfPOSIXTime()
    return time


@pytest.mark.parametrize(
    ["time", "lower", "upper", "lower_closed", "upper_closed", "result"],
    [
        (1, 0, 2, True, True, True),
        (0, 0, 0, False, False, True),
        (0, 0, 0, True, True, False),
        (-1, 0, 2, True, True, False),
        (0, 0, 2, False, True, True),
        (0, -math.inf, math.inf, True, True, True),
    ],
)
def test_contains_example(time, lower, upper, lower_closed, upper_closed, result):
    time_range = POSIXTimeRange(
        LowerBoundPOSIXTime(get_posix_time_type(lower), get_bool(lower_closed)),
        UpperBoundPOSIXTime(get_posix_time_type(upper), get_bool(upper_closed)),
    )
    assert vesting.contains(time, time_range) == result
    assert parameterized_vesting.contains(time, time_range) == result


@given(st.integers(), st.integers(), st.integers(), st.booleans(), st.booleans())
def test_contains_hypothesis(time, lower, upper, lower_closed, upper_closed):
    if lower_closed:
        lower_comparison = lower < time
    else:
        lower_comparison = lower <= time
    if upper_closed:
        upper_comparison = time < upper
    else:
        upper_comparison = time <= upper
    result = lower_comparison and upper_comparison
    time_range = POSIXTimeRange(
        LowerBoundPOSIXTime(get_posix_time_type(lower), get_bool(lower_closed)),
        UpperBoundPOSIXTime(get_posix_time_type(upper), get_bool(upper_closed)),
    )
    assert vesting.contains(time, time_range) == result
    assert parameterized_vesting.contains(time, time_range) == result


@given(
    st.integers(),
    st.integers(),
    st.integers(),
    st.booleans(),
    st.booleans(),
    st.booleans(),
    st.booleans(),
    st.booleans(),
    st.booleans(),
)
def test_contains_hypothesis_inf(
    time,
    lower,
    upper,
    lower_closed,
    upper_closed,
    lower_inf,
    upper_inf,
    lower_pos_sign,
    upper_pos_sign,
):
    if lower_inf:
        lower = math.inf
    if not lower_pos_sign:
        lower = -lower
    if upper_inf:
        upper = math.inf
    if not upper_pos_sign:
        upper = -upper_inf
    if lower_closed:
        lower_comparison = lower < time
    else:
        lower_comparison = lower <= time
    if upper_closed:
        upper_comparison = time < upper
    else:
        upper_comparison = time <= upper
    result = lower_comparison and upper_comparison
    time_range = POSIXTimeRange(
        LowerBoundPOSIXTime(get_posix_time_type(lower), get_bool(lower_closed)),
        UpperBoundPOSIXTime(get_posix_time_type(upper), get_bool(upper_closed)),
    )
    assert vesting.contains(time, time_range) == result
    assert parameterized_vesting.contains(time, time_range) == result


python_files = [
    "vesting.py",
    "parameterized_vesting.py",
]
script_paths = [str(lecture_dir.joinpath(f)) for f in python_files]


@pytest.mark.parametrize("path", script_paths)
def test_lecture_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())
