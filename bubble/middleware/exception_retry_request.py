from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Type,
)

from requests.exceptions import (
    ConnectionError,
    HTTPError,
    Timeout,
    TooManyRedirects,
)

from bubble.types import (
    RPCEndpoint,
    RPCResponse,
)

if TYPE_CHECKING:
    from bubble import Web3  # noqa: F401

whitelist = [
    "admin",
    "miner",
    "net",
    "txpool",
    "testing",
    "evm",
    "bub_protocolVersion",
    "bub_syncing",
    "bub_coinbase",
    "bub_mining",
    "bub_hashrate",
    "bub_chainId",
    "bub_gasPrice",
    "bub_accounts",
    "bub_blockNumber",
    "bub_getBalance",
    "bub_getStorageAt",
    "bub_getProof",
    "bub_getCode",
    "bub_getBlockByNumber",
    "bub_getBlockByHash",
    "bub_getBlockTransactionCountByNumber",
    "bub_getBlockTransactionCountByHash",
    "bub_getUncleCountByBlockNumber",
    "bub_getUncleCountByBlockHash",
    "bub_getTransactionByHash",
    "bub_getTransactionByBlockHashAndIndex",
    "bub_getTransactionByBlockNumberAndIndex",
    "bub_getTransactionReceipt",
    "bub_getTransactionCount",
    "bub_getRawTransactionByHash",
    "bub_call",
    "bub_estimateGas",
    "bub_newBlockFilter",
    "bub_newPendingTransactionFilter",
    "bub_newFilter",
    "bub_getFilterChanges",
    "bub_getFilterLogs",
    "bub_getLogs",
    "bub_uninstallFilter",
    "bub_getCompilers",
    "bub_getWork",
    "bub_sign",
    "bub_signTypedData",
    "bub_sendRawTransaction",
    "personal_importRawKey",
    "personal_newAccount",
    "personal_listAccounts",
    "personal_listWallets",
    "personal_lockAccount",
    "personal_unlockAccount",
    "personal_ecRecover",
    "personal_sign",
    "personal_signTypedData",
]


def check_if_retry_on_failure(method: RPCEndpoint) -> bool:
    root = method.split("_")[0]
    if root in whitelist:
        return True
    elif method in whitelist:
        return True
    else:
        return False


def exception_retry_middleware(
    make_request: Callable[[RPCEndpoint, Any], RPCResponse],
    w3: "Web3",
    errors: Collection[Type[BaseException]],
    retries: int = 5,
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    """
    Creates middleware that retries failed HTTP requests. Is a default
    middleware for HTTPProvider.
    """

    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if check_if_retry_on_failure(method):
            for i in range(retries):
                try:
                    return make_request(method, params)
                # https://github.com/python/mypy/issues/5349
                except errors:  # type: ignore
                    if i < retries - 1:
                        continue
                    else:
                        raise
            return None
        else:
            return make_request(method, params)

    return middleware


def http_retry_request_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], w3: "Web3"
) -> Callable[[RPCEndpoint, Any], Any]:
    return exception_retry_middleware(
        make_request, w3, (ConnectionError, HTTPError, Timeout, TooManyRedirects)
    )
