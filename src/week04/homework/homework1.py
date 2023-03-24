# Prompt:
# 1- Figure out what this (already finished) validator does by using all the tools at your disposal.
# 2- Write the off-chain code necessary to cover all possible interactions with the validator using
#    the off-chain tool of your choosing.
# HINT: If you get stuck, take a look at Week03's lecture

from opshin.ledger.interval import *


@dataclass()
class MisteryDatum(PlutusData):
    beneficiary1: PubKeyHash
    beneficiary2: PubKeyHash
    deadline: POSIXTime


def validator(datum: MisteryDatum, redeemer: None, context: ScriptContext) -> None:
    valid_range = context.tx_info.valid_range
    signed1 = datum.beneficiary1 in context.tx_info.signatories
    deadline1 = contains(make_to(datum.deadline, TrueData()), valid_range)
    condition1 = signed1 and deadline1
    if not condition1:
        print("Benificiary1 did not sign or to late")
    signed2 = datum.beneficiary2 in context.tx_info.signatories
    deadline2 = contains(make_from(datum.deadline, FalseData()), valid_range)
    condition2 = signed2 and deadline2
    if not condition2:
        print("Benificiary2 did not sign or is to early")
    assert condition1 or condition2
