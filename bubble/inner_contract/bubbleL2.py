from typing import (
    Union,
)

from bubble.datastructures import AttributeDict
from eth_typing import (
    NodeID,
    URI,
    BLSPubkey,
    BLSSignature,
    HexStr,
    Decodable,
)
from eth_typing.evm import (
    AnyAddress,
)
from eth_utils import (
    remove_0x_prefix
)
from bubble.types import (
    InnerFunction,
)
from bubble.types import (
    Wei,
    Version,
    _Hash32,
)
from bubble.inner_contract import (
    InnerContract,
)


class BubbleL2(InnerContract):
    ADDRESS = '0x1000000000000000000000000000000000000020'

    def mint_token(self,
                   tx_hash: Union[bytes, HexStr],
                   address: AnyAddress,
                   amount: int,
                   tokens: [dict]):
        """
        After the user pledges a token on the main chain, the main chain operation node will initiate a coin trading to the corresponding bubble to cast tokens of the same currency and quantity.
        :param tokens:a list of token asset, for example:
        [{'token_address': '3aa4e6d933342648173f17cf8557a75850f29b59', 'amount': 10 * 10 ** 6}, {'token_address': '', 'amount': 20 * 10 ** 6}]
        """
        asset_data = []
        asset_data.append(bytes.fromhex(remove_0x_prefix(address)))
        asset_data.append(amount)
        for token in tokens:
            token['token_address'] = bytes.fromhex(remove_0x_prefix(token['token_address']))
        asset_data.append([list(token.values()) for token in tokens])

        return self.function(InnerFunction.bubbleL2_mintToken,
                             tx_hash=tx_hash,
                             acc_asset=asset_data)

    def settle_bubble(self):
        """
        After running the bubble for a period of time, settlement can be made to the main chain by calling the contract trading interface of this system.
        """
        return self.function(InnerFunction.bubbleL2_settleBubble)

    # def get_L2_hash_by_L1_hash(self, tx_hash: Union[bytes, HexStr]):
    #     """
    #     Obtain sub chain Hash based on the main chain Hash.
    #     """
    #     return self.function(InnerFunction.bubbleL2_getL2HashByL1Hash, tx_hash=tx_hash)

    def get_L2_hash_by_L1_hash(self, tx_hash: Union[bytes, HexStr]):
        """
        Obtain sub chain Hash based on the main chain Hash.
        """
        return self.function(InnerFunction.bubbleL2_getL2HashByL1Hash, tx_hash=tx_hash)
