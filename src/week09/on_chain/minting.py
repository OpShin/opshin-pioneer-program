from src.week09.on_chain.common import *


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


# -------- ORACLE-RELATED FUNCTIONS ------------


def script_hash_address(vh: PubKeyHash) -> Address:
    """The address that should be used by a transaction output locked by the given validator script hash."""
    return Address(PubKeyCredential(vh), NoStakingCredential())


def get_oracle_input(mp: MintParams, context: ScriptContext) -> TxOut:
    """Get the oracle's input"""
    # TODO: add reference inputs with list concatenation workaround
    outputs = [
        i.resolved
        for i in context.tx_info.inputs  # + context.tx_info.reference_inputs
        if i.resolved.address == script_hash_address(mp.oracle_validator)
    ]
    assert len(outputs) == 1, "expected exactly one oracle input"
    return outputs[0]


def rate(mp: MintParams, context: ScriptContext) -> int:
    return parse_oracle_datum_unsafe(get_oracle_input(mp, context), context.tx_info)


# --------- COLLATERAL-RELATED FUNCTIONS ------------


@dataclass()
class CollateralOutput(PlutusData):
    datum: CollateralDatum
    value: Value


def collateral_output(mp: MintParams, context: ScriptContext) -> CollateralOutput:
    """Get the collateral's output datum and value"""

    def correct_addr(addr: Address) -> bool:
        staking_cred = addr.staking_credential
        result = False
        if isinstance(staking_cred, NoStakingCredential):
            payment_cred = addr.payment_credential
            if payment_cred.credential_hash == mp.collateral_validator:
                result = True
        return result

    def get_collateral_output(output: TxOut) -> CollateralOutput:
        datum = parse_collateral_datum_unsafe(output, context.tx_info)
        return CollateralOutput(datum, output.value)

    outputs = [
        get_collateral_output(output)
        for output in context.tx_info.outputs
        if correct_addr(output.address)
    ]
    assert len(outputs) == 1, "expected exactly one collateral output"
    return outputs[0]


def collateral_output_datum(output: CollateralOutput) -> CollateralDatum:
    """Get the collateral's output datum"""
    return output.datum


def collateral_output_amount(output: CollateralOutput) -> int:
    """Get the collateral's output amount as an integer"""
    return output.value[b""][b""]


def collateral_input(mp: MintParams, context: ScriptContext) -> TxOut:
    """Get the collateral's input"""
    # TODO: add reference inputs with list concatenation workaround
    outputs = [
        i.resolved
        for i in context.tx_info.inputs  # + context.tx_info.reference_inputs
        if i.resolved.address == script_hash_address(mp.collateral_validator)
    ]
    assert len(outputs) == 1, "expected exactly one oracle input"
    return outputs[0]


def collateral_input_datum(
    context: ScriptContext, collateral_inp: TxOut
) -> CollateralDatum:
    """Get the collateral's input datum"""
    return parse_collateral_datum_unsafe(collateral_inp, context.tx_info)


def collateral_input_amount(collateral_inp: TxOut) -> int:
    """Get the collateral's input amount"""
    return collateral_inp.value[b""][b""]


# --------- MINTING-RELATED FUNCTIONS ------------


def minted_amount(context: ScriptContext) -> int:
    """Get amount of stablecoins to minted (or burned if negative) in this transaction"""
    minted = context.tx_info.mint
    purpose: Minting = context.purpose
    return minted.get(purpose.policy_id, {b"": 0}).get(STABLECOIN_TOKEN_NAME, 0)


def check_mint_positive(minted_amt: int) -> bool:
    """Check that the amount of stablecoins minted is positive"""
    return minted_amt > 0


def check_burn_negative(minted_amt: int) -> bool:
    """Check that the amount of stablecoins minted is negative"""
    return minted_amt < 0


def max_mint(mp: MintParams, context: ScriptContext, collateral_amount: int) -> int:
    """
    max_mint calculates the maximum amount of stablecoins that can be minted with the given collateral.

    Oracle has ada price in USD cents [USD¢] ($1 is ¢100 in the oracle's datum). So rate needs to be divided by 100.
    Also, collateral_output_amount is in lovelaces [L], so final calculation needs to be divided by 1_000_000.

    ca = collateral_amount
    CMP = mp.collateral_min_percent


                      ca [L]        rate [USD¢/ADA]                 ca [L]
                 --------------- * ------------------           --------------- * rate [USD/ADA]
                      CMP [%]        100 [USD¢/USD]                   CMP
                    ---------
                      100 [%]
    max_mint = ------------------------------------------ =  ------------------------------------- = [USD]
                        1_000_000 [L/A]                                1_000_000 [L/A]
    """
    return (
        collateral_amount // mp.collateral_min_percent * rate(mp, context)
    ) // 1_000_000


def check_max_mint_out(
    mp: MintParams,
    context: ScriptContext,
    collateral_out: CollateralOutput,
    minted_amt: int,
) -> bool:
    """Check that the amount of stablecoins minted does not exceed the maximum"""
    return max_mint(mp, context, collateral_output_amount(collateral_out)) >= minted_amt


def check_datum(
    minted_amt: int, context: ScriptContext, collateral_out: CollateralOutput
) -> bool:
    """Check that the collateral's output datum has the correct values"""
    datum = collateral_output_datum(collateral_out)

    purpose: Minting = context.purpose
    own_currency_symbol = purpose.policy_id
    return (
        datum.minting_policy_id == own_currency_symbol
        and datum.stable_coin_amount == minted_amt
        and datum.owner in context.tx_info.signatories
    )


def check_burn_amount_matches_col_datum(
    datum: CollateralDatum, minted_amt: int
) -> bool:
    """Check that the amount of stablecoins burned matches the amont at the collateral's datum"""
    return -datum.stable_coin_amount == minted_amt


def check_col_owner(datum: CollateralDatum, context: ScriptContext) -> bool:
    """Check that the owner's signature is present"""
    return datum.owner in context.tx_info.signatories


def check_liquidation(
    mp: MintParams, context: ScriptContext, collateral_inp: TxOut, minted_amt: int
) -> bool:
    """Check that the collateral's value is low enough to liquidate"""
    return max_mint(mp, context, collateral_input_amount(collateral_inp)) < -minted_amt


# ---------------------------------------------------------------------------------------------------
# ------------------------------------ ON-CHAIN: VALIDATOR ------------------------------------------


def validator(mp: MintParams, r: MintRedeemer, context: ScriptContext):
    minted_amt = minted_amount(context)
    if isinstance(r, Mint):
        collateral_out = collateral_output(mp, context)
        assert check_mint_positive(minted_amt), "minted amount must be positive"
        assert check_max_mint_out(
            mp, context, collateral_out, minted_amt
        ), "minted amount exceeds max"
        assert check_datum(
            minted_amt, context, collateral_out
        ), "invalid datum at collateral output"
    elif isinstance(r, Burn):
        datum = collateral_input_datum(context, collateral_input(mp, context))
        assert check_burn_amount_matches_col_datum(
            datum, minted_amt
        ), "invalid burning amount"
        assert check_col_owner(datum, context), "owner's signature missing"
        assert check_burn_negative(minted_amt), "Minting instead of burning!"
    elif isinstance(r, Liquidate):
        collateral_inp = collateral_input(mp, context)
        datum = collateral_input_datum(context, collateral_inp)
        assert check_burn_amount_matches_col_datum(
            datum, minted_amt
        ), "invalid liquidating amount"
        assert check_liquidation(
            mp, context, collateral_inp, minted_amt
        ), "liquidation threshold not reached"
        assert check_burn_negative(minted_amt), "Minting instead of burning!"
