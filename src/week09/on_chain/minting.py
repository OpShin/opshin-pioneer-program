from opshin.prelude import *


@dataclass()
class MintParams(PlutusData):
    oracle_validator: ValidatorHash
    collateral_validator: ValidatorHash
    collateral_min_percent: int


@dataclass()
class Mint(PlutusData):
    CONSTR_ID = 1042


@dataclass()
class Burn(PlutusData):
    CONSTR_ID = 1043


@dataclass()
class Liquidate(PlutusData):
    CONSTR_ID = 1045


MintRedeemer = Union[Mint, Burn, Liquidate]


def validator(mp: MintParams, r: None, context: ScriptContext):
    pass
