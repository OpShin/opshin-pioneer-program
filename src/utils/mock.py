from collections import defaultdict
from typing import Dict, List, Union, Optional

import pycardano
from pycardano import *

from src.utils.protocol_params import (
    DEFAULT_PROTOCOL_PARAMETERS,
    DEFAULT_GENESIS_PARAMETERS,
)
from src.utils.tx_tools import (
    evaluate_script,
    generate_script_contexts_resolved,
)


class MockChainContext(ChainContext):
    def __init__(
        self,
        protocol_param: Optional[ProtocolParameters] = None,
        genesis_param: Optional[GenesisParameters] = None,
    ):
        self._protocol_param = (
            protocol_param if protocol_param else DEFAULT_PROTOCOL_PARAMETERS
        )
        self._genesis_param = (
            genesis_param if genesis_param else DEFAULT_GENESIS_PARAMETERS
        )
        self._utxo_state: Dict[str, List[UTxO]] = defaultdict(list)
        self._address_lookup: Dict[UTxO, str] = {}
        self._utxo_from_txid: Dict[TransactionId, Dict[int, UTxO]] = defaultdict(dict)
        self._network = Network.TESTNET
        self._epoch = 0
        self._last_block_slot = 0

    @property
    def protocol_param(self) -> ProtocolParameters:
        return self._protocol_param

    @property
    def genesis_param(self) -> GenesisParameters:
        return self._genesis_param

    @property
    def network(self) -> Network:
        return self._network

    @property
    def epoch(self) -> int:
        return self._epoch

    @property
    def last_block_slot(self) -> int:
        return self._last_block_slot

    def utxos(self, address: str) -> List[UTxO]:
        return self._utxo_state.get(address, [])

    def add_utxo(self, utxo: UTxO):
        address = str(utxo.output.address)
        self._utxo_state[address].append(utxo)
        self._address_lookup[utxo] = address
        self._utxo_from_txid[utxo.input.transaction_id][utxo.input.index] = utxo

    def get_address(self, utxo: UTxO) -> str:
        return self._address_lookup[utxo]

    def remove_utxo(self, utxo: UTxO):
        del self._utxo_from_txid[utxo.input.transaction_id][utxo.input.index]
        address = self._address_lookup[utxo]
        del self._address_lookup[utxo]
        i = self._utxo_state[address].index(utxo)
        self._utxo_state[address].pop(i)

    def get_utxo_from_txid(self, transaction_id: TransactionId, index: int) -> UTxO:
        return self._utxo_from_txid[transaction_id][index]

    def submit_tx(self, cbor: Union[bytes, str]):
        self.evaluate_tx(cbor)
        self.submit_tx_mock(Transaction.from_cbor(cbor))

    def submit_tx_mock(self, tx: Transaction):
        for input in tx.transaction_body.inputs:
            utxo = self.get_utxo_from_txid(input.transaction_id, input.index)
            self.remove_utxo(utxo)
        for i, output in enumerate(tx.transaction_body.outputs):
            utxo = UTxO(TransactionInput(tx.id, i), output)
            self.add_utxo(utxo)

    def evaluate_tx(self, cbor: Union[bytes, str]) -> Dict[str, ExecutionUnits]:
        tx = Transaction.from_cbor(cbor)
        input_utxos = [
            self.get_utxo_from_txid(input.transaction_id, input.index)
            for input in tx.transaction_body.inputs
        ]
        ref_input_utxos = (
            [
                self.get_utxo_from_txid(input.transaction_id, input.index)
                for input in tx.transaction_body.reference_inputs
            ]
            if tx.transaction_body.reference_inputs is not None
            else []
        )
        script_invocations = generate_script_contexts_resolved(
            tx, input_utxos, ref_input_utxos
        )
        ret = {}
        for invocation in script_invocations:
            redeemer = invocation.redeemer
            if redeemer.ex_units.steps <= 0 and redeemer.ex_units.mem <= 0:
                redeemer.ex_units = ExecutionUnits(
                    self.protocol_param.max_tx_ex_mem,
                    self.protocol_param.max_tx_ex_steps,
                )
            (suc, err), (cpu, mem) = evaluate_script(invocation)
            if err:
                raise ValueError(err)
            key = f"{redeemer.tag.name.lower()}:{redeemer.index}"
            ret[key] = ExecutionUnits(mem, cpu)
        return ret

    def wait(self, slots):
        self._last_block_slot += slots


class MockUser:
    def __init__(self, context: MockChainContext):
        self.context = context
        self.signing_key = pycardano.PaymentSigningKey.generate()
        self.verification_key = pycardano.PaymentVerificationKey.from_signing_key(
            self.signing_key
        )
        self.network = pycardano.Network.TESTNET
        self.address = pycardano.Address(
            payment_part=self.verification_key.hash(), network=self.network
        )

    def fund(self, amount: int):
        self.context.add_utxo(
            # not sure what the correct genesis transaction is
            UTxO(
                TransactionInput(TransactionId(self.verification_key.payload), 0),
                TransactionOutput(self.address, Value(coin=amount)),
            ),
        )

    def utxos(self):
        return self.context.utxos(str(self.address))
