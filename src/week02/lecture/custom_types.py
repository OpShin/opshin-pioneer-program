from eopsin.prelude import *


@dataclass()
class MySillyRedeemer(PlutusData):
    r: int


def validator(datum: None, redeemer: MySillyRedeemer, context: ScriptContext) -> bool:
    return redeemer.r == 42
