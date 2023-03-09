from src.week03.lecture.range import *


@dataclass()
class VestingDatum(PlutusData):
    beneficiary1: PubKeyHash
    beneficiary2: PubKeyHash
    deadline: POSIXTime


# This should validate if either beneficiary1 has signed the transaction and the current slot is before or at the
# deadline or if beneficiary2 has signed the transaction and the deadline has passed.
def validator(datum: VestingDatum, redeemer: None, context: ScriptContext) -> bool:
    signed1 = datum.beneficiary1 in context.tx_info.signatories
    signed2 = datum.beneficiary2 in context.tx_info.signatories
    deadline1 = in_lower_bound(datum.deadline, context.tx_info.valid_range.lower_bound)
    deadline2 = not deadline1
    return (signed1 and deadline1) or (signed2 and deadline2)
