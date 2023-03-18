from opshin.prelude import *


def validator(datum: None, redeemer: int, context: ScriptContext) -> None:
    assert redeemer == 42
