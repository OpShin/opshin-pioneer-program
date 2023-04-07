from opshin.prelude import *


# This policy should only allow minting (or burning) of tokens if the owner of the specified PubKeyHash
# has signed the transaction and if the specified deadline has not passed.
def validator(
    pkh: PubKeyHash, deadline: POSIXTime, redeemer: None, context: ScriptContext
) -> None:
    assert False  # Fix this
