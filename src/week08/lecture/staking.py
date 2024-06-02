from opshin.prelude import *


def get_amount(context: ScriptContext, purpose: Rewarding) -> int:
    amount = 0
    found = False
    for staking_cred, a in context.tx_info.wdrl.items():
        if staking_cred == purpose.staking_credential:
            found = True
            amount = a
    assert found, "withdrawal not found"
    return amount


def validator(addr: Address, _: None, context: ScriptContext):
    purpose = context.purpose
    if isinstance(purpose, Certifying):
        print("certifying")
    elif isinstance(purpose, Rewarding):
        amount = get_amount(context, purpose)
        paid_amount = all_tokens_locked_at_address(
            context.tx_info.outputs, addr, Token(b"", b"")
        )
        assert 2 * paid_amount >= amount, "insufficient reward sharing"
    else:
        assert False, "script purpose must be certifying or rewarding"
