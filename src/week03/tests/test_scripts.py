import time

import pytest
from pytest_mock import MockerFixture

import src.week03.scripts.build
import src.week03.scripts.collect_vest
import src.week03.scripts.make_vest
from src.utils.mock import MockChainContext, MockUser
from src.utils.mock_scripts import mock_context, run_script


@pytest.fixture(scope="module", autouse=True)
def test_build():
    src.week03.scripts.build.main()


@pytest.mark.parametrize("parameterized", [True, False])
def test_vest(mocker: MockerFixture, parameterized: bool):
    # setup chain
    context = MockChainContext()
    u1 = MockUser(context)
    u1.fund(10_000_000)
    u2 = MockUser(context)
    u2.fund(5_000_000)  # add collateral
    users = {"u1": u1, "u2": u2}

    # wait until current time slot
    context.wait(context.slot_from_posix(int(time.time())))

    # test make_vest.py
    if parameterized:
        args = ["--parameterized"]
    else:
        args = []
    mock = mock_context(mocker, "src.week03.scripts.make_vest", context, users)
    run_script(
        mocker,
        src.week03.scripts.make_vest,
        args=["u1", "u2", "--amount", "5000000", "--wait_time", "100", *args],
    )
    mock.assert_called_once()

    # try to unlock before deadline
    mock = mock_context(mocker, "src.week03.scripts.collect_vest", context, users)
    try:
        run_script(mocker, src.week03.scripts.collect_vest, args=["u2", *args])
        validates = True
    except (AssertionError, ValueError):
        validates = False
    assert not validates
    mock.assert_called_once()

    # wait for deadline
    context.wait(1000)
    mocker.patch("time.time", return_value=time.time() + 1000)

    # test collect_vest.py
    mock = mock_context(mocker, "src.week03.scripts.collect_vest", context, users)
    run_script(mocker, src.week03.scripts.collect_vest, args=["u2", *args])
    mock.assert_called_once()
