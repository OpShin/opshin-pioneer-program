from opshin.ledger.interval import *


# This policy should only allow minting (or burning) of tokens if the owner of the specified PubKeyHash
# has signed the transaction and if the specified deadline has not passed.
def validator(
    pkh: PubKeyHash, deadline: POSIXTime, redeemer: None, context: ScriptContext
) -> None:
    assert pkh in context.tx_info.signatories, "transaction not signed"
    assert contains(make_to(deadline), context.tx_info.valid_range), "deadline passed"
