from eopsin.prelude import *


def validator(datum: None, redeemer: int, context: ScriptContext) -> bool:
    return redeemer == 42
