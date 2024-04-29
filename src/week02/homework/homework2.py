from opshin.prelude import *


@dataclass()
class MyRedeemer(PlutusData):
    CONSTR_ID = 0
    flag1: bool
    flag2: bool


# Create a validator that unlocks the funds if MyRedemeer's flags are different
def validator(v: None, r: MyRedeemer, c: ScriptContext) -> None:
    assert False, "Not implemented yet!"
