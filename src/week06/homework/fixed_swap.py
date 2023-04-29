from opshin.prelude import *


@dataclass()
class DatumSwap(PlutusData):
    beneficiary: PubKeyHash
    price: int


# Implement the swap protocol but avoid the double spending issue in exploitable_swap.py
def validator(datum: DatumSwap, redeemer: None, context: ScriptContext):
    assert False  # fix me!
