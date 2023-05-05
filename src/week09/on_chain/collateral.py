from opshin.prelude import *


CurrencySymbol = bytes


@dataclass()
class CollateralDatum(PlutusData):
    minting_policy_id: CurrencySymbol
    owner: PubKeyHash
    stable_coin_amount: int


@dataclass()
class Redeem(PlutusData):
    CONSTR_ID = 1048


@dataclass()
class Liquidate(PlutusData):
    CONSTR_ID = 1049


CollateralRedeemer = Union[Redeem, Liquidate]


def validator(datum: CollateralDatum, r: CollateralRedeemer, context: ScriptContext):
    pass
