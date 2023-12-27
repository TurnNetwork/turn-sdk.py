import copy
import json
from typing import (
    Optional,
    Any,
    cast,
    TYPE_CHECKING,
)

import rlp
from hexbytes import HexBytes

from eth_typing import (
    HexStr, Address, AnyAddress,
)
from eth_utils import (
    remove_0x_prefix,
    combomethod, to_bytes,
)

from bubble.datastructures import MutableAttributeDict
from bubble.inner_contract.error_code import ERROR_CODE
from bubble.module import apply_result_formatters

from bubble._utils.empty import (
    empty,
)
from bubble._utils.rpc_abi import (
    apply_abi_formatters_to_dict,
)
from bubble._utils.transactions import (
    fill_transaction_defaults,
)
from bubble.inner_contract.formatters import (
    INNER_CONTRACT_PARAM_ABIS,
    DEFAULT_PARAM_NORMALIZERS,
    DEFAULT_PARAM_ABIS,
    INNER_CONTRACT_RESULT_FORMATTERS,
    INNER_CONTRACT_EVENT_FORMATTERS,
)
from bubble.types import (
    TxParams,
    BlockIdentifier,
    CallOverrideParams,
    FunctionIdentifier,
    TxReceipt,
    LogReceipt,
    RLPEventData,
)

if TYPE_CHECKING:
    from bubble import Web3


class InnerContract:
    ADDRESS: AnyAddress = None

    # If you want to get the result of the transaction, please set it to True,
    # if you only want to get the transaction hash, please set it to False
    # is_analyze = False

    def __init__(self, web3: "Web3"):
        self.web3: Web3 = web3
        self.function = InnerContractFunction(self.web3, self.ADDRESS)

    @combomethod
    def event(self, fid: FunctionIdentifier):
        return InnerContractEvent(fid)


class InnerContractFunction:
    fid: FunctionIdentifier = None
    kwargs: dict = None

    def __init__(self, web3: "Web3", address: AnyAddress):
        self.web3: Web3 = web3
        self.address: AnyAddress = address

    def __call__(self, func_type: FunctionIdentifier, **kwargs) -> 'InnerContractFunction':
        clone = copy.copy(self)
        clone.fid = func_type
        if kwargs is None:
            clone.kwargs = {}
        else:
            clone.kwargs = copy.copy(kwargs)

        return clone

    def call(self,
             transaction: Optional[TxParams] = None,
             block_identifier: BlockIdentifier = 'latest',
             state_override: Optional[CallOverrideParams] = None,
             ) -> Any:

        if transaction is None:
            call_transaction: TxParams = {}
        else:
            call_transaction = cast(TxParams, dict(**transaction))

        if 'data' in call_transaction:
            raise ValueError("Cannot set data in call transaction")

        if 'to' in call_transaction:
            raise ValueError("Cannot set to address in contract call transaction")

        if self.address:
            call_transaction.setdefault('to', self.address)

        if self.web3.bub.default_account is not empty:
            # type ignored b/c check prevents an empty default_account
            call_transaction.setdefault('from', self.web3.bub.default_account)  # type: ignore

        if 'to' not in call_transaction:
            raise ValueError(
                "Please ensure that this inner contract instance has an address."
            )

        call_transaction['data'] = self._encode_transaction_data()

        return_data = self.web3.bub.call(call_transaction,
                                         block_identifier=block_identifier,
                                         state_override=state_override,
                                         )

        return self._formatter_result(self.fid, return_data)

    def transact(self):
        # todo: wait coding
        pass

    def estimate_gas(self,
                     transaction: Optional[TxParams] = None,
                     block_identifier: Optional[BlockIdentifier] = None
                     ) -> int:
        if transaction is None:
            estimate_transaction: TxParams = {}
        else:
            estimate_transaction = cast(TxParams, dict(**transaction))

        if 'data' in estimate_transaction:
            raise ValueError("Cannot set data in build transaction")

        if 'to' in estimate_transaction:
            raise ValueError("Cannot set to address in contract call build transaction")

        if self.address:
            estimate_transaction.setdefault('to', self.address)

        if 'to' not in estimate_transaction:
            raise ValueError(
                "Please ensure that this inner contract instance has an address."
            )

        estimate_transaction['data'] = self._encode_transaction_data()

        return self.web3.bub.estimate_gas(estimate_transaction, block_identifier)

    def build_transaction(self, transaction: Optional[TxParams] = None) -> TxParams:
        """
        Build the transaction dictionary without sending
        """
        if transaction is None:
            built_transaction: TxParams = {}
        else:
            built_transaction = cast(TxParams, dict(**transaction))

        if 'data' in built_transaction:
            raise ValueError("Cannot set data in build transaction")

        if 'to' in built_transaction:
            raise ValueError("Cannot set to address in contract call build transaction")

        if self.address:
            built_transaction.setdefault('to', self.address)

        if 'to' not in built_transaction:
            raise ValueError(
                "Please ensure that this inner contract instance has an address."
            )

        built_transaction['data'] = self._encode_transaction_data()

        built_transaction = fill_transaction_defaults(self.web3, built_transaction)

        return built_transaction

    def _encode_transaction_data(self) -> HexStr:
        encoded_args = [rlp.encode(self.fid)]

        self.kwargs = self._formatter_param(self.fid, params=self.kwargs)
        if self.kwargs:
            # encodes parameters sequentially
            for key, value in self.kwargs.items():
                if value is None:
                    encoded_args.append(b'')
                else:
                    encoded_args.append(rlp.encode(value))

        return rlp.encode(encoded_args)

    @staticmethod
    def _formatter_param(fid: FunctionIdentifier, params: dict):
        """
        Format parameters so that it can be used correctly during RPC encoding
        """
        params = apply_abi_formatters_to_dict(DEFAULT_PARAM_NORMALIZERS,
                                              DEFAULT_PARAM_ABIS,
                                              params)
        function_abis = INNER_CONTRACT_PARAM_ABIS.get(fid)
        if function_abis:
            return apply_abi_formatters_to_dict(DEFAULT_PARAM_NORMALIZERS, function_abis, params)
        return params

    @staticmethod
    def _formatter_result(fid: FunctionIdentifier, result: Any):
        """
        Format result to make its easier to use
        """
        if type(result) in [bytes, HexBytes]:
            result = MutableAttributeDict.recursive(json.loads(HexBytes(result).decode('utf-8')))

        if 'Code' not in result.keys() or 'Ret' not in result.keys():
            return result

        rets = result.get('Ret')

        if result.get('Code') != 0:
            # todo: Wait bubble resolve the return value issue
            # raise ContractLogicError(rets)
            return rets

        # when rest is empty value, as <''> \ <[]> ...
        if not rets:
            return rets

        function_formatter = INNER_CONTRACT_RESULT_FORMATTERS.get(fid)

        if function_formatter:
            return MutableAttributeDict.recursive(apply_result_formatters(function_formatter, rets))

        return rets


class InnerContractEvent:

    def __init__(self, fid: FunctionIdentifier = None):
        self.formatter = INNER_CONTRACT_EVENT_FORMATTERS.get(fid)

    def process_receipt(self, receipt: TxReceipt) -> RLPEventData:
        # an inner-contract receipt has only one log
        log = receipt['logs'][-1]
        return self._parse_log(log)

    def _parse_log(self, log: LogReceipt) -> RLPEventData:
        data = log.get('data')
        if type(data) is str:
            data = remove_0x_prefix(data)
        # todo: return the entire event
        return self._format_data(data)

    def _format_data(self, data) -> RLPEventData:
        data = self.decode_data(data)
        code = data[0]
        message = ERROR_CODE.get(int(code), 'Unknown error code')
        # no returns in data
        if not self.formatter:
            formatted_data = {'code': code, 'message': message, 'data': data[1:]}
            return cast(RLPEventData, MutableAttributeDict.recursive(formatted_data))

        args = data[1:]
        if self.formatter.__name__ == 'apply_formatters_to_dict':
            # format the returns as a dict
            raw_formatter = self.formatter.args[0]
            packaged_args = dict(zip(raw_formatter.keys(), args))

        elif self.formatter.__name__ == 'apply_formatter_to_array':
            # format the returns as a dict-list
            actual_args = args[0]
            if type(actual_args) is not list:
                raise ValueError('event data is inconsistent with formatter')

            packaged_args = []
            raw_formatter = self.formatter.args[0].args[0]
            for _args in actual_args:
                packaged_args.append(dict(zip(raw_formatter.keys(), _args)))

        else:
            raise ValueError(f'Unknown formatter: {self.formatter.__name__}')

        formatted_args = apply_result_formatters(self.formatter, packaged_args)
        formatted_data = {'code': code, 'message': message, 'data': formatted_args}
        return cast(RLPEventData, MutableAttributeDict.recursive(formatted_data))

    @staticmethod
    def decode_data(data):
        decoded = []
        unshaped_data = rlp.decode(to_bytes(data))
        # 解码事件code
        code = int(unshaped_data[0])
        decoded.append(code)
        # 解码事件参数
        for arg in unshaped_data[1:]:
            decoded.append(rlp.decode(arg))

        return decoded


def bubble_dict(target: dict, *keys: Any):
    """
    rebuild dict and bubble the keys to top
    """
    copy_dict = copy.copy(target)
    new_dict = dict()
    for key in keys:
        value = copy_dict.pop(key)
        new_dict.update({key: value})
    new_dict.update(copy_dict)
    return new_dict
