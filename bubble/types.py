from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    NewType,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    Hash32,
    HexStr,
)
from hexbytes import (
    HexBytes,
)

from bubble._utils.compat import (
    Literal,
    TypedDict,
)
from bubble._utils.function_identifiers import (
    FallbackFn,
    ReceiveFn,
)
from bubble.datastructures import (
    NamedElementOnion,
)


if TYPE_CHECKING:
    from bubble.contract.async_contract import AsyncContractFunction  # noqa: F401
    from bubble.contract.contract import ContractFunction  # noqa: F401
    from bubble.main import (  # noqa: F401
        AsyncWeb3,
        Web3,
    )

TReturn = TypeVar("TReturn")
TParams = TypeVar("TParams")
TValue = TypeVar("TValue")

BlockParams = Literal["latest", "earliest", "pending", "safe", "finalized"]
BlockIdentifier = Union[BlockParams, BlockNumber, Hash32, HexStr, HexBytes, int]
LatestBlockParam = Literal["latest"]

FunctionIdentifier = Union[str, Type[FallbackFn], Type[ReceiveFn]]

Version = NewType('Version', int)

# bytes, hexbytes, or hexstr representing a 32 byte hash
_Hash32 = Union[Hash32, HexBytes, HexStr]
EnodeURI = NewType("EnodeURI", str)
ENS = NewType("ENS", str)
Nonce = NewType("Nonce", int)
RPCEndpoint = NewType("RPCEndpoint", str)
Timestamp = NewType("Timestamp", int)
Wei = NewType("Wei", int)
Gwei = NewType("Gwei", int)
Formatters = Dict[RPCEndpoint, Callable[..., Any]]


class AccessListEntry(TypedDict):
    address: HexStr
    storageKeys: Sequence[HexStr]


AccessList = NewType("AccessList", Sequence[AccessListEntry])


# todo: move these to eth_typing once bubble is type hinted
class ABIEventParams(TypedDict, total=False):
    indexed: bool
    name: str
    type: str


class ABIEvent(TypedDict, total=False):
    anonymous: bool
    inputs: Sequence["ABIEventParams"]
    name: str
    type: Literal["event"]


class ABIFunctionComponents(TypedDict, total=False):
    # better typed as Sequence['ABIFunctionComponents'], but recursion isnt possible yet
    # https://github.com/python/mypy/issues/731
    components: Sequence[Any]
    name: str
    type: str


class ABIFunctionParams(TypedDict, total=False):
    components: Sequence["ABIFunctionComponents"]
    name: str
    type: str


class ABIFunction(TypedDict, total=False):
    constant: bool
    inputs: Sequence["ABIFunctionParams"]
    name: str
    outputs: Sequence["ABIFunctionParams"]
    payable: bool
    stateMutability: Literal["pure", "view", "nonpayable", "payable"]
    type: Literal["function", "constructor", "fallback", "receive"]


ABIElement = Union[ABIFunction, ABIEvent]
ABI = Sequence[Union[ABIFunction, ABIEvent]]


class EventData(TypedDict):
    address: ChecksumAddress
    args: Dict[str, Any]
    blockHash: HexBytes
    blockNumber: int
    event: str
    logIndex: int
    transactionHash: HexBytes
    transactionIndex: int


FunctionNumber = NewType('FunctionNumber', int)


class InnerFunction:
    # staking
    staking_createStaking = FunctionNumber(1000)
    staking_editStaking = FunctionNumber(1001)
    staking_increaseStaking = FunctionNumber(1002)
    staking_withdrewStaking = FunctionNumber(1003)
    staking_getVerifierList = FunctionNumber(1100)
    staking_getValidatorList = FunctionNumber(1101)
    staking_getCandidateList = FunctionNumber(1102)
    staking_getCandidateInfo = FunctionNumber(1105)
    staking_getBlockReward = FunctionNumber(1200)
    staking_getStakingReward = FunctionNumber(1201)
    staking_getAvgBlockTime = FunctionNumber(1202)
    # stakingL2
    stakingL2_createStaking = FunctionNumber(7000)
    stakingL2_editStaking = FunctionNumber(7001)
    stakingL2_withdrewStaking = FunctionNumber(7003)
    stakingL2_getCandidateList = FunctionNumber(7102)
    stakingL2_getCandidateInfo = FunctionNumber(7103)
    # bubble
    # bubble_createBubble = FunctionNumber(8001)
    # bubble_releaseBubble = FunctionNumber(8002)
    # bubble_getBubbleInfo = FunctionNumber(8100)
    # bubble_depositToken = FunctionNumber(8003)
    # bubble_withdrewToken = FunctionNumber(8004)
    # bubble_getL1HashByL2Hash = FunctionNumber(8101)
    # bubble_getBubTxHashList = FunctionNumber(8102)
    # bubble_settleBubble = FunctionNumber(8005)

    bubble_selectBubble = FunctionNumber(8001)
    bubble_getBubbleInfo = FunctionNumber(8100)
    bubble_depositToken = FunctionNumber(8003)
    bubble_withdrewToken = FunctionNumber(8004)
    bubble_remoteDeploy = FunctionNumber(8006)
    bubble_remoteCall = FunctionNumber(8007)
    bubble_remoteCallExecutor = FunctionNumber(8008)
    bubble_remoteRemove = FunctionNumber(8009)
    bubble_getL1HashByL2Hash = FunctionNumber(8101)
    bubble_getBubTxHashList = FunctionNumber(8102)
    bubble_settleBubble = FunctionNumber(8005)

    # bubbleL2
    bubbleL2_mintToken = FunctionNumber(6000)
    bubbleL2_settleBubble = FunctionNumber(6001)
    bubbleL2_getL2HashByL1Hash = FunctionNumber(6100)
    #tempPrikey
    tempPrikey_bindTempPrivateKey = FunctionNumber(7200)
    tempPrikey_behalfSignature = FunctionNumber(7201)
    tempPrikey_invalidateTempPrivateKey = FunctionNumber(7202)
    tempPrikey_addLineOfCredit = FunctionNumber(7203)
    tempPrikey_getLineOfCredit = FunctionNumber(7204)
    # delegate
    delegate_delegate = FunctionNumber(1004)
    delegate_withdrewDelegate = FunctionNumber(1005)
    delegate_redeemDelegate = FunctionNumber(1006)
    delegate_getDelegateList = FunctionNumber(1103)
    delegate_getDelegateInfo = FunctionNumber(1104)
    delegate_getDelegateLockInfo = FunctionNumber(1106)
    # reward
    reward_withdrawDelegateReward = FunctionNumber(5000)
    reward_getDelegateReward = FunctionNumber(5100)
    # proposal
    proposal_submitTextProposal = FunctionNumber(2000)
    proposal_submitVersionProposal = FunctionNumber(2001)
    proposal_submitParamProposal = FunctionNumber(2002)
    proposal_vote = FunctionNumber(2003)
    proposal_declareVersion = FunctionNumber(2004)
    proposal_submitCancelProposal = FunctionNumber(2005)
    proposal_getProposal = FunctionNumber(2100)
    proposal_getProposalResult = FunctionNumber(2101)
    proposal_proposalList = FunctionNumber(2102)
    proposal_getChainVersion = FunctionNumber(2103)
    proposal_getGovernParam = FunctionNumber(2104)
    proposal_getProposalVotes = FunctionNumber(2105)
    proposal_governParamList = FunctionNumber(2106)
    # slashing
    slashing_reportDuplicateSign = FunctionNumber(3000)
    slashing_checkDuplicateSign = FunctionNumber(3001)
    slashing_zeroProduceNodeList = FunctionNumber(3002)
    # restricting
    restricting_createRestricting = FunctionNumber(4000)
    restricting_getRestrictingInfo = FunctionNumber(4100)


class RLPEventData(TypedDict):
    code: int
    message: str
    data: Optional[Any]


class RPCError(TypedDict):
    code: int
    message: str
    data: Optional[str]


class RPCResponse(TypedDict, total=False):
    error: Union[RPCError, str]
    id: int
    jsonrpc: Literal["2.0"]
    result: Any


Middleware = Callable[[Callable[[RPCEndpoint, Any], RPCResponse], "Web3"], Any]
AsyncMiddlewareCoroutine = Callable[
    [RPCEndpoint, Any], Coroutine[Any, Any, RPCResponse]
]
AsyncMiddleware = Callable[
    [Callable[[RPCEndpoint, Any], RPCResponse], "AsyncWeb3"], Any
]
MiddlewareOnion = NamedElementOnion[str, Middleware]
AsyncMiddlewareOnion = NamedElementOnion[str, AsyncMiddleware]


class FormattersDict(TypedDict, total=False):
    error_formatters: Optional[Formatters]
    request_formatters: Optional[Formatters]
    result_formatters: Optional[Formatters]


class FilterParams(TypedDict, total=False):
    address: Union[Address, ChecksumAddress, List[Address], List[ChecksumAddress]]
    blockHash: HexBytes
    fromBlock: BlockIdentifier
    toBlock: BlockIdentifier
    topics: Sequence[Optional[Union[_Hash32, Sequence[_Hash32]]]]


class FeeHistory(TypedDict):
    baseFeePerGas: List[Wei]
    gasUsedRatio: List[float]
    oldestBlock: BlockNumber
    reward: List[List[Wei]]


class LogReceipt(TypedDict):
    address: ChecksumAddress
    blockHash: HexBytes
    blockNumber: BlockNumber
    data: HexStr
    logIndex: int
    payload: HexBytes
    removed: bool
    topic: HexBytes
    topics: Sequence[HexBytes]
    transactionHash: HexBytes
    transactionIndex: int


# syntax b/c "from" keyword not allowed w/ class construction
TxData = TypedDict(
    "TxData",
    {
        "accessList": AccessList,
        "blockHash": HexBytes,
        "blockNumber": BlockNumber,
        "chainId": int,
        "data": Union[bytes, HexStr],
        "from": ChecksumAddress,
        "gas": int,
        "gasPrice": Wei,
        "maxFeePerGas": Wei,
        "maxPriorityFeePerGas": Wei,
        "hash": HexBytes,
        "input": HexStr,
        "nonce": Nonce,
        "r": HexBytes,
        "s": HexBytes,
        "to": ChecksumAddress,
        "transactionIndex": int,
        "type": Union[int, HexStr],
        "v": int,
        "value": Wei,
    },
    total=False,
)

# syntax b/c "from" keyword not allowed w/ class construction
TxParams = TypedDict(
    "TxParams",
    {
        "chainId": int,
        "data": Union[bytes, HexStr],
        # addr or ens
        "from": Union[Address, ChecksumAddress, str],
        "gas": int,
        # legacy pricing
        "gasPrice": Wei,
        # dynamic fee pricing
        "maxFeePerGas": Union[str, Wei],
        "maxPriorityFeePerGas": Union[str, Wei],
        "nonce": Nonce,
        # addr or ens
        "to": Union[Address, ChecksumAddress, str],
        "type": Union[int, HexStr],
        "value": Wei,
    },
    total=False,
)

WithdrawalData = TypedDict(
    "WithdrawalData",
    {
        "index": int,
        "validator_index": int,
        "address": ChecksumAddress,
        "amount": Gwei,
    },
)

CallOverrideParams = TypedDict(
    "CallOverrideParams",
    {
        "balance": Optional[Wei],
        "nonce": Optional[int],
        "code": Optional[Union[bytes, HexStr]],
        "state": Optional[Dict[HexStr, HexStr]],
        "stateDiff": Optional[Dict[HexStr, HexStr]],
    },
    total=False,
)

CallOverride = Dict[ChecksumAddress, CallOverrideParams]

GasPriceStrategy = Union[
    Callable[["Web3", TxParams], Wei], Callable[["AsyncWeb3", TxParams], Wei]
]

# syntax b/c "from" keyword not allowed w/ class construction
TxReceipt = TypedDict(
    "TxReceipt",
    {
        "blockHash": HexBytes,
        "blockNumber": BlockNumber,
        "contractAddress": Optional[ChecksumAddress],
        "cumulativeGasUsed": int,
        "effectiveGasPrice": Wei,
        "gasUsed": int,
        "from": ChecksumAddress,
        "logs": List[LogReceipt],
        "logsBloom": HexBytes,
        "root": HexStr,
        "status": int,
        "to": ChecksumAddress,
        "transactionHash": HexBytes,
        "transactionIndex": int,
    },
)


class SignedTx(TypedDict, total=False):
    raw: bytes
    tx: TxParams


class StorageProof(TypedDict):
    key: HexStr
    proof: Sequence[HexStr]
    value: HexBytes


class MerkleProof(TypedDict):
    address: ChecksumAddress
    accountProof: Sequence[HexStr]
    balance: int
    codeHash: HexBytes
    nonce: Nonce
    storageHash: HexBytes
    storageProof: Sequence[StorageProof]


class Protocol(TypedDict):
    difficulty: int
    head: HexStr
    network: int
    version: int


class NodeInfo(TypedDict):
    enode: EnodeURI
    id: HexStr
    ip: str
    listenAddr: str
    name: str
    ports: Dict[str, int]
    protocols: Dict[str, Protocol]


class Peer(TypedDict, total=False):
    caps: Sequence[str]
    id: HexStr
    name: str
    network: Dict[str, str]
    protocols: Dict[str, Protocol]


class SyncStatus(TypedDict):
    currentBlock: int
    highestBlock: int
    knownStates: int
    pulledStates: int
    startingBlock: int


class BlockData(TypedDict, total=False):
    baseFeePerGas: Wei
    difficulty: int
    extraData: HexBytes
    gasLimit: int
    gasUsed: int
    hash: HexBytes
    logsBloom: HexBytes
    miner: ChecksumAddress
    mixHash: HexBytes
    nonce: HexBytes
    number: BlockNumber
    parentHash: HexBytes
    receiptsRoot: HexBytes
    sha3Uncles: HexBytes
    size: int
    stateRoot: HexBytes
    timestamp: Timestamp
    totalDifficulty: int
    transactions: Union[Sequence[HexBytes], Sequence[TxData]]
    transactionsRoot: HexBytes
    uncles: Sequence[HexBytes]
    withdrawals: Sequence[WithdrawalData]
    withdrawalsRoot: HexBytes

    # node_poa_middleware replaces extraData w/ proofOfAuthorityData
    proofOfAuthorityData: HexBytes


class Uncle(TypedDict):
    author: ChecksumAddress
    difficulty: HexStr
    extraData: HexStr
    gasLimit: HexStr
    gasUsed: HexStr
    hash: HexBytes
    logsBloom: HexStr
    miner: HexBytes
    mixHash: HexBytes
    nonce: HexStr
    number: HexStr
    parentHash: HexBytes
    receiptsRoot: HexBytes
    sealFields: Sequence[HexStr]
    sha3Uncles: HexBytes
    size: int
    stateRoot: HexBytes
    timestamp: Timestamp
    totalDifficulty: HexStr
    transactions: Sequence[HexBytes]
    transactionsRoot: HexBytes
    uncles: Sequence[HexBytes]


#
# txpool types
#

# syntax b/c "from" keyword not allowed w/ class construction
PendingTx = TypedDict(
    "PendingTx",
    {
        "blockHash": HexBytes,
        "blockNumber": None,
        "from": ChecksumAddress,
        "gas": HexBytes,
        "maxFeePerGas": HexBytes,
        "maxPriorityFeePerGas": HexBytes,
        "gasPrice": HexBytes,
        "hash": HexBytes,
        "input": HexBytes,
        "nonce": HexBytes,
        "to": ChecksumAddress,
        "transactionIndex": None,
        "value": HexBytes,
    },
    total=False,
)


class TxPoolContent(TypedDict, total=False):
    pending: Dict[ChecksumAddress, Dict[Nonce, List[PendingTx]]]
    queued: Dict[ChecksumAddress, Dict[Nonce, List[PendingTx]]]


class TxPoolInspect(TypedDict, total=False):
    pending: Dict[ChecksumAddress, Dict[Nonce, str]]
    queued: Dict[ChecksumAddress, Dict[Nonce, str]]


class TxPoolStatus(TypedDict, total=False):
    pending: int
    queued: int


#
# bubble.bub types
#


class BubWallet(TypedDict):
    accounts: Sequence[Dict[str, str]]
    status: str
    url: str


# Contract types

TContractFn = TypeVar("TContractFn", "ContractFunction", "AsyncContractFunction")

# Tracing types
BlockTrace = NewType("BlockTrace", Dict[str, Any])
FilterTrace = NewType("FilterTrace", Dict[str, Any])
TraceMode = Sequence[Literal["trace", "vmTrace", "stateDiff"]]


class TraceFilterParams(TypedDict, total=False):
    after: int
    count: int
    fromAddress: Sequence[Union[Address, ChecksumAddress, ENS]]
    fromBlock: BlockIdentifier
    toAddress: Sequence[Union[Address, ChecksumAddress, ENS]]
    toBlock: BlockIdentifier
