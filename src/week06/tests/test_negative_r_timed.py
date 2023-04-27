import hypothesis
import hypothesis.strategies as st
import pycardano
import pytest
from opshin import build

from src.utils import network
from src.utils.mock import MockChainContext, MockUser
from src.week06 import lecture_dir
from src.week06.lecture.negative_r_timed import CustomDatum

from src.week06.lecture import negative_r_timed


@pytest.mark.parametrize(
    ["d", "r", "validates"],
    [
        [50, -42, True],
        [50, 0, True],
        [50, 42, False],
        [5000, -42, False],
        [5000, 0, False],
        [5000, 42, False],
    ],
)
def test_unit(d: int, r: int, validates: bool):
    if validates:
        run(d, r)
    else:
        run_fails(d, r)


@hypothesis.given(
    d=st.integers(min_value=1002),
    r=st.integers(),
)
def test_property_before_fails(d: int, r: int):
    """All redeemers fail before deadline."""
    run_fails(d, r)


@hypothesis.given(
    d=st.integers(min_value=0, max_value=998),
    r=st.integers(min_value=1),
)
def test_property_positive_after_fails(d: int, r: int):
    """Positive redeemer always fail after deadline."""
    run_fails(d, r)


@hypothesis.given(
    d=st.integers(min_value=0, max_value=998),
    r=st.integers(max_value=0),
)
def test_property_negative_after_succeeds(d: int, r: int):
    """Negative redeemers always succeed after deadline."""
    run(d, r)


def run_fails(d, r):
    try:
        run(d, r)
        errored = False
    except ValueError:
        errored = True
    assert errored


def setup_user(context: MockChainContext):
    user = MockUser(context)
    user.fund(100000000)  # 100 ADA
    return user


# build script once outside test function
plutus_script = build(lecture_dir.joinpath("negative_r_timed.py"))
script_hash = pycardano.plutus_script_hash(plutus_script)
script_address = pycardano.Address(script_hash, network=network)


def run(deadline_slot: int, redeemer_data: int):
    mock_chain_context = MockChainContext()
    mock_chain_context.opshin_scripts[plutus_script] = negative_r_timed
    # setup users
    u1 = setup_user(mock_chain_context)
    u2 = setup_user(mock_chain_context)
    # create datum
    deadline_posix = mock_chain_context.posix_from_slot(deadline_slot) * 1000
    datum = CustomDatum(deadline_posix)

    # user 1 locks 2 ADA ("val") in validator
    val = pycardano.Value(coin=5000000)  # 5 ADA
    tx_builder = pycardano.TransactionBuilder(mock_chain_context)
    tx_builder.add_input_address(u1.address)
    tx_builder.add_output(
        pycardano.TransactionOutput(script_address, amount=val, datum=datum)
    )
    tx = tx_builder.build_and_sign([u1.signing_key], change_address=u1.address)
    mock_chain_context.submit_tx(tx)

    # wait for a bit
    mock_chain_context.wait(1000)

    # user 2 takes "val" from validator - fees
    utxo = mock_chain_context.utxos(script_address)[0]
    tx_builder = pycardano.TransactionBuilder(mock_chain_context)
    tx_builder.add_input_address(u2.address)
    tx_builder.add_script_input(
        utxo,
        redeemer=pycardano.Redeemer(
            redeemer_data,
        ),
        script=plutus_script,
    )
    tx_builder.validity_start = mock_chain_context.last_block_slot
    tx_builder.ttl = tx_builder.validity_start + 1


    tx = tx_builder.build_and_sign([u2.signing_key], change_address=u2.address)
    mock_chain_context.submit_tx(tx)


if __name__ == "__main__":
    run(1000, -1)
