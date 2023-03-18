from opshin.prelude import *


def validator(datum: BuiltinData, redeemer: BuiltinData, context: BuiltinData) -> None:
    r: int = redeemer
    assert r == 42
