# Prompt:
# 1- Figure out what this (already finished) validator does by using all the tools at your disposal.
# 2- Write the off-chain code necessary to cover all possible interactions with the validator using
#    the off-chain tool of your choosing.
# HINT: If you get stuck, take a look at Week03's lecture

from opshin.ledger.interval import *


def validator(
    beneficiary: PubKeyHash, deadline: POSIXTime, redeemer: None, context: ScriptContext
) -> None:
    signed = beneficiary in context.tx_info.signatories
    assert signed, "not signed by beneficiary"
    deadline_met = contains(
        make_from(deadline, TrueData()), context.tx_info.valid_range
    )
    assert deadline_met, "deadline has not passed yet"
