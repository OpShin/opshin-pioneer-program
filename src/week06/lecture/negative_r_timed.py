from opshin.ledger.interval import *


@dataclass()
class CustomDatum(PlutusData):
    deadline: POSIXTime


def validator(datum: CustomDatum, redeemer: int, context: ScriptContext):
    assert redeemer <= 0, "expected a negative redeemer"
    assert contains(
        make_from(datum.deadline), context.tx_info.valid_range
    ), "deadline not reached"
