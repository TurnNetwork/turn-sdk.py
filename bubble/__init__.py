from eth_account import Account  # noqa: E402,
import pkg_resources

from bubble.main import (
    AsyncWeb3,
    Web3,
)
from bubble.providers.async_rpc import (  # noqa: E402
    AsyncHTTPProvider,
)
from bubble.providers.bub_tester import (  # noqa: E402
    BubbleTesterProvider,
)
from bubble.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from bubble.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from bubble.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

__version__ = pkg_resources.get_distribution("bubble-sdk").version

__all__ = [
    "__version__",
    "AsyncWeb3",
    "Web3",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "BubbleTesterProvider",
    "Account",
    "AsyncHTTPProvider",
]
