from pathlib import Path

import pytest
from eopsin import compiler

lecture_dir = Path(__file__).parent.parent.joinpath("lecture")
script_paths = [
    lecture_dir.joinpath("burn.py"),
    lecture_dir.joinpath("custom_types.py"),
    lecture_dir.joinpath("fourty_two.py"),
    lecture_dir.joinpath("fourty_two_typed.py"),
    lecture_dir.joinpath("gift.py"),
]


@pytest.mark.parametrize("path", script_paths)
def test_lecture_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())
