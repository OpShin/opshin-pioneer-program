import pytest
from pytest_mock import MockerFixture

import src.utils.network
import src.week02.scripts.build
import src.week02.scripts.collect_gift
import src.week02.scripts.make_gift
import src.week02.scripts.send
from src.utils.mock import MockChainContext, MockUser
from src.utils.mock_scripts import mock_context, run_script


@pytest.fixture(scope="module", autouse=True)
def test_build():
    src.week02.scripts.build.main()


def test_send(mocker: MockerFixture):
    context = MockChainContext()
    u1 = MockUser(context)
    u1.fund(10_000_000)
    u2 = MockUser(context)
    users = {"u1": u1, "u2": u2}
    mock = mock_context(mocker, "src.week02.scripts.send", context, users)

    run_script(
        mocker, src.week02.scripts.send, args=["u1", "u2", "--amount", "5000000"]
    )

    mock.assert_called_once()
    assert u1.balance().coin <= 5000000
    assert u2.balance().coin == 5000000


@pytest.mark.parametrize(
    "script", ["burn", "custom_types", "fourty_two", "fourty_two_typed", "gift"]
)
def test_gift(mocker: MockerFixture, script: str):
    # setup chain
    context = MockChainContext()
    u1 = MockUser(context)
    u1.fund(10_000_000)
    u2 = MockUser(context)
    u2.fund(5_000_000)  # add collateral
    users = {"u1": u1, "u2": u2}
    # test make_gift.py
    mock = mock_context(mocker, "src.week02.scripts.make_gift", context, users)
    run_script(
        mocker,
        src.week02.scripts.make_gift,
        args=["u1", "--amount", "5000000", "--script", script],
    )
    mock.assert_called_once()
    # test collect_gift.py
    mock = mock_context(mocker, "src.week02.scripts.collect_gift", context, users)
    try:
        run_script(
            mocker, src.week02.scripts.collect_gift, args=["u2", "--script", script]
        )
    except ValueError as e:
        if script != "burn":
            raise e
    mock.assert_called_once()
