from opshin.prelude import *


@dataclass()
class MyRedeemer(PlutusData):
    flag1: bool
    flag2: bool


# Create a validator that unlocks the funds if MyRedemeer's flags are different
def validator(v: None, r: MyRedeemer, c: ScriptContext) -> None:
    assert not r.flag1 == r.flag2
