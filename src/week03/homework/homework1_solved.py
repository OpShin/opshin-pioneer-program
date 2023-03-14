from src.week03.lecture.interval import *


@dataclass()
class VestingDatum(PlutusData):
    beneficiary1: PubKeyHash
    beneficiary2: PubKeyHash
    deadline: POSIXTime


# This should validate if either beneficiary1 has signed the transaction and the current slot is before or at the
# deadline or if beneficiary2 has signed the transaction and the deadline has passed.
def validator(datum: VestingDatum, redeemer: None, context: ScriptContext) -> None:
    signed1 = datum.beneficiary1 in context.tx_info.signatories
    signed2 = datum.beneficiary2 in context.tx_info.signatories
    deadline1 = contains(
        make_to(datum.deadline, TrueData()), context.tx_info.valid_range
    )
    deadline2 = contains(
        make_from(datum.deadline, FalseData()), context.tx_info.valid_range
    )
    assert (signed1 and deadline1) or (signed2 and deadline2)
