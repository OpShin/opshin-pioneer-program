from opshin.prelude import *


@dataclass()
class DatumSwap(PlutusData):
    beneficiary: PubKeyHash
    price: int


def validator(datum: DatumSwap, redeemer: None, context: ScriptContext):
    tx_info = context.tx_info
    count = 0
    for txin in tx_info.inputs:
        d = txin.resolved.datum
        if isinstance(d, SomeOutputDatum):
            count += 1
        if isinstance(d, SomeOutputDatumHash):
            count += 1
    assert count == 1, "You can only include 1 uxto with a datum."
    paid = False
    for output in tx_info.outputs:
        payment_cred: PubKeyCredential = output.address.payment_credential
        if payment_cred.credential_hash == datum.beneficiary:
            value_paid = output.value
            ada_payed = value_paid.get(b"", {b"": 0}).get(b"", 0)
            if ada_payed == datum.price:
                paid = True
    assert paid, "Hey! You have to pay the owner!"
