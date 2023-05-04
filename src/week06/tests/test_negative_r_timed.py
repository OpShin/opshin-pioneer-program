from copy import deepcopy
from functools import cache

import hypothesis
import hypothesis.strategies as st
import pycardano
import pytest
from opshin import build

from src.utils import network
from src.utils.mock import MockChainContext, MockUser
from src.week06 import lecture_dir
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


@hypothesis.settings(deadline=None)
@hypothesis.given(
    d=st.integers(min_value=1002),
    r=st.integers(),
)
def test_property_before_fails(d: int, r: int):
    """All redeemers fail before deadline."""
    run_fails(d, r)


@hypothesis.settings(deadline=None)
@hypothesis.given(
    d=st.integers(min_value=0, max_value=998),
    r=st.integers(min_value=1),
)
def test_property_positive_after_fails(d: int, r: int):
    """Positive redeemer always fail after deadline."""
    run_fails(d, r)


@hypothesis.settings(deadline=None)
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
    except (ValueError, AssertionError):
        errored = True
    assert errored


def setup_user(context: MockChainContext):
    user = MockUser(context)
    user.fund(100000000)  # 100 ADA
    return user


@cache
def setup_context():
    context = MockChainContext()
    # enable opshin validator debugging
    context.opshin_scripts[plutus_script] = negative_r_timed.validator
    return context, setup_user(context), setup_user(context)


# build script once outside our test functions
plutus_script = build(lecture_dir.joinpath("negative_r_timed.py"))
script_hash = pycardano.plutus_script_hash(plutus_script)
script_address = pycardano.Address(script_hash, network=network)


def lock(context: MockChainContext, u1: MockUser, deadline_slot: int):
    deadline_posix = context.posix_from_slot(deadline_slot) * 1000
    datum = negative_r_timed.CustomDatum(deadline_posix)

    val = pycardano.Value(coin=5000000)  # 5 ADA
    tx_builder = pycardano.TransactionBuilder(context)
    tx_builder.add_input_address(u1.address)
    tx_builder.add_output(
        pycardano.TransactionOutput(script_address, amount=val, datum=datum)
    )
    tx = tx_builder.build_and_sign([u1.signing_key], change_address=u1.address)
    context.submit_tx(tx)
    return context


def unlock(context: MockChainContext, u2: MockUser, redeemer_data: int):
    utxo = context.utxos(script_address)[0]
    tx_builder = pycardano.TransactionBuilder(context)
    tx_builder.add_input_address(u2.address)
    tx_builder.add_script_input(
        utxo,
        redeemer=pycardano.Redeemer(
            redeemer_data,
        ),
        script=plutus_script,
    )
    tx_builder.validity_start = context.last_block_slot
    tx_builder.ttl = tx_builder.validity_start + 1

    tx = tx_builder.build_and_sign([u2.signing_key], change_address=u2.address)
    context.submit_tx(tx)
    return context


def run(deadline_slot: int, redeemer_data: int):
    # setup context and users
    # needs deepcopy so state starts fresh each run
    context, u1, u2 = deepcopy(setup_context())

    # user 1 locks 2 ADA ("val") in validator
    context = lock(context, u1, deadline_slot)

    # wait for a bit
    context.wait(1000)

    # user 2 takes "val" from validator - fees
    unlock(context, u2, redeemer_data)


if __name__ == "__main__":
    run(1000, -1)
