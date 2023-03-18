from opshin.prelude import *


@dataclass()
class MySillyRedeemer(PlutusData):
    r: int


def validator(datum: None, redeemer: MySillyRedeemer, context: ScriptContext) -> None:
    assert redeemer.r == 42
