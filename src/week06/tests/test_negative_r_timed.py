import hypothesis
import hypothesis.strategies as st
from opshin import build

from src.utils import network
from src.utils.mock import MockChainContext, MockUser
from src.week06.lecture.negative_r_timed import validator, CustomDatum
import opshin.prelude
import datetime
import pycardano
from src.week06 import lecture_dir


def make_mock_context(
    valid_range: opshin.prelude.POSIXTimeRange,
):
    tx_info = opshin.prelude.TxInfo(
        inputs=None,
        reference_inputs=None,
        outputs=None,
        fee=None,
        mint=None,
        dcert=None,
        wdrl=None,
        valid_range=valid_range,
        signatories=None,
        redeemers=None,
        data=None,
        id=None,
    )
    context = opshin.prelude.ScriptContext(tx_info=tx_info, purpose=None)
    return context


@hypothesis.given(
    dt=st.datetimes(max_value=datetime.datetime(year=3000, month=1, day=1)),
    redeemer=st.integers(),
)
def test_property_before_fails(dt: datetime.datetime, redeemer: int):
    deadline: opshin.prelude.POSIXTime = int(
        dt.timestamp() * 1000
    )  # plutus contracts uses milliseconds
    run(CustomDatum(deadline), redeemer)


def setup_user(context: MockChainContext):
    user = MockUser(context)
    user.fund(1000000000)  # 100 ADA
    return user


def run(datum, redeemer_data, *args):
    mock_chain_context = MockChainContext()
    # SETUP USERS
    u1 = setup_user(mock_chain_context)
    u2 = setup_user(mock_chain_context)
    # build script
    plutus_script = build(lecture_dir.joinpath("negative_r_timed.py"), *args)
    script_hash = pycardano.plutus_script_hash(plutus_script)
    script_address = pycardano.Address(script_hash, network=network)

    # USER 1 LOCKS 100 Lovelaces ("val") IN VALIDATOR
    val = pycardano.Value(coin=2000000)  # 2 ADA
    tx_builder = pycardano.TransactionBuilder(mock_chain_context)
    tx_builder.add_input_address(u1.address)
    tx_builder.add_output(
        pycardano.TransactionOutput(
            script_address, amount=val, datum=datum, script=plutus_script
        )
    )
    tx = tx_builder.build_and_sign([u1.signing_key], change_address=u1.address)
    mock_chain_context.submit_tx_mock(tx)

    # WAIT FOR A BIT
    mock_chain_context.wait(1000)

    # USER 2 TAKES "val" FROM VALIDATOR
    utxo = mock_chain_context.utxos(str(script_address))[0]
    tx_builder = pycardano.TransactionBuilder(mock_chain_context)
    tx_builder.add_script_input(
        utxo,
        redeemer=pycardano.Redeemer(
            redeemer_data,
        ),
        script=plutus_script,
    )
    tx_builder.collaterals.append(mock_chain_context.utxos(str(u2.address))[0])
    # mock_chain_context.evaluate_scripts(tx_builder)  # TODO: fix evaluation errors here
    tx = tx_builder.build_and_sign([u2.signing_key], change_address=u2.address)
    mock_chain_context.submit_tx_mock(tx)


if __name__ == "__main__":
    run(CustomDatum(1000), -1)
