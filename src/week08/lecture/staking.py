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


def paid_to_address(addr: Address, context: ScriptContext) -> int:
    paid_amount = 0
    for output in context.tx_info.outputs:
        if output.address == addr:
            paid_amount += output.value.get(b"", {b"": 0}).get(b"", 0)
    return paid_amount


def validator(addr: Address, _: None, context: ScriptContext):
    purpose = context.purpose
    if isinstance(purpose, Certifying):
        print("certifying")
    elif isinstance(purpose, Rewarding):
        amount = get_amount(context, purpose)
        paid_amount = paid_to_address(addr, context)
        assert 2 * paid_amount >= amount, "insufficient reward sharing"
    else:
        assert False, "script purpose must be certifying or rewarding"
