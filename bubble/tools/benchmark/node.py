import os
import socket
from subprocess import (
    PIPE,
    Popen,
    check_output,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Any,
    Generator,
    Sequence,
)
import zipfile

from bubble.install import (
    get_executable_path,
    install_bubble,
)

from bubble.tools.benchmark.utils import (
    kill_proc_gracefully,
)

BUB_FIXTURE_ZIP = "bub-1.11.5-fixture.zip"

# use same coinbase value as in `bubble.py/tests/integration/generate_fixtures/common.py`
COINBASE = "0xdc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd"


class BubBenchmarkFixture:
    def __init__(self) -> None:
        self.rpc_port = self._rpc_port()
        self.endpoint_uri = self._endpoint_uri()
        self.bub_binary = self._bub_binary()

    def build(self) -> Generator[Any, None, None]:
        with TemporaryDirectory() as base_dir:
            zipfile_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../../tests/integration/",
                    BUB_FIXTURE_ZIP,
                )
            )
            tmp_datadir = os.path.join(str(base_dir), "datadir")
            with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
                zip_ref.extractall(tmp_datadir)
            self.datadir = tmp_datadir

            genesis_file = os.path.join(self.datadir, "genesis.json")

            yield self._bub_process(self.datadir, genesis_file, self.rpc_port)

    def _rpc_port(self) -> str:
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        return str(port)

    def _endpoint_uri(self) -> str:
        return f"http://localhost:{self.rpc_port}"

    def _bub_binary(self) -> str:
        if "BUB_BINARY" in os.environ:
            return os.environ["BUB_BINARY"]
        elif "BUB_VERSION" in os.environ:
            bub_version = os.environ["BUB_VERSION"]
            _bub_binary = get_executable_path(bub_version)
            if not os.path.exists(_bub_binary):
                install_bub(bub_version)
            assert os.path.exists(_bub_binary)
            return _bub_binary
        else:
            return "bub"

    def _bub_command_arguments(self, datadir: str) -> Sequence[str]:
        return (
            self.bub_binary,
            "--datadir",
            str(datadir),
            "--nodiscover",
            "--fakepow",
            "--http",
            "--http.port",
            self.rpc_port,
            "--http.api",
            "admin,bub,net,bubble,personal,miner",
            "--ipcdisable",
            "--allow-insecure-unlock",
            "--miner.etherbase",
            COINBASE[2:],
            "--rpc.enabledeprecatedpersonal",
        )

    def _bub_process(
        self, datadir: str, genesis_file: str, rpc_port: str
    ) -> Generator[Any, None, None]:
        init_datadir_command = (
            self.bub_binary,
            "--datadir",
            str(datadir),
            "init",
            str(genesis_file),
        )
        check_output(
            init_datadir_command,
            stdin=PIPE,
            stderr=PIPE,
        )
        proc = Popen(
            self._bub_command_arguments(datadir),
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )
        try:
            yield proc
        finally:
            kill_proc_gracefully(proc)
