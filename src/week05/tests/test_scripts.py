import pytest
from pytest_mock import MockerFixture

import src.week05.scripts.build
import src.week05.scripts.mint
from src.utils.mock import MockChainContext, MockUser
from src.utils.mock_scripts import mock_context, run_script


@pytest.fixture(scope="module", autouse=True)
def test_build():
    src.week05.scripts.build.main()


@pytest.mark.parametrize("script", ["free", "nft", "signed"])
def test_mint(mocker: MockerFixture, script: str):
    # setup chain
    context = MockChainContext()
    u1 = MockUser(context)
    u1.fund(10_000_000)
    users = {"u1": u1}

    # test mint
    mock = mock_context(mocker, "src.week05.scripts.mint", context, users)
    run_script(
        mocker,
        src.week05.scripts.mint,
        args=["u1", "token", "--amount", "1", "--script", script],
    )
    mock.assert_called_once()

    assert u1.balance().multi_asset

    if script == "nft":
        return

    # test burn
    mock = mock_context(mocker, "src.week05.scripts.mint", context, users)
    run_script(
        mocker,
        src.week05.scripts.mint,
        args=["u1", "token", "--amount", "-1", "--script", script],
    )
    mock.assert_called_once()

    assert u1.balance().multi_asset.count(lambda p, an, a: a > 0) == 0
