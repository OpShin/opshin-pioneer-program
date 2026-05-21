import pytest
from opshin import compiler

from src.week09 import on_chain_dir

python_files = [
    "collateral.py",
    "minting.py",
    "nft.py",
    "oracle.py",
]
script_paths = [str(on_chain_dir.joinpath(f)) for f in python_files]


@pytest.mark.parametrize("path", script_paths)
def test_lecture_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())
