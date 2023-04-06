from typing import List

import pytest
from opshin import compiler
from opshin.ledger.interval import make_range
from opshin.prelude import POSIXTimeRange, TrueData, PubKeyHash, TxInfo, ScriptContext

from src.week04 import homework_dir
from src.week04.homework import homework1, homework2

python_files = [
    "homework1.py",
    "homework2.py",
]
script_paths = [str(homework_dir.joinpath(f)) for f in python_files]


@pytest.mark.parametrize("path", script_paths)
def test_homework_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())


@pytest.mark.parametrize(
    ["deadline", "valid_lower", "valid_upper", "validates"],
    [
        [10, 5, 5, True],
        [10, 5, 10, True],
        [10, 9, 10, True],
        [10, 9, 11, False],
        [10, 10, 10, True],
        [10, 10, 15, False],
        [10, 15, 15, False],
    ],
)
def test_beneficiary_1(
    deadline: int, valid_lower: int, valid_upper: int, validates: bool
):
    evaluate_homework1_validator(
        deadline, make_range(valid_lower, valid_upper), validates, True, False
    )


@pytest.mark.parametrize(
    ["deadline", "valid_lower", "valid_upper", "validates"],
    [
        [10, 5, 5, False],
        [10, 5, 10, False],
        [10, 9, 11, False],
        [10, 10, 10, False],
        [10, 10, 15, False],
        [10, 11, 11, True],
        [10, 11, 12, True],
        [10, 11, 15, True],
        [10, 15, 15, True],
    ],
)
def test_beneficiary_2(
    deadline: int, valid_lower: int, valid_upper: int, validates: bool
):
    evaluate_homework1_validator(
        deadline, make_range(valid_lower, valid_upper), validates, False, True
    )


def evaluate_homework1_validator(
    deadline,
    valid_range,
    validates,
    beneficiary1_signed: bool,
    beneficiary2_signed: bool,
):
    datum = homework1.MisteryDatum(
        deadline=deadline,
        beneficiary1=b"1",
        beneficiary2=b"2",
    )
    signatories = []
    if beneficiary1_signed:
        signatories.append(b"1")
    if beneficiary2_signed:
        signatories.append(b"2")
    context = make_context(valid_range, signatories)
    try:
        homework1.validator(datum, None, context)
        passed = True
    except AssertionError as e:
        passed = False
    assert passed == validates


def make_context(valid_range: POSIXTimeRange, signatories: List[PubKeyHash]):
    tx_info = TxInfo(
        inputs=None,
        reference_inputs=None,
        outputs=None,
        fee=None,
        mint=None,
        dcert=None,
        wdrl=None,
        valid_range=valid_range,
        signatories=signatories,
        redeemers=None,
        data=None,
        id=None,
    )
    context = ScriptContext(tx_info=tx_info, purpose=None)
    return context


@pytest.mark.parametrize(
    ["deadline", "valid_lower", "valid_upper", "validates"],
    [
        [10, 20, 30, True],
        [10, 10, 10, True],
        [10, 10, 20, True],
        [10, 11, 20, True],
        [10, 19, 20, True],
        [10, 0, 10, False],
        [10, 9, 10, False],
        [10, 9, 11, False],
    ],
)
def test_homework_2(deadline: int, valid_lower: int, valid_upper: int, validates: bool):
    beneficiary = b"1"
    datum = deadline
    signatories = [b"1"]
    valid_range = make_range(valid_lower, valid_upper)
    context = make_context(valid_range, signatories)
    try:
        homework2.validator(beneficiary, datum, None, context)
        passed = True
    except AssertionError as e:
        passed = False
    assert passed == validates
