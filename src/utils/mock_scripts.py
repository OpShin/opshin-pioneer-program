from types import ModuleType
from typing import Dict, Optional

from pytest_mock import MockerFixture

from src.utils.mock import MockChainContext, MockUser


def mock_context(
    mocker: MockerFixture,
    script_module: str,
    context: MockChainContext,
    users: Dict[str, MockUser],
):
    mock = mocker.patch(f"{script_module}.get_chain_context", return_value=context)

    def get_address(name: str):
        return users[name].address

    mocker.patch(f"{script_module}.get_address", get_address)

    def get_signing_info(name: str):
        u = users[name]
        return u.verification_key, u.signing_key, u.address

    mocker.patch(f"{script_module}.get_signing_info", get_signing_info)
    return mock


def run_script(
    mocker: MockerFixture, script_module: ModuleType, args: Optional[list] = None
):
    if args is None:
        args = []
    mocker.patch("sys.argv", [script_module.__file__, *args])
    try:
        script_module.main()
    except SystemExit as e:
        if e.code != 0:
            raise e
