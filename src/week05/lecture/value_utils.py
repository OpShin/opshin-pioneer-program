from opshin.prelude import *


EMTPY_TOKENNAME_DICT: Dict[bytes, int] = {}
EMPTY_VALUE_DICT: Value = {}


def token_value(token: Token, amount: int) -> Value:
    return {token.policy_id: {token.token_name: amount}}


def amount_of_token_in_value(
    token: Token,
    value: Value,
) -> int:
    return value.get(token.policy_id, {b"": 0}).get(token.token_name, 0)


def merge_without_duplicates(a: List[bytes], b: List[bytes]) -> List[bytes]:
    """
    Merge two lists without duplicates
    """
    return [x for x in a if not x in b] + b


def _add_token_names(
    a: Dict[TokenName, int], b: Dict[TokenName, int]
) -> Dict[TokenName, int]:
    """
    Add b to a, return a + b
    """
    if not a:
        return b
    if not b:
        return a
    return {
        tn: a.get(tn, 0) + b.get(tn, 0)
        for tn in merge_without_duplicates(list(a.keys()), list(b.keys()))
    }


def add_value(a: Value, b: Value) -> Value:
    """
    Add b to a, return a + b
    """
    if not a:
        return b
    if not b:
        return a
    return {
        pid: _add_token_names(
            a.get(pid, EMTPY_TOKENNAME_DICT), b.get(pid, EMTPY_TOKENNAME_DICT)
        )
        for pid in merge_without_duplicates(list(a.keys()), list(b.keys()))
    }


def _subtract_token_names(
    a: Dict[TokenName, int], b: Dict[TokenName, int]
) -> Dict[TokenName, int]:
    """
    Subtract b from a, return a - b
    """
    if not b:
        return a
    elif not a:
        return {tn_amount[0]: -tn_amount[1] for tn_amount in b.items()}
    return {
        tn: a.get(tn, 0) - b.get(tn, 0)
        for tn in merge_without_duplicates(list(a.keys()), list(b.keys()))
    }


def subtract_value(a: Value, b: Value) -> Value:
    """
    Subtract b from a, return a - b
    """
    if not b:
        return a
    elif not a:
        return {
            pid_tokens[0]: {
                tn_amount[0]: -tn_amount[1] for tn_amount in pid_tokens[1].items()
            }
            for pid_tokens in b.items()
        }
    return {
        pid: _subtract_token_names(
            a.get(pid, EMTPY_TOKENNAME_DICT), b.get(pid, EMTPY_TOKENNAME_DICT)
        )
        for pid in merge_without_duplicates(list(a.keys()), list(b.keys()))
    }
