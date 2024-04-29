from opshin.prelude import *


# This should validate if and only if the two booleans in the redeemer list are True!
def validator(v: None, r: List[bool], c: ScriptContext) -> None:
    assert all(r)
