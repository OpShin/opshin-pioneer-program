from opshin.prelude import *


CurrencySymbol = bytes


@dataclass()
class CollateralDatum(PlutusData):
    """Datum containing all the relevant information"""

    minting_policy_id: CurrencySymbol
    owner: PubKeyHash
    stable_coin_amount: int


STABLECOIN_TOKEN_NAME = b"USDP"


def parse_collateral_datum_unsafe(o: TxOut, info: TxInfo) -> CollateralDatum:
    datum: CollateralDatum = resolve_datum_unsafe(o, info)
    return datum


@dataclass()
class AssetClass(PlutusData):
    currency_symbol: bytes
    token_name: bytes


@dataclass()
class OracleParams(PlutusData):
    oracle_nft: AssetClass
    oracle_operator: PubKeyHash


# Oracle Datum
Rate = int


def parse_oracle_datum_unsafe(o: TxOut, info: TxInfo) -> int:
    datum: Rate = resolve_datum_unsafe(o, info)
    return datum
