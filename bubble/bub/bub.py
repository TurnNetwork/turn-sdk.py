from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
    overload,
)
import warnings

from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    HexStr,
)
from eth_utils.toolz import (
    merge,
)
from hexbytes import (
    HexBytes,
)

from bubble._utils.blocks import (
    select_method_for_block_identifier,
)
from bubble._utils.fee_utils import (
    fee_history_priority_fee,
)
from bubble._utils.filters import (
    Filter,
    select_filter_method,
)
from bubble._utils.rpc_abi import (
    RPC,
)
from bubble._utils.threads import (
    Timeout,
)
from bubble._utils.transactions import (
    assert_valid_transaction_params,
    extract_valid_transaction_params,
    get_required_transaction,
    replace_transaction,
)
from bubble.contract import (
    Contract,
    ContractCaller,
)
from bubble.bub.base_bub import (
    BaseBub,
)
from bubble.exceptions import (
    OffchainLookup,
    TimeExhausted,
    TooManyRequests,
    TransactionNotFound,
)
from bubble.method import (
    Method,
    default_root_munger,
)
from bubble.types import (
    ENS,
    BlockData,
    BlockIdentifier,
    BlockParams,
    CallOverride,
    FeeHistory,
    FilterParams,
    LogReceipt,
    MerkleProof,
    Nonce,
    SignedTx,
    SyncStatus,
    TxData,
    TxParams,
    TxReceipt,
    Uncle,
    Wei,
    _Hash32,
)
from bubble.utils import (
    handle_offchain_lookup,
)

if TYPE_CHECKING:
    from bubble import Web3  # noqa: F401


class Bub(BaseBub):
    # mypy types
    w3: "Web3"

    _default_contract_factory: Type[Union[Contract, ContractCaller]] = Contract

    # bub_accounts

    _accounts: Method[Callable[[], Tuple[ChecksumAddress]]] = Method(
        RPC.bub_accounts,
        is_property=True,
    )

    @property
    def accounts(self) -> Tuple[ChecksumAddress]:
        return self._accounts()

    # bub_blockNumber

    get_block_number: Method[Callable[[], BlockNumber]] = Method(
        RPC.bub_blockNumber,
        is_property=True,
    )

    @property
    def block_number(self) -> BlockNumber:
        return self.get_block_number()

    # bub_chainId

    _chain_id: Method[Callable[[], int]] = Method(
        RPC.bub_chainId,
        is_property=True,
    )

    @property
    def chain_id(self) -> int:
        return self._chain_id()

    # bub_gasPrice

    _gas_price: Method[Callable[[], Wei]] = Method(
        RPC.bub_gasPrice,
        is_property=True,
    )

    @property
    def gas_price(self) -> Wei:
        return self._gas_price()

    # bub_maxPriorityFeePerGas

    # _max_priority_fee: Method[Callable[[], Wei]] = Method(
    #     RPC.bub_maxPriorityFeePerGas,
    #     is_property=True,
    # )
    #
    # @property
    # def max_priority_fee(self) -> Wei:
    #     """
    #     Try to use bub_maxPriorityFeePerGas but, since this is not part
    #     of the spec and is only supported by some clients, fall back to
    #     an bub_feeHistory calculation with min and max caps.
    #     """
    #     try:
    #         return self._max_priority_fee()
    #     except ValueError:
    #         warnings.warn(
    #             "There was an issue with the method bub_maxPriorityFeePerGas. "
    #             "Calculating using bub_feeHistory."
    #         )
    #         return fee_history_priority_fee(self)

    # bub_syncing

    _syncing: Method[Callable[[], Union[SyncStatus, bool]]] = Method(
        RPC.bub_syncing,
        is_property=True,
    )

    @property
    def syncing(self) -> Union[SyncStatus, bool]:
        return self._syncing()

    # bub_feeHistory

    # _fee_history: Method[
    #     Callable[
    #         [int, Union[BlockParams, BlockNumber], Optional[List[float]]], FeeHistory
    #     ]
    # ] = Method(RPC.bub_feeHistory, mungers=[default_root_munger])

    # def fee_history(
    #     self,
    #     block_count: int,
    #     newest_block: Union[BlockParams, BlockNumber],
    #     reward_percentiles: Optional[List[float]] = None,
    # ) -> FeeHistory:
    #     return self._fee_history(block_count, newest_block, reward_percentiles)

    # bub_call

    _call: Method[
        Callable[
            [TxParams, Optional[BlockIdentifier], Optional[CallOverride]],
            HexBytes,
        ]
    ] = Method(RPC.bub_call, mungers=[BaseBub.call_munger])

    def call(
        self,
        transaction: TxParams,
        block_identifier: Optional[BlockIdentifier] = None,
        state_override: Optional[CallOverride] = None,
        ccip_read_enabled: Optional[bool] = None,
    ) -> HexBytes:
        ccip_read_enabled_on_provider = self.w3.provider.global_ccip_read_enabled
        if (
            # default conditions:
            ccip_read_enabled_on_provider
            and ccip_read_enabled is not False
            # explicit call flag overrides provider flag,
            # enabling ccip read for specific calls:
            or not ccip_read_enabled_on_provider
            and ccip_read_enabled is True
        ):
            return self._durin_call(transaction, block_identifier, state_override)

        return self._call(transaction, block_identifier, state_override)

    def _durin_call(
        self,
        transaction: TxParams,
        block_identifier: Optional[BlockIdentifier] = None,
        state_override: Optional[CallOverride] = None,
    ) -> HexBytes:
        max_redirects = self.w3.provider.ccip_read_max_redirects

        if not max_redirects or max_redirects < 4:
            raise ValueError(
                "ccip_read_max_redirects property on provider must be at least 4."
            )

        for _ in range(max_redirects):
            try:
                return self._call(transaction, block_identifier, state_override)
            except OffchainLookup as offchain_lookup:
                durin_calldata = handle_offchain_lookup(
                    offchain_lookup.payload, transaction
                )
                transaction["data"] = durin_calldata

        raise TooManyRequests("Too many CCIP read redirects")

    # bub_estimateGas

    _estimate_gas: Method[
        Callable[[TxParams, Optional[BlockIdentifier]], int]
    ] = Method(RPC.bub_estimateGas, mungers=[BaseBub.estimate_gas_munger])

    def estimate_gas(
        self, transaction: TxParams, block_identifier: Optional[BlockIdentifier] = None
    ) -> int:
        return self._estimate_gas(transaction, block_identifier)

    # bub_getTransactionByHash

    _get_transaction: Method[Callable[[_Hash32], TxData]] = Method(
        RPC.bub_getTransactionByHash, mungers=[default_root_munger]
    )

    def get_transaction(self, transaction_hash: _Hash32) -> TxData:
        return self._get_transaction(transaction_hash)

    # bub_getRawTransactionByHash

    _get_raw_transaction: Method[Callable[[_Hash32], HexBytes]] = Method(
        RPC.bub_getRawTransactionByHash, mungers=[default_root_munger]
    )

    def get_raw_transaction(self, transaction_hash: _Hash32) -> HexBytes:
        return self._get_raw_transaction(transaction_hash)

    # bub_getTransactionByBlockNumberAndIndex
    # bub_getTransactionByBlockHashAndIndex

    get_transaction_by_block: Method[Callable[[BlockIdentifier, int], TxData]] = Method(
        method_choice_depends_on_args=select_method_for_block_identifier(
            if_predefined=RPC.bub_getTransactionByBlockNumberAndIndex,
            if_hash=RPC.bub_getTransactionByBlockHashAndIndex,
            if_number=RPC.bub_getTransactionByBlockNumberAndIndex,
        ),
        mungers=[default_root_munger],
    )

    # bub_getRawTransactionByBlockHashAndIndex
    # bub_getRawTransactionByBlockNumberAndIndex

    _get_raw_transaction_by_block: Method[
        Callable[[BlockIdentifier, int], HexBytes]
    ] = Method(
        method_choice_depends_on_args=select_method_for_block_identifier(
            if_predefined=RPC.bub_getRawTransactionByBlockNumberAndIndex,
            if_hash=RPC.bub_getRawTransactionByBlockHashAndIndex,
            if_number=RPC.bub_getRawTransactionByBlockNumberAndIndex,
        ),
        mungers=[default_root_munger],
    )

    def get_raw_transaction_by_block(
        self, block_identifier: BlockIdentifier, index: int
    ) -> HexBytes:
        return self._get_raw_transaction_by_block(block_identifier, index)

    # bub_getBlockTransactionCountByHash
    # bub_getBlockTransactionCountByNumber

    get_block_transaction_count: Method[Callable[[BlockIdentifier], int]] = Method(
        method_choice_depends_on_args=select_method_for_block_identifier(
            if_predefined=RPC.bub_getBlockTransactionCountByNumber,
            if_hash=RPC.bub_getBlockTransactionCountByHash,
            if_number=RPC.bub_getBlockTransactionCountByNumber,
        ),
        mungers=[default_root_munger],
    )

    # bub_sendTransaction

    _send_transaction: Method[Callable[[TxParams], HexBytes]] = Method(
        RPC.bub_sendTransaction, mungers=[BaseBub.send_transaction_munger]
    )

    def send_transaction(self, transaction: TxParams) -> HexBytes:
        return self._send_transaction(transaction)

    # bub_sendRawTransaction

    _send_raw_transaction: Method[Callable[[Union[HexStr, bytes]], HexBytes]] = Method(
        RPC.bub_sendRawTransaction,
        mungers=[default_root_munger],
    )

    def send_raw_transaction(self, transaction: Union[HexStr, bytes]) -> HexBytes:
        return self._send_raw_transaction(transaction)

    # bub_getBlockByHash
    # bub_getBlockByNumber

    _get_block: Method[Callable[[BlockIdentifier, bool], BlockData]] = Method(
        method_choice_depends_on_args=select_method_for_block_identifier(
            if_predefined=RPC.bub_getBlockByNumber,
            if_hash=RPC.bub_getBlockByHash,
            if_number=RPC.bub_getBlockByNumber,
        ),
        mungers=[BaseBub.get_block_munger],
    )

    def get_block(
        self, block_identifier: BlockIdentifier, full_transactions: bool = False
    ) -> BlockData:
        return self._get_block(block_identifier, full_transactions)

    # bub_getBalance

    _get_balance: Method[
        Callable[[Union[Address, ChecksumAddress, ENS], Optional[BlockIdentifier]], Wei]
    ] = Method(
        RPC.bub_getBalance,
        mungers=[BaseBub.block_id_munger],
    )

    def get_balance(
        self,
        account: Union[Address, ChecksumAddress, ENS],
        block_identifier: Optional[BlockIdentifier] = None,
    ) -> Wei:
        return self._get_balance(account, block_identifier)

    # bub_getCode

    _get_code: Method[
        Callable[
            [Union[Address, ChecksumAddress, ENS], Optional[BlockIdentifier]], HexBytes
        ]
    ] = Method(RPC.bub_getCode, mungers=[BaseBub.block_id_munger])

    def get_code(
        self,
        account: Union[Address, ChecksumAddress, ENS],
        block_identifier: Optional[BlockIdentifier] = None,
    ) -> HexBytes:
        return self._get_code(account, block_identifier)

    # bub_getLogs

    _get_logs: Method[Callable[[FilterParams], List[LogReceipt]]] = Method(
        RPC.bub_getLogs, mungers=[default_root_munger]
    )

    def get_logs(
        self,
        filter_params: FilterParams,
    ) -> List[LogReceipt]:
        return self._get_logs(filter_params)

    # bub_getTransactionCount

    _get_transaction_count: Method[
        Callable[
            [Union[Address, ChecksumAddress, ENS], Optional[BlockIdentifier]], Nonce
        ]
    ] = Method(
        RPC.bub_getTransactionCount,
        mungers=[BaseBub.block_id_munger],
    )

    def get_transaction_count(
        self,
        account: Union[Address, ChecksumAddress, ENS],
        block_identifier: Optional[BlockIdentifier] = None,
    ) -> Nonce:
        return self._get_transaction_count(account, block_identifier)

    # bub_getTransactionReceipt

    _transaction_receipt: Method[Callable[[_Hash32], TxReceipt]] = Method(
        RPC.bub_getTransactionReceipt, mungers=[default_root_munger]
    )

    def get_transaction_receipt(self, transaction_hash: _Hash32) -> TxReceipt:
        return self._transaction_receipt(transaction_hash)

    def wait_for_transaction_receipt(
        self, transaction_hash: _Hash32, timeout: float = 120, poll_latency: float = 0.1
    ) -> TxReceipt:
        timeout = 60
        try:
            with Timeout(timeout) as _timeout:
                while True:
                    try:
                        tx_receipt = self._transaction_receipt(transaction_hash)
                    except TransactionNotFound:
                        tx_receipt = None
                    if tx_receipt is not None:
                        break
                    _timeout.sleep(poll_latency)
            return tx_receipt

        except Timeout:
            raise TimeExhausted(
                f"Transaction {HexBytes(transaction_hash) !r} is not in the chain "
                f"after {timeout} seconds"
            )

    # bub_getStorageAt

    get_storage_at: Method[
        Callable[[Union[Address, ChecksumAddress, ENS], int], HexBytes]
    ] = Method(
        RPC.bub_getStorageAt,
        mungers=[BaseBub.get_storage_at_munger],
    )

    # bub_getProof

    # def get_proof_munger(
    #     self,
    #     account: Union[Address, ChecksumAddress, ENS],
    #     positions: Sequence[int],
    #     block_identifier: Optional[BlockIdentifier] = None,
    # ) -> Tuple[
    #     Union[Address, ChecksumAddress, ENS], Sequence[int], Optional[BlockIdentifier]
    # ]:
    #     if block_identifier is None:
    #         block_identifier = self.default_block
    #     return (account, positions, block_identifier)

    # get_proof: Method[
    #     Callable[
    #         [
    #             Tuple[
    #                 Union[Address, ChecksumAddress, ENS],
    #                 Sequence[int],
    #                 Optional[BlockIdentifier],
    #             ]
    #         ],
    #         MerkleProof,
    #     ]
    # ] = Method(
    #     RPC.bub_getProof,
    #     mungers=[get_proof_munger],
    # )

    def replace_transaction(
        self, transaction_hash: _Hash32, new_transaction: TxParams
    ) -> HexBytes:
        current_transaction = get_required_transaction(self.w3, transaction_hash)
        return replace_transaction(self.w3, current_transaction, new_transaction)

    # todo: Update Any to stricter kwarg checking with TxParams
    # https://github.com/python/mypy/issues/4441
    def modify_transaction(
        self, transaction_hash: _Hash32, **transaction_params: Any
    ) -> HexBytes:
        assert_valid_transaction_params(cast(TxParams, transaction_params))
        current_transaction = get_required_transaction(self.w3, transaction_hash)
        current_transaction_params = extract_valid_transaction_params(
            current_transaction
        )
        new_transaction = merge(current_transaction_params, transaction_params)
        return replace_transaction(self.w3, current_transaction, new_transaction)

    # bub_sign

    sign: Method[Callable[..., HexStr]] = Method(
        RPC.bub_sign, mungers=[BaseBub.sign_munger]
    )

    # bub_signTransaction

    sign_transaction: Method[Callable[[TxParams], SignedTx]] = Method(
        RPC.bub_signTransaction,
        mungers=[default_root_munger],
    )

    # bub_signTypedData

    sign_typed_data: Method[
        Callable[[Union[Address, ChecksumAddress, ENS], str], HexStr]
    ] = Method(
        RPC.bub_signTypedData,
        mungers=[default_root_munger],
    )

    # bub_newFilter, bub_newBlockFilter, bub_newPendingTransactionFilter

    filter: Method[
        Callable[[Optional[Union[str, FilterParams, HexStr]]], Filter]
    ] = Method(
        method_choice_depends_on_args=select_filter_method(
            if_new_block_filter=RPC.bub_newBlockFilter,
            if_new_pending_transaction_filter=RPC.bub_newPendingTransactionFilter,
            if_new_filter=RPC.bub_newFilter,
        ),
        mungers=[BaseBub.filter_munger],
    )

    # bub_getFilterChanges, bub_getFilterLogs, bub_uninstallFilter

    get_filter_changes: Method[Callable[[HexStr], List[LogReceipt]]] = Method(
        RPC.bub_getFilterChanges, mungers=[default_root_munger]
    )

    get_filter_logs: Method[Callable[[HexStr], List[LogReceipt]]] = Method(
        RPC.bub_getFilterLogs, mungers=[default_root_munger]
    )

    uninstall_filter: Method[Callable[[HexStr], bool]] = Method(
        RPC.bub_uninstallFilter,
        mungers=[default_root_munger],
    )

    @overload
    def contract(self, address: None = None, **kwargs: Any) -> Type[Contract]:
        ...

    @overload
    def contract(
        self, address: Union[Address, ChecksumAddress, ENS], **kwargs: Any
    ) -> Contract:
        ...

    def contract(
        self,
        address: Optional[Union[Address, ChecksumAddress, ENS]] = None,
        **kwargs: Any,
    ) -> Union[Type[Contract], Contract]:
        ContractFactoryClass = kwargs.pop(
            "ContractFactoryClass", self._default_contract_factory
        )

        ContractFactory = ContractFactoryClass.factory(self.w3, **kwargs)

        if address:
            return ContractFactory(address)
        else:
            return ContractFactory

    def set_contract_factory(
        self,
        contract_factory: Type[Union[Contract, ContractCaller]],
    ) -> None:
        self._default_contract_factory = contract_factory
