import subprocess
from pathlib import Path

import pytest

from src.week02.homework import homework1, homework2


# from src.week02.homework import homework1_solved as homework1
# from src.week02.homework import homework2_solved as homework2


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
    assert homework1.validator(None, [r1, r2], None) == result


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
    assert homework2.validator(None, redeemer, None) == result


homework_dir = Path(__file__).parent.parent.joinpath("homework")
script_paths = [
    homework_dir.joinpath("homework1.py"),
    homework_dir.joinpath("homework1_solved.py"),
    homework_dir.joinpath("homework2.py"),
    homework_dir.joinpath("homework2_solved.py"),
]


@pytest.mark.parametrize("path", script_paths)
def test_homework_compile(path):
    subprocess.run(["eopsin", "compile", str(path)], check=True)
