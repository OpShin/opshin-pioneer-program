from opshin.prelude import *


STABLECOIN_TOKEN_NAME = b"USDP"


CurrencySymbol = bytes


@dataclass()
class CollateralDatum(PlutusData):
    minting_policy_id: CurrencySymbol
    owner: PubKeyHash
    stable_coin_amount: int


def parse_collateral_datum_unsafe(o: TxOut, info: TxInfo) -> CollateralDatum:
    datum: CollateralDatum = resolve_datum_unsafe(o, info)
    return datum


# Oracle Datum
Rate = int


def parse_oracle_datum_unsafe(o: TxOut, info: TxInfo) -> int:
    datum: Rate = resolve_datum_unsafe(o, info)
    return datum
