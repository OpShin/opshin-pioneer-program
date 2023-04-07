from opshin.prelude import *


# Minting policy for an NFT, where the minting transaction must consume the given UTxO as input
# and where the TokenName will be the empty ByteString.
def validator(oref: TxOutRef, redeemer: None, context: ScriptContext) -> None:
    assert False  # Fix this
