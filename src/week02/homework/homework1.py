from eopsin.prelude import *

# `Tuple` is not supported yet
# This should validate if and only if the two Booleans in the redeemer are True!
# def validator(v: None, r: Tuple[bool, bool], c: ScriptContext) -> None:
#     assert False


# This should validate if and only if the Booleans in the redeemer list are True!
def validator(v: None, r: List[bool], c: ScriptContext) -> None:
    assert False
