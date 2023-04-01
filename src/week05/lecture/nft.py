from opshin.prelude import *


def assert_minting_purpose(context: ScriptContext) -> None:
    purpose = context.purpose
    if isinstance(purpose, Minting):
        is_minting = True
    else:
        is_minting = False
    assert is_minting, "not minting purpose"


def has_utxo(context: ScriptContext, oref: TxOutRef) -> bool:
    return any([oref == i.out_ref for i in context.tx_info.inputs])


def check_minted_amount(tn: TokenName, context: ScriptContext) -> bool:
    mint_value = context.tx_info.mint
    valid = False
    count = 0
    for policy_id in mint_value.keys():
        v = mint_value.get(policy_id, {b"": 0})
        if len(v.keys()) == 1:
            for token_name in v.keys():
                amount = v.get(token_name, 0)
                valid = token_name == tn and amount == 1
                if amount != 0:
                    count += 1
    return valid and count == 1


def validator(
    oref: TxOutRef, tn: TokenName, redeemer: None, context: ScriptContext
) -> None:
    assert_minting_purpose(context)
    assert has_utxo(context, oref), "UTxO not consumed"
    assert check_minted_amount(tn, context), "wrong amount minted"
