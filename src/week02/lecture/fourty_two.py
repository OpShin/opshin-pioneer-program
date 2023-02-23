from eopsin.prelude import *

# `isinstance` is not available yet: https://github.com/ImperatorLang/eopsin/issues/44
# def validator(datum: BuiltinData, redeemer: BuiltinData, context: BuiltinData) -> None:
#     assert isinstance(redeemer, int) and redeemer == 42


def validator(datum: BuiltinData, redeemer: int, context: BuiltinData) -> None:
    assert redeemer == 42
