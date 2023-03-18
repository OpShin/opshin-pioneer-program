import pytest
from opshin import compiler

from src.week03 import homework_dir

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
