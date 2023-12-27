from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
)

from eth_utils.curried import (
    apply_formatter_if,
    apply_formatters_to_dict,
    apply_key_map,
    is_null,
)
from eth_utils.toolz import (
    complement,
    compose,
)
from hexbytes import (
    HexBytes,
)

from bubble._utils.rpc_abi import (
    RPC,
)
from bubble.middleware.formatting import (
    async_construct_formatting_middleware,
    construct_formatting_middleware,
)
from bubble.types import (
    AsyncMiddlewareCoroutine,
    RPCEndpoint,
)

if TYPE_CHECKING:
    from bubble import (  # noqa: F401
        AsyncWeb3,
        Web3,
    )

is_not_null = complement(is_null)

remap_node_poa_fields = apply_key_map(
    {
        "extraData": "proofOfAuthorityData",
    }
)

pythonic_bub_poa = apply_formatters_to_dict(
    {
        "proofOfAuthorityData": HexBytes,
    }
)

node_poa_cleanup = compose(pythonic_bub_poa, remap_node_poa_fields)


node_poa_middleware = construct_formatting_middleware(
    result_formatters={
        RPC.bub_getBlockByHash: apply_formatter_if(is_not_null, node_poa_cleanup),
        RPC.bub_getBlockByNumber: apply_formatter_if(is_not_null, node_poa_cleanup),
    },
)


async def async_node_poa_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], w3: "AsyncWeb3"
) -> AsyncMiddlewareCoroutine:
    middleware = await async_construct_formatting_middleware(
        result_formatters={
            RPC.bub_getBlockByHash: apply_formatter_if(is_not_null, node_poa_cleanup),
            RPC.bub_getBlockByNumber: apply_formatter_if(is_not_null, node_poa_cleanup),
        },
    )
    return await middleware(make_request, w3)
