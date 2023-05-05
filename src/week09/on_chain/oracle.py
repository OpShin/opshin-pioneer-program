from opshin.prelude import *


@dataclass()
class OracleParams(PlutusData):
    nft: None
    operator: PubKeyHash


@dataclass()
class Update(PlutusData):
    CONSTR_ID = 1046


@dataclass()
class Delete(PlutusData):
    CONSTR_ID = 1047


OracleRedeemer = Union[Update, Delete]


def validator(
    oracle: OracleParams, rate: int, r: OracleRedeemer, context: ScriptContext
):
    pass
