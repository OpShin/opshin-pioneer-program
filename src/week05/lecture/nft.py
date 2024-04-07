from opshin.prelude import *


def get_minting_purpose(context: ScriptContext) -> Minting:
    purpose = context.purpose
    if isinstance(purpose, Minting):
        is_minting = True
    else:
        is_minting = False
    assert is_minting, "Not minting purpose"
    minting_purpose: Minting = purpose
    return minting_purpose


def check_mint_exactly_one_with_name(
    token: Token,
    mint: Value,
) -> None:
    assert (
        mint[token.policy_id][token.token_name] == 1
    ), "Exactly 1 token must be minted"
    assert len(mint[token.policy_id]) == 1, "No other token must be minted"


def has_utxo(context: ScriptContext, oref: TxOutRef) -> bool:
    return any([oref == i.out_ref for i in context.tx_info.inputs])


def validator(
    oref: TxOutRef, tn: TokenName, redeemer: None, context: ScriptContext
) -> None:
    minting_purpose = get_minting_purpose(context)
    check_mint_exactly_one_with_name(
        Token(minting_purpose.policy_id, tn), context.tx_info.mint
    )
    assert has_utxo(context, oref), "UTxO not consumed"
