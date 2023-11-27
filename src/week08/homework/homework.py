from opshin.prelude import *


# A staking validator with two parameters, a pubkey hash and an address. The validator
# should work as follows:
# 1. The given pubkey hash needs to sign all transactions involving this validator.
# 2. The given address needs to receive at least half of all withdrawn rewards.
def validator(pkh: PubKeyHash, addr: Address, _: None, context: ScriptContext):
    pass
