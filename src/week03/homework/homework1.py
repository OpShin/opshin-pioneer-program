from opshin.prelude import *


@dataclass()
class VestingDatum(PlutusData):
    beneficiary1: PubKeyHash
    beneficiary2: PubKeyHash
    deadline: POSIXTime


# This should validate if either beneficiary1 has signed the transaction and the current slot is before or at the
# deadline or if beneficiary2 has signed the transaction and the deadline has passed.
def validator(datum: VestingDatum, redeemer: None, context: ScriptContext) -> None:
    assert False  # FIX ME!
