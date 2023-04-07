from opshin.prelude import *


def check_minted(context: ScriptContext) -> bool:
    mint_value = context.tx_info.mint
    correct_token_name = True
    correct_amount = True
    count = 0
    for policy_id in mint_value.keys():
        v = mint_value.get(policy_id, {b"": 0})
        if len(v.keys()) == 1:
            for token_name in v.keys():
                amount = v.get(token_name, 0)
                if amount != 0:
                    correct_token_name = correct_token_name and token_name == b""
                    correct_amount = correct_amount and amount == 1
                    count += 1
    return count == 1 and correct_token_name and correct_amount


# Minting policy for an NFT, where the minting transaction must consume the given UTxO as input
# and where the TokenName will be the empty ByteString.
def validator(oref: TxOutRef, redeemer: None, context: ScriptContext) -> None:
    assert any([oref == i.out_ref for i in context.tx_info.inputs]), "utxo not found"
    assert check_minted(context), "minted wrong value"
