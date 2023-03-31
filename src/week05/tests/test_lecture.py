import pytest
from opshin import compiler

from src.week05 import lecture_dir

python_files = [
    "free.py",
    "nft.py",
    "signed.py",
]
script_paths = [str(lecture_dir.joinpath(f)) for f in python_files]


@pytest.mark.parametrize("path", script_paths)
def test_lecture_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())
