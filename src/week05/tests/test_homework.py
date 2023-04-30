import os
from typing import List, Tuple

import pytest
from opshin import compiler
from opshin.ledger.api_v2 import (
    POSIXTimeRange,
    PubKeyHash,
    TxInfo,
    ScriptContext,
    Minting,
    TxOutRef,
    TxId,
    TxInInfo,
)
from opshin.ledger.interval import make_range

from src.week05 import homework_dir
from src.week05.homework import homework1
from src.week05.homework import homework2

skip = "SKIP_HOMEWORK" in os.environ

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


@pytest.mark.skipif(skip, reason="skip homework tests if not implemented")
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
def test_homework1_deadline_met(
    deadline: int, valid_lower: int, valid_upper: int, validates: bool
):
    evaluate_homework1_validator(
        deadline, make_range(valid_lower, valid_upper), [b"1"], validates
    )


@pytest.mark.skipif(skip, reason="skip homework tests if not implemented")
@pytest.mark.parametrize(
    ["signatories", "validates"],
    [
        [[], False],
        [[b""], False],
        [[b"1"], True],
        [[b"2"], False],
        [[b"1", b"2"], True],
        [[b"2", b"3"], False],
    ],
)
def test_homework1_signed(signatories, validates):
    evaluate_homework1_validator(10, make_range(5, 5), signatories, validates)


def evaluate_homework1_validator(
    deadline: int,
    valid_range: POSIXTimeRange,
    signatories: List[bytes],
    validates: bool,
):
    context = make_context(valid_range, signatories)
    try:
        homework1.validator(b"1", deadline, None, context)
        passed = True
    except AssertionError as e:
        passed = False
    assert passed == validates


def make_context(
    valid_range: POSIXTimeRange, signatories: List[PubKeyHash], mint=None, inputs=None
):
    tx_info = TxInfo(
        inputs=inputs,
        reference_inputs=None,
        outputs=None,
        fee=None,
        mint=mint,
        dcert=None,
        wdrl=None,
        valid_range=valid_range,
        signatories=signatories,
        redeemers=None,
        data=None,
        id=None,
    )
    context = ScriptContext(tx_info=tx_info, purpose=Minting(b"policy_id"))
    return context


@pytest.mark.skipif(skip, reason="skip homework tests if not implemented")
@pytest.mark.parametrize(
    ["tx_id", "index", "mint", "validates"],
    [
        [b"1", 0, [(b"0", b"", 1)], False],
        [b"1", 1, [(b"0", b"", 1)], False],
        [b"0", 0, [(b"0", b"", 1)], True],
        [b"0", 1, [(b"0", b"", 1)], False],
        [b"0", 0, [(b"0", b"1", 1)], False],
        [b"0", 0, [(b"0", b"foo", 1)], False],
        [b"0", 0, [(b"0", b"", 1), (b"", b"", 0)], True],
        [b"0", 0, [(b"0", b"", 0), (b"", b"", 0)], False],
        [b"0", 0, [(b"", b"", 0)], False],
        [b"0", 0, [], False],
        [b"0", 0, [(b"1", b"", 1), (b"2", b"", 1)], False],
        [b"0", 0, [(b"0", b"", 2)], False],
        [b"0", 0, [(b"0", b"", 1000)], False],
        [b"0", 0, [(b"0", b"", -1)], False],
    ],
)
def test_homework_2(
    tx_id: bytes, index: int, mint: List[Tuple[bytes, bytes, int]], validates: bool
):
    oref_1 = TxOutRef(TxId(tx_id), index)
    inputs = [TxInInfo(oref_1, None)]
    mint_value = {}
    for policy_id, tn, amount in mint:
        mint_value[policy_id] = {tn: amount}
    context = make_context(
        valid_range=None, signatories=None, mint=mint_value, inputs=inputs
    )
    oref = TxOutRef(TxId(b"0"), 0)
    try:
        homework2.validator(oref, None, context)
        passed = True
    except AssertionError as e:
        passed = False
    assert passed == validates
