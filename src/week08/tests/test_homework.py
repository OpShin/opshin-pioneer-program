import os
from typing import Dict, List

import pytest
from opshin import compiler
from opshin.prelude import (
    Address,
    Certifying,
    DCertDelegRegKey,
    NoOutputDatum,
    NoScriptHash,
    NoStakingCredential,
    PubKeyCredential,
    PubKeyHash,
    Rewarding,
    ScriptContext,
    ScriptCredential,
    StakingCredential,
    StakingHash,
    TxInfo,
    TxOut,
)

from src.week08 import homework_dir
from src.week08.homework import homework

skip = "SKIP_HOMEWORK" in os.environ

python_files = [
    "homework.py",
]
script_paths = [str(homework_dir.joinpath(f)) for f in python_files]


@pytest.mark.parametrize("path", script_paths)
def test_homework_compile(path):
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())


def make_address(pkh: PubKeyHash) -> Address:
    return Address(PubKeyCredential(pkh), NoStakingCredential())


def make_output(addr: Address, lovelace: int) -> TxOut:
    return TxOut(
        address=addr,
        value={b"": {b"": lovelace}},
        datum=NoOutputDatum(),
        reference_script=NoScriptHash(),
    )


def make_context(
    signatories: List[PubKeyHash],
    outputs: List[TxOut],
    withdrawals: Dict[StakingCredential, int],
    purpose,
) -> ScriptContext:
    return ScriptContext(
        tx_info=TxInfo(
            inputs=[],
            reference_inputs=[],
            outputs=outputs,
            fee={},
            mint={},
            dcert=[],
            wdrl=withdrawals,
            valid_range=None,
            signatories=signatories,
            redeemers={},
            data={},
            id=None,
        ),
        purpose=purpose,
    )


def validates(pkh: PubKeyHash, addr: Address, context: ScriptContext) -> bool:
    try:
        homework.validator(pkh, addr, None, context)
        return True
    except AssertionError:
        return False


@pytest.mark.skipif(skip, reason="skip homework tests if not implemented")
@pytest.mark.parametrize(
    ["signatories", "expected"],
    [
        [[b"owner"], True],
        [[], False],
        [[b"someone-else"], False],
    ],
)
def test_certifying_requires_owner_signature(signatories, expected):
    pkh = b"owner"
    addr = make_address(b"recipient")
    stake = StakingHash(ScriptCredential(b"stake"))
    context = make_context(
        signatories=signatories,
        outputs=[],
        withdrawals={},
        purpose=Certifying(DCertDelegRegKey(stake)),
    )
    assert validates(pkh, addr, context) == expected


@pytest.mark.skipif(skip, reason="skip homework tests if not implemented")
@pytest.mark.parametrize(
    ["paid", "expected"],
    [
        [0, False],
        [4_999_999, False],
        [5_000_000, True],
        [6_000_000, True],
    ],
)
def test_rewarding_requires_half_of_all_withdrawals_paid(paid: int, expected: bool):
    pkh = b"owner"
    addr = make_address(b"recipient")
    stake_1 = StakingHash(ScriptCredential(b"stake-1"))
    stake_2 = StakingHash(ScriptCredential(b"stake-2"))
    context = make_context(
        signatories=[pkh],
        outputs=[
            make_output(addr, paid),
            make_output(make_address(b"other"), 10_000_000),
        ],
        withdrawals={stake_1: 7_000_000, stake_2: 3_000_000},
        purpose=Rewarding(stake_1),
    )
    assert validates(pkh, addr, context) == expected


@pytest.mark.skipif(skip, reason="skip homework tests if not implemented")
def test_rewarding_accumulates_multiple_outputs_to_parameter_address():
    pkh = b"owner"
    addr = make_address(b"recipient")
    stake = StakingHash(ScriptCredential(b"stake"))
    context = make_context(
        signatories=[pkh],
        outputs=[
            make_output(addr, 2_000_000),
            make_output(make_address(b"other"), 100_000_000),
            make_output(addr, 3_000_000),
        ],
        withdrawals={stake: 10_000_000},
        purpose=Rewarding(stake),
    )
    assert validates(pkh, addr, context)


@pytest.mark.skipif(skip, reason="skip homework tests if not implemented")
def test_rewarding_still_requires_owner_signature():
    pkh = b"owner"
    addr = make_address(b"recipient")
    stake = StakingHash(ScriptCredential(b"stake"))
    context = make_context(
        signatories=[],
        outputs=[make_output(addr, 10_000_000)],
        withdrawals={stake: 10_000_000},
        purpose=Rewarding(stake),
    )
    assert not validates(pkh, addr, context)
