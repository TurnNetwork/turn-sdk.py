import itertools
import os
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    AsyncIterator,
    Callable,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
    cast,
)

from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    Hash32,
    HexStr,
)
from eth_utils import (
    apply_key_map,
    is_hex,
    is_string,
    to_hex,
    to_int,
    to_list,
)
from eth_utils.toolz import (
    concat,
    valfilter,
)

from bubble._utils.formatters import (
    hex_to_integer,
)
from bubble._utils.rpc_abi import (
    RPC,
)
from bubble.types import (
    Coroutine,
    FilterParams,
    LatestBlockParam,
    LogReceipt,
    RPCEndpoint,
    RPCResponse,
    _Hash32,
)

if TYPE_CHECKING:
    from bubble import Web3  # noqa: F401

if "WEB3_MAX_BLOCK_REQUEST" in os.environ:
    MAX_BLOCK_REQUEST = to_int(text=os.environ["WEB3_MAX_BLOCK_REQUEST"])
else:
    MAX_BLOCK_REQUEST = 50


def segment_count(start: int, stop: int, step: int = 5) -> Iterable[Tuple[int, int]]:
    """Creates a segment counting generator

    The generator returns tuple pairs of integers
    that correspond to segments in the provided range.

    :param start: The initial value of the counting range
    :param stop: The last value in the
    counting range
    :param step: Optional, the segment length. Default is 5.
    :return: returns a generator object


    Example:

    >>> segment_counter = segment_count(start=0, stop=10, step=3)
    >>> next(segment_counter)
    (0, 3)
    >>> next(segment_counter)
    (3, 6)
    >>> next(segment_counter)
    (6, 9)
    >>> next(segment_counter) #  Remainder is also returned
    (9, 10)
    """
    return gen_bounded_segments(start, stop, step)


def gen_bounded_segments(start: int, stop: int, step: int) -> Iterable[Tuple[int, int]]:
    #  If the initial range is less than the step
    #  just return (start, stop)
    if start + step >= stop:
        yield (start, stop)
        return
    for segment in zip(
        range(start, stop - step + 1, step), range(start + step, stop + 1, step)
    ):
        yield segment

    remainder = (stop - start) % step
    #  Handle the remainder
    if remainder:
        yield (stop - remainder, stop)


def block_ranges(
    start_block: BlockNumber, last_block: Optional[BlockNumber], step: int = 5
) -> Iterable[Tuple[BlockNumber, BlockNumber]]:
    """Returns 2-tuple ranges describing ranges of block from start_block to last_block

    Ranges do not overlap to facilitate use as ``toBlock``, ``fromBlock``
    json-rpc arguments, which are both inclusive.
    """
    if last_block is not None and start_block > last_block:
        raise TypeError(
            "Incompatible start and stop arguments.",
            "Start must be less than or equal to stop.",
        )

    return (
        (BlockNumber(from_block), BlockNumber(to_block - 1))
        for from_block, to_block in segment_count(start_block, last_block + 1, step)
    )


def iter_latest_block(
    w3: "Web3", to_block: Optional[Union[BlockNumber, LatestBlockParam]] = None
) -> Iterable[BlockNumber]:
    """Returns a generator that dispenses the latest block, if
    any new blocks have been mined since last iteration.

    If there are no new blocks or the latest block is greater than
    the ``to_block`` None is returned.

    >>> new_blocks = iter_latest_block(w3, 0, 10)
    >>> next(new_blocks)  # Latest block = 0
    0
    >>> next(new_blocks)  # No new blocks
    >>> next(new_blocks)  # Latest block = 1
    1
    >>> next(new_blocks)  # Latest block = 10
    10
    >>> next(new_blocks)  # latest block > to block
    """
    _last = None

    is_bounded_range = to_block is not None and to_block != "latest"

    while True:
        latest_block = w3.bub.block_number
        # type ignored b/c is_bounded_range prevents unsupported comparison
        if is_bounded_range and latest_block > to_block:  # type: ignore
            yield None
        #  No new blocks since last iteration.
        if _last is not None and _last == latest_block:
            yield None
        else:
            yield latest_block
        _last = latest_block


def iter_latest_block_ranges(
    w3: "Web3",
    from_block: BlockNumber,
    to_block: Optional[Union[BlockNumber, LatestBlockParam]] = None,
) -> Iterable[Tuple[Optional[BlockNumber], Optional[BlockNumber]]]:
    """Returns an iterator unloading ranges of available blocks

    starting from `fromBlock` to the latest mined block,
    until reaching toBlock. e.g.:


    >>> blocks_to_filter = iter_latest_block_ranges(w3, 0, 50)
    >>> next(blocks_to_filter)  # latest block number = 11
    (0, 11)
    >>> next(blocks_to_filter)  # latest block number = 45
    (12, 45)
    >>> next(blocks_to_filter)  # latest block number = 50
    (46, 50)
    """
    for latest_block in iter_latest_block(w3, to_block):
        if latest_block is None:
            yield (None, None)
        elif from_block > latest_block:
            yield (None, None)
        else:
            yield (from_block, latest_block)
            from_block = BlockNumber(latest_block + 1)


def drop_items_with_none_value(params: Dict[str, Any]) -> Dict[str, Any]:
    return valfilter(lambda x: x is not None, params)


def get_logs_multipart(
    w3: "Web3",
    start_block: BlockNumber,
    stop_block: BlockNumber,
    address: Union[Address, ChecksumAddress, List[Union[Address, ChecksumAddress]]],
    topics: List[Optional[Union[_Hash32, List[_Hash32]]]],
    max_blocks: int,
) -> Iterable[List[LogReceipt]]:
    """Used to break up requests to ``bub_getLogs``

    The getLog request is partitioned into multiple calls of the max number of blocks
    ``max_blocks``.
    """
    _block_ranges = block_ranges(start_block, stop_block, max_blocks)
    for from_block, to_block in _block_ranges:
        params = {
            "fromBlock": from_block,
            "toBlock": to_block,
            "address": address,
            "topics": topics,
        }
        yield w3.bub.get_logs(cast(FilterParams, drop_items_with_none_value(params)))


class RequestLogs:
    _from_block: BlockNumber

    def __init__(
        self,
        w3: "Web3",
        from_block: Optional[Union[BlockNumber, LatestBlockParam]] = None,
        to_block: Optional[Union[BlockNumber, LatestBlockParam]] = None,
        address: Optional[
            Union[Address, ChecksumAddress, List[Union[Address, ChecksumAddress]]]
        ] = None,
        topics: Optional[List[Optional[Union[_Hash32, List[_Hash32]]]]] = None,
    ) -> None:
        self.address = address
        self.topics = topics
        self.w3 = w3
        if from_block is None or from_block == "latest":
            self._from_block = BlockNumber(w3.bub.block_number + 1)
        elif is_string(from_block) and is_hex(from_block):
            self._from_block = BlockNumber(hex_to_integer(from_block))  # type: ignore
        else:
            # cast b/c LatestBlockParam is handled above
            self._from_block = from_block
        self._to_block = to_block
        self.filter_changes = self._get_filter_changes()

    @property
    def from_block(self) -> BlockNumber:
        return self._from_block

    @property
    def to_block(self) -> BlockNumber:
        if self._to_block is None:
            to_block = self.w3.bub.block_number
        elif self._to_block == "latest":
            to_block = self.w3.bub.block_number
        elif is_string(self._to_block) and is_hex(self._to_block):
            to_block = BlockNumber(hex_to_integer(self._to_block))  # type: ignore
        else:
            to_block = self._to_block

        return to_block

    def _get_filter_changes(self) -> Iterator[List[LogReceipt]]:
        for start, stop in iter_latest_block_ranges(
            self.w3, self.from_block, self.to_block
        ):
            if None in (start, stop):
                yield []
            else:
                yield list(
                    concat(
                        get_logs_multipart(
                            self.w3,
                            start,
                            stop,
                            self.address,
                            self.topics,
                            max_blocks=MAX_BLOCK_REQUEST,
                        )
                    )
                )

    def get_logs(self) -> List[LogReceipt]:
        return list(
            concat(
                get_logs_multipart(
                    self.w3,
                    self.from_block,
                    self.to_block,
                    self.address,
                    self.topics,
                    max_blocks=MAX_BLOCK_REQUEST,
                )
            )
        )


FILTER_PARAMS_KEY_MAP = {"toBlock": "to_block", "fromBlock": "from_block"}

NEW_FILTER_METHODS = {
    "bub_newBlockFilter",
    "bub_newFilter",
}

FILTER_CHANGES_METHODS = {
    "bub_getFilterChanges",
    "bub_getFilterLogs",
}


class RequestBlocks:
    def __init__(self, w3: "Web3") -> None:
        self.w3 = w3
        self.start_block = BlockNumber(w3.bub.block_number + 1)

    @property
    def filter_changes(self) -> Iterator[List[Hash32]]:
        return self.get_filter_changes()

    def get_filter_changes(self) -> Iterator[List[Hash32]]:
        block_range_iter = iter_latest_block_ranges(self.w3, self.start_block, None)

        for block_range in block_range_iter:
            yield (block_hashes_in_range(self.w3, block_range))


@to_list
def block_hashes_in_range(
    w3: "Web3", block_range: Tuple[BlockNumber, BlockNumber]
) -> Iterable[Hash32]:
    from_block, to_block = block_range
    if from_block is None or to_block is None:
        return
    for block_number in range(from_block, to_block + 1):
        yield getattr(w3.bub.get_block(BlockNumber(block_number)), "hash", None)


def local_filter_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], w3: "Web3"
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    filters = {}
    filter_id_counter = map(to_hex, itertools.count())

    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if method in NEW_FILTER_METHODS:
            filter_id = next(filter_id_counter)

            _filter: Union[RequestLogs, RequestBlocks]
            if method == RPC.bub_newFilter:
                _filter = RequestLogs(
                    w3, **apply_key_map(FILTER_PARAMS_KEY_MAP, params[0])
                )

            elif method == RPC.bub_newBlockFilter:
                _filter = RequestBlocks(w3)

            else:
                raise NotImplementedError(method)

            filters[filter_id] = _filter
            return {"result": filter_id}

        elif method in FILTER_CHANGES_METHODS:
            filter_id = params[0]
            #  Pass through to filters not created by middleware
            if filter_id not in filters:
                return make_request(method, params)
            _filter = filters[filter_id]
            if method == RPC.bub_getFilterChanges:
                return {"result": next(_filter.filter_changes)}

            elif method == RPC.bub_getFilterLogs:
                # type ignored b/c logic prevents RequestBlocks which
                # doesn't implement get_logs
                return {"result": _filter.get_logs()}  # type: ignore
            else:
                raise NotImplementedError(method)
        else:
            return make_request(method, params)

    return middleware


# --- async --- #


async def async_iter_latest_block(
    w3: "Web3", to_block: Optional[Union[BlockNumber, LatestBlockParam]] = None
) -> AsyncIterable[BlockNumber]:
    """Returns a generator that dispenses the latest block, if
    any new blocks have been mined since last iteration.

    If there are no new blocks or the latest block is greater than
    the ``to_block`` None is returned.

    >>> new_blocks = iter_latest_block(w3, 0, 10)
    >>> next(new_blocks)  # Latest block = 0
    0
    >>> next(new_blocks)  # No new blocks
    >>> next(new_blocks)  # Latest block = 1
    1
    >>> next(new_blocks)  # Latest block = 10
    10
    >>> next(new_blocks)  # latest block > to block
    """
    _last = None

    is_bounded_range = to_block is not None and to_block != "latest"

    while True:
        latest_block = await w3.bub.block_number  # type: ignore
        # type ignored b/c is_bounded_range prevents unsupported comparison
        if is_bounded_range and latest_block > to_block:
            yield None
        #  No new blocks since last iteration.
        if _last is not None and _last == latest_block:
            yield None
        else:
            yield latest_block
        _last = latest_block


async def async_iter_latest_block_ranges(
    w3: "Web3",
    from_block: BlockNumber,
    to_block: Optional[Union[BlockNumber, LatestBlockParam]] = None,
) -> AsyncIterable[Tuple[Optional[BlockNumber], Optional[BlockNumber]]]:
    """Returns an iterator unloading ranges of available blocks

    starting from `from_block` to the latest mined block,
    until reaching to_block. e.g.:


    >>> blocks_to_filter = iter_latest_block_ranges(w3, 0, 50)
    >>> next(blocks_to_filter)  # latest block number = 11
    (0, 11)
    >>> next(blocks_to_filter)  # latest block number = 45
    (12, 45)
    >>> next(blocks_to_filter)  # latest block number = 50
    (46, 50)
    """
    latest_block_iterator = async_iter_latest_block(w3, to_block)
    async for latest_block in latest_block_iterator:
        if latest_block is None:
            yield (None, None)
        elif from_block > latest_block:
            yield (None, None)
        else:
            yield (from_block, latest_block)
            from_block = BlockNumber(latest_block + 1)


async def async_get_logs_multipart(
    w3: "Web3",
    start_block: BlockNumber,
    stop_block: BlockNumber,
    address: Union[Address, ChecksumAddress, List[Union[Address, ChecksumAddress]]],
    topics: List[Optional[Union[_Hash32, List[_Hash32]]]],
    max_blocks: int,
) -> AsyncIterable[List[LogReceipt]]:
    """Used to break up requests to ``bub_getLogs``

    The getLog request is partitioned into multiple calls of the max number of blocks
    ``max_blocks``.
    """
    _block_ranges = block_ranges(start_block, stop_block, max_blocks)
    for from_block, to_block in _block_ranges:
        params = {
            "fromBlock": from_block,
            "toBlock": to_block,
            "address": address,
            "topics": topics,
        }
        params_with_none_dropped = cast(
            FilterParams, drop_items_with_none_value(params)
        )
        next_logs = await w3.bub.get_logs(params_with_none_dropped)  # type: ignore
        yield next_logs


class AsyncRequestLogs:
    _from_block: BlockNumber

    def __init__(
        self,
        w3: "Web3",
        from_block: Optional[Union[BlockNumber, LatestBlockParam]] = None,
        to_block: Optional[Union[BlockNumber, LatestBlockParam]] = None,
        address: Optional[
            Union[Address, ChecksumAddress, List[Union[Address, ChecksumAddress]]]
        ] = None,
        topics: Optional[List[Optional[Union[_Hash32, List[_Hash32]]]]] = None,
    ) -> None:
        self.address = address
        self.topics = topics
        self.w3 = w3
        self._from_block_arg = from_block
        self._to_block = to_block
        self.filter_changes = self._get_filter_changes()

    def __await__(self) -> Generator[Any, None, "AsyncRequestLogs"]:
        async def closure() -> "AsyncRequestLogs":
            if self._from_block_arg is None or self._from_block_arg == "latest":
                self.block_number = await self.w3.bub.block_number  # type: ignore
                self._from_block = BlockNumber(self.block_number + 1)
            elif is_string(self._from_block_arg) and is_hex(self._from_block_arg):
                self._from_block = BlockNumber(
                    hex_to_integer(cast(HexStr, self._from_block_arg))
                )
            else:
                self._from_block = self._from_block_arg

            return self

        return closure().__await__()

    @property
    async def from_block(self) -> BlockNumber:
        return self._from_block

    @property
    async def to_block(self) -> BlockNumber:
        if self._to_block is None or self._to_block == "latest":
            to_block = await self.w3.bub.block_number  # type: ignore
        elif is_string(self._to_block) and is_hex(self._to_block):
            to_block = BlockNumber(hex_to_integer(cast(HexStr, self._to_block)))
        else:
            to_block = self._to_block

        return to_block

    async def _get_filter_changes(self) -> AsyncIterator[List[LogReceipt]]:
        self_from_block = await self.from_block
        self_to_block = await self.to_block
        async for start, stop in async_iter_latest_block_ranges(
            self.w3, self_from_block, self_to_block
        ):
            if None in (start, stop):
                yield []
            else:
                yield [
                    item
                    async for sublist in async_get_logs_multipart(
                        self.w3,
                        start,
                        stop,
                        self.address,
                        self.topics,
                        max_blocks=MAX_BLOCK_REQUEST,
                    )
                    for item in sublist
                ]

    async def get_logs(self) -> List[LogReceipt]:
        self_from_block = await self.from_block
        self_to_block = await self.to_block
        return [
            item
            async for sublist in async_get_logs_multipart(
                self.w3,
                self_from_block,
                self_to_block,
                self.address,
                self.topics,
                max_blocks=MAX_BLOCK_REQUEST,
            )
            for item in sublist
        ]


class AsyncRequestBlocks:
    def __init__(self, w3: "Web3") -> None:
        self.w3 = w3

    def __await__(self) -> Generator[Any, None, "AsyncRequestBlocks"]:
        async def closure() -> "AsyncRequestBlocks":
            self.block_number = await self.w3.bub.block_number  # type: ignore
            self.start_block = BlockNumber(self.block_number + 1)
            return self

        return closure().__await__()

    @property
    def filter_changes(self) -> AsyncIterator[List[Hash32]]:
        return self.get_filter_changes()

    async def get_filter_changes(self) -> AsyncIterator[List[Hash32]]:
        block_range_iter = async_iter_latest_block_ranges(
            self.w3, self.start_block, None
        )
        async for block_range in block_range_iter:
            hash = await async_block_hashes_in_range(self.w3, block_range)
            yield hash


async def async_block_hashes_in_range(
    w3: "Web3", block_range: Tuple[BlockNumber, BlockNumber]
) -> List[Union[None, Hash32]]:
    from_block, to_block = block_range
    if from_block is None or to_block is None:
        return []

    block_hashes = []
    for block_number in range(from_block, to_block + 1):
        w3_get_block = await w3.bub.get_block(BlockNumber(block_number))  # type: ignore
        block_hashes.append(getattr(w3_get_block, "hash", None))

    return block_hashes


async def async_local_filter_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], w3: "Web3"
) -> Callable[[RPCEndpoint, Any], Coroutine[Any, Any, RPCResponse]]:
    filters = {}
    filter_id_counter = map(to_hex, itertools.count())

    async def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if method in NEW_FILTER_METHODS:
            filter_id = next(filter_id_counter)

            _filter: Union[AsyncRequestLogs, AsyncRequestBlocks]
            if method == RPC.bub_newFilter:
                _filter = await AsyncRequestLogs(
                    w3, **apply_key_map(FILTER_PARAMS_KEY_MAP, params[0])
                )

            elif method == RPC.bub_newBlockFilter:
                _filter = await AsyncRequestBlocks(w3)

            else:
                raise NotImplementedError(method)

            filters[filter_id] = _filter
            return {"result": filter_id}

        elif method in FILTER_CHANGES_METHODS:
            filter_id = params[0]
            #  Pass through to filters not created by middleware
            if filter_id not in filters:
                return await make_request(method, params)
            _filter = filters[filter_id]

            if method == RPC.bub_getFilterChanges:
                changes = await _filter.filter_changes.__anext__()
                return {"result": changes}

            elif method == RPC.bub_getFilterLogs:
                # type ignored b/c logic prevents RequestBlocks which
                # doesn't implement get_logs
                logs = await _filter.get_logs()  # type: ignore
                return {"result": logs}
            else:
                raise NotImplementedError(method)
        else:
            return await make_request(method, params)

    return middleware
