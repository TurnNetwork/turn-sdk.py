from bubble import (
    IPCProvider,
    Web3,
)
from bubble.middleware import (
    node_poa_middleware,
)
from bubble.providers.ipc import (
    get_dev_ipc_path,
)

w3 = Web3(IPCProvider(get_dev_ipc_path()))
w3.middleware_onion.inject(node_poa_middleware, layer=0)
