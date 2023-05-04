from typing import List

import pycardano

from src.utils.mock import MockChainContext, MockUser


def setup_users(context: MockChainContext) -> List[MockUser]:
    users = []
    for _ in range(3):
        u = MockUser(context)
        u.fund(10_000_000)  # 10 ADA
        users.append(u)
    return users


def send_value(
    context: MockChainContext, u1: MockUser, value: pycardano.Value, u2: MockUser
):
    builder = pycardano.TransactionBuilder(context)
    builder.add_input_address(u1.address)
    builder.add_output(pycardano.TransactionOutput(u2.address, value))
    tx = builder.build_and_sign([u1.signing_key], change_address=u1.address)
    context.submit_tx(tx)
    return context


def test_simple_spend():
    # Create the mock pycardano chain context
    context = MockChainContext()
    # Create 3 users and assign each 10 ADA
    users = setup_users(context)
    # Send 1 ADA from user 0 to user 1
    send_value(context, users[0], pycardano.Value(coin=1_000_000), users[1])
    # Send 1 ADA from user 1 to user 2
    send_value(context, users[1], pycardano.Value(coin=1_000_000), users[2])


def test_not_enough_funds():
    context = MockChainContext()
    users = setup_users(context)
    # Send 100 ADA from user 0 to user 1
    try:
        send_value(context, users[0], pycardano.Value(coin=100_000_000), users[1])
        validates = True
    except pycardano.UTxOSelectionException:
        validates = False
    assert not validates, "transaction must fail"
