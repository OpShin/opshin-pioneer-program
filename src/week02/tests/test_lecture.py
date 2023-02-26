from pathlib import Path

import pytest
from eopsin import compiler

lecture_dir = Path(__file__).parent.parent.joinpath("lecture")
python_files = [
    "burn.py",
    "custom_types.py",
    "fourty_two.py",
    "fourty_two_typed.py",
    "gift.py",
]
script_paths = [str(lecture_dir.joinpath(f)) for f in python_files]


@pytest.mark.parametrize("path", script_paths)
def test_lecture_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())
