from opshin.prelude import *


def assert_minting_purpose(context: ScriptContext) -> None:
    purpose = context.purpose
    if isinstance(purpose, Minting):
        is_minting = True
    else:
        is_minting = False
    assert is_minting, "not minting purpose"


def validator(redeemer: None, context: ScriptContext) -> None:
    assert_minting_purpose(context)
