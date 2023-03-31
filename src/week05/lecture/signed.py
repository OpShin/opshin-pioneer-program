from opshin.prelude import *


def assert_minting_purpose(context: ScriptContext) -> None:
    purpose = context.purpose
    if isinstance(purpose, Minting):
        is_minting = True
    else:
        is_minting = False
    assert is_minting, "not minting purpose"


def assert_signed(pkh: PubKeyHash, context: ScriptContext) -> None:
    assert pkh in context.tx_info.signatories, "missing signature"


def validator(pkh: PubKeyHash, redeemer: None, context: ScriptContext) -> None:
    assert_minting_purpose(context)
    assert_signed(pkh, context)
