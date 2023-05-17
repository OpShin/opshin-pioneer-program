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

STABLECOIN_TOKEN_NAME = b"USDP"


def check_signed_by_owner(datum: CollateralDatum, context: ScriptContext) -> bool:
    return datum.owner in context.tx_info.signatories


def minted_amount(datum: CollateralDatum, context: ScriptContext) -> int:
    minted = context.tx_info.mint
    return minted.get(datum.minting_policy_id, {b"": 0}).get(STABLECOIN_TOKEN_NAME, 0)


def check_stablecoin_amount(datum: CollateralDatum, context: ScriptContext) -> bool:
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
