import os

import pytest
from opshin import compiler

from src.week02 import homework_dir
from src.week02.homework import homework1, homework2


if "TEST_SOLVED" in os.environ:
    from src.week02.homework import homework1_solved as homework1
    from src.week02.homework import homework2_solved as homework2


@pytest.mark.parametrize(
    ["r1", "r2", "result"],
    [
        (False, False, False),
        (True, False, False),
        (False, True, False),
        (True, True, True),
    ],
)
def test_homework1(r1: bool, r2: bool, result: bool):
    validate = True
    try:
        homework1.validator(None, [r1, r2], None)
    except AssertionError:
        validate = False
    assert validate == result


@pytest.mark.parametrize(
    ["r1", "r2", "result"],
    [
        (False, False, False),
        (True, False, True),
        (False, True, True),
        (True, True, False),
    ],
)
def test_homework2(r1: bool, r2: bool, result: bool):
    redeemer = homework2.MyRedeemer(flag1=r1, flag2=r2)
    validate = True
    try:
        homework2.validator(None, redeemer, None)
    except AssertionError:
        validate = False
    assert validate == result


python_files = [
    "homework1.py",
    "homework1_solved.py",
    "homework2.py",
    "homework2_solved.py",
]
script_paths = [str(homework_dir.joinpath(f)) for f in python_files]


@pytest.mark.parametrize("path", script_paths)
def test_homework_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())
