from typing import (
    Optional,
)

from bubble import (
    Web3,
)
from bubble._utils.rpc_abi import (
    RPC,
)
from bubble.types import (
    TxParams,
    Wei,
)


def rpc_gas_price_strategy(
    w3: Web3, transaction_params: Optional[TxParams] = None
) -> Wei:
    """
    A simple gas price strategy deriving it's value from the bub_gasPrice JSON-RPC call.
    """
    return w3.manager.request_blocking(RPC.bub_gasPrice, [])
