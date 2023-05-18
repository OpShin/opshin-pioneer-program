from opshin.prelude import *

from src.week09.on_chain.common import *


@dataclass()
class Redeem(PlutusData):
    CONSTR_ID = 1048


@dataclass()
class Liquidate(PlutusData):
    CONSTR_ID = 1049


# We can lock or redeem our own collateral or liquidate someone else's
CollateralRedeemer = Union[Redeem, Liquidate]


def check_signed_by_owner(datum: CollateralDatum, context: ScriptContext) -> bool:
    """Check if the transaction is signed by the collateral owner"""
    return datum.owner in context.tx_info.signatories


def minted_amount(datum: CollateralDatum, context: ScriptContext) -> int:
    """Amount of stablecoins minted in this transaction"""
    minted = context.tx_info.mint
    return minted.get(datum.minting_policy_id, {b"": 0}).get(STABLECOIN_TOKEN_NAME, 0)


def check_stablecoin_amount(datum: CollateralDatum, context: ScriptContext) -> bool:
    """Check that the amount of stablecoins burned matches the amont at the collateral's datum"""
    return -datum.stable_coin_amount == minted_amount(datum, context)


def validator(datum: CollateralDatum, r: CollateralRedeemer, context: ScriptContext):
    if isinstance(r, Redeem):
        assert check_signed_by_owner(
            datum, context
        ), "collateral owner's signature missing"
        assert check_stablecoin_amount(
            datum, context
        ), "burned stablecoin amount mismatch"
    elif isinstance(r, Liquidate):
        assert check_stablecoin_amount(
            datum, context
        ), "burned stablecoin amount mismatch"
