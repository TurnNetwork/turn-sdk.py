from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Sequence,
    Tuple,
)

from eth_typing import (
    TypeStr,
)
from eth_utils import (
    to_dict,
)
from eth_utils.curried import (
    apply_formatter_at_index,
)
from eth_utils.toolz import (
    curry,
)

from bubble._utils.abi import (
    map_abi_data,
)
from bubble.types import (
    RPCEndpoint,
)


class RPC:
    # admin
    admin_addPeer = RPCEndpoint("admin_addPeer")
    admin_datadir = RPCEndpoint("admin_datadir")
    admin_nodeInfo = RPCEndpoint("admin_nodeInfo")
    admin_peers = RPCEndpoint("admin_peers")
    admin_startHTTP = RPCEndpoint("admin_startHTTP")
    admin_startWS = RPCEndpoint("admin_startWS")
    admin_stopHTTP = RPCEndpoint("admin_stopHTTP")
    admin_stopWS = RPCEndpoint("admin_stopWS")
    admin_getProgramVersion = RPCEndpoint("admin_getProgramVersion")
    admin_getSchnorrNIZKProve = RPCEndpoint("admin_getSchnorrNIZKProve")
    # deprecated
    admin_startRPC = RPCEndpoint("admin_startRPC")
    admin_stopRPC = RPCEndpoint("admin_stopRPC")

    # bub
    bub_accounts = RPCEndpoint("bub_accounts")
    bub_blockNumber = RPCEndpoint("bub_blockNumber")
    bub_call = RPCEndpoint("bub_call")
    bub_chainId = RPCEndpoint("bub_chainId")
    bub_estimateGas = RPCEndpoint("bub_estimateGas")
    bub_feeHistory = RPCEndpoint("bub_feeHistory")
    bub_maxPriorityFeePerGas = RPCEndpoint("bub_maxPriorityFeePerGas")
    bub_gasPrice = RPCEndpoint("bub_gasPrice")
    bub_getBalance = RPCEndpoint("bub_getBalance")
    bub_getBlockByHash = RPCEndpoint("bub_getBlockByHash")
    bub_getBlockByNumber = RPCEndpoint("bub_getBlockByNumber")
    bub_getBlockTransactionCountByHash = RPCEndpoint(
        "bub_getBlockTransactionCountByHash"
    )
    bub_getBlockTransactionCountByNumber = RPCEndpoint(
        "bub_getBlockTransactionCountByNumber"
    )
    bub_getCode = RPCEndpoint("bub_getCode")
    bub_getFilterChanges = RPCEndpoint("bub_getFilterChanges")
    bub_getFilterLogs = RPCEndpoint("bub_getFilterLogs")
    bub_getLogs = RPCEndpoint("bub_getLogs")
    bub_getProof = RPCEndpoint("bub_getProof")
    bub_getRawTransactionByHash = RPCEndpoint("bub_getRawTransactionByHash")
    bub_getStorageAt = RPCEndpoint("bub_getStorageAt")
    bub_getTransactionByBlockHashAndIndex = RPCEndpoint(
        "bub_getTransactionByBlockHashAndIndex"
    )
    bub_getTransactionByBlockNumberAndIndex = RPCEndpoint(
        "bub_getTransactionByBlockNumberAndIndex"
    )
    bub_getRawTransactionByBlockHashAndIndex = RPCEndpoint(
        "bub_getRawTransactionByBlockHashAndIndex"
    )
    bub_getRawTransactionByBlockNumberAndIndex = RPCEndpoint(
        "bub_getRawTransactionByBlockNumberAndIndex"
    )
    bub_getTransactionByHash = RPCEndpoint("bub_getTransactionByHash")
    bub_getTransactionCount = RPCEndpoint("bub_getTransactionCount")
    bub_getTransactionReceipt = RPCEndpoint("bub_getTransactionReceipt")
    bub_newBlockFilter = RPCEndpoint("bub_newBlockFilter")
    bub_newFilter = RPCEndpoint("bub_newFilter")
    bub_newPendingTransactionFilter = RPCEndpoint("bub_newPendingTransactionFilter")
    bub_protocolVersionndingTransactionFilter = RPCEndpoint("bub_protocolVersionndingTransactionFilter")
    bub_sendRawTransaction = RPCEndpoint("bub_sendRawTransaction")
    bub_sendTransaction = RPCEndpoint("bub_sendTransaction")
    bub_sign = RPCEndpoint("bub_sign")
    bub_signTransaction = RPCEndpoint("bub_signTransaction")
    bub_signTypedData = RPCEndpoint("bub_signTypedData")
    bub_syncing = RPCEndpoint("bub_syncing")
    bub_uninstallFilter = RPCEndpoint("bub_uninstallFilter")

    # evm
    # evm_mine = RPCEndpoint("evm_mine")
    # evm_reset = RPCEndpoint("evm_reset")
    # evm_revert = RPCEndpoint("evm_revert")
    # evm_snapshot = RPCEndpoint("evm_snapshot")

    # net
    net_listening = RPCEndpoint("net_listening")
    net_peerCount = RPCEndpoint("net_peerCount")
    net_version = RPCEndpoint("net_version")
    net_availablePorts = RPCEndpoint("net_availablePorts")
    net_signData = RPCEndpoint("net_signData")


    # personal
    personal_ecRecover = RPCEndpoint("personal_ecRecover")
    personal_importRawKey = RPCEndpoint("personal_importRawKey")
    personal_listAccounts = RPCEndpoint("personal_listAccounts")
    personal_listWallets = RPCEndpoint("personal_listWallets")
    personal_lockAccount = RPCEndpoint("personal_lockAccount")
    personal_newAccount = RPCEndpoint("personal_newAccount")
    personal_sendTransaction = RPCEndpoint("personal_sendTransaction")
    personal_sign = RPCEndpoint("personal_sign")
    personal_signTypedData = RPCEndpoint("personal_signTypedData")
    personal_unlockAccount = RPCEndpoint("personal_unlockAccount")

    # debug
    debug_economicConfig = RPCEndpoint("debug_economicConfig")
    debug_getWaitSlashingNodeList = RPCEndpoint("debug_getWaitSlashingNodeList")
    debug_getBadBlocks = RPCEndpoint("debug_getBadBlocks")
    debug_accountRange = RPCEndpoint("debug_accountRange")
    debug_chaindbProperty = RPCEndpoint("debug_chaindbProperty")

    # trace
    trace_block = RPCEndpoint("trace_block")
    trace_call = RPCEndpoint("trace_call")
    trace_filter = RPCEndpoint("trace_filter")
    trace_rawTransaction = RPCEndpoint("trace_rawTransaction")
    trace_replayBlockTransactions = RPCEndpoint("trace_replayBlockTransactions")
    trace_replayTransaction = RPCEndpoint("trace_replayTransaction")
    trace_transaction = RPCEndpoint("trace_transaction")

    # txpool
    txpool_content = RPCEndpoint("txpool_content")
    txpool_inspect = RPCEndpoint("txpool_inspect")
    txpool_status = RPCEndpoint("txpool_status")

    # bubble
    web3_clientVersion = RPCEndpoint("web3_clientVersion")


TRANSACTION_PARAMS_ABIS = {
    "data": "bytes",
    "from": "address",
    "gas": "uint",
    "gasPrice": "uint",
    "maxFeePerGas": "uint",
    "maxPriorityFeePerGas": "uint",
    "nonce": "uint",
    "to": "address",
    "value": "uint",
    "chainId": "uint",
}

FILTER_PARAMS_ABIS = {
    "to": "address",
    "address": "address[]",
}

TRACE_FILTER_PARAM_ABIS = {
    "fromBlock": "uint",
    "toBlock": "uint",
    "fromAddress": "address[]",
    "toAddress": "address[]",
    "after": "int",
    "count": "int",
}

RPC_ABIS = {
    # bub
    "bub_call": TRANSACTION_PARAMS_ABIS,
    "bub_estimateGas": TRANSACTION_PARAMS_ABIS,
    "bub_getBalance": ["address", None],
    "bub_getBlockByHash": ["bytes32", "bool"],
    "bub_getBlockTransactionCountByHash": ["bytes32"],
    "bub_getCode": ["address", None],
    "bub_getLogs": FILTER_PARAMS_ABIS,
    "bub_getRawTransactionByHash": ["bytes32"],
    "bub_getStorageAt": ["address", "uint", None],
    "bub_getProof": ["address", "uint[]", None],
    "bub_getTransactionByBlockHashAndIndex": ["bytes32", "uint"],
    "bub_getTransactionByHash": ["bytes32"],
    "bub_getTransactionCount": ["address", None],
    "bub_getTransactionReceipt": ["bytes32"],
    "bub_getRawTransactionByBlockHashAndIndex": ["bytes32", "uint"],
    "bub_newFilter": FILTER_PARAMS_ABIS,
    "bub_sendRawTransaction": ["bytes"],
    "bub_sendTransaction": TRANSACTION_PARAMS_ABIS,
    "bub_signTransaction": TRANSACTION_PARAMS_ABIS,
    "bub_sign": ["address", "bytes"],
    "bub_signTypedData": ["address", None],
    # personal
    "personal_sendTransaction": TRANSACTION_PARAMS_ABIS,
    "personal_lockAccount": ["address"],
    "personal_unlockAccount": ["address", None, None],
    "personal_sign": [None, "address", None],
    "personal_signTypedData": [None, "address", None],
    # "trace_call": TRANSACTION_PARAMS_ABIS,
    # "trace_filter": TRACE_FILTER_PARAM_ABIS,
}


@curry
def apply_abi_formatters_to_dict(
    normalizers: Sequence[Callable[[TypeStr, Any], Tuple[TypeStr, Any]]],
    abi_dict: Dict[str, Any],
    data: Dict[Any, Any],
) -> Dict[Any, Any]:
    fields = list(abi_dict.keys() & data.keys())
    formatted_values = map_abi_data(
        normalizers,
        [abi_dict[field] for field in fields],
        [data[field] for field in fields],
    )
    formatted_dict = dict(zip(fields, formatted_values))
    return dict(data, **formatted_dict)


@to_dict
def abi_request_formatters(
    normalizers: Sequence[Callable[[TypeStr, Any], Tuple[TypeStr, Any]]],
    abis: Dict[RPCEndpoint, Any],
) -> Iterable[Tuple[RPCEndpoint, Callable[..., Any]]]:
    for method, abi_types in abis.items():
        if isinstance(abi_types, list):
            yield method, map_abi_data(normalizers, abi_types)
        elif isinstance(abi_types, dict):
            single_dict_formatter = apply_abi_formatters_to_dict(normalizers, abi_types)
            yield method, apply_formatter_at_index(single_dict_formatter, 0)
        else:
            raise TypeError(
                f"ABI definitions must be a list or dictionary, got {abi_types!r}"
            )
