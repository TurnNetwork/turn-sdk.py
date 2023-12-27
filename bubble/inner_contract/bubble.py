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
)
from bubble.inner_contract import (
    InnerContract,
)


class Bubble(InnerContract):
    ADDRESS = '0x2000000000000000000000000000000000000002'

    def select_bubble(self):
        """
        create a bubble chain.
        """
        return self.function(InnerFunction.bubble_selectBubble)

    def get_bubble_info(self, bubble_id: int):
        """
        get bubble info.
        """
        return self.function(InnerFunction.bubble_getBubbleInfo, bubble_id=bubble_id)

    def remote_deploy(self, bubble_id: int, address: AnyAddress, amount: int, data: bytes):
        """
        remote deploy
        """
        return self.function(InnerFunction.bubble_remoteDeploy, bubble_id=bubble_id, address=address, amount=amount,
                             data=data)

    def remote_call(self, bubble_id: int, address: AnyAddress, data: bytes):
        """
        get bubble info.
        """
        return self.function(InnerFunction.bubble_call, bubble_id=bubble_id, address=address, data=data)

    def remote_remove(self, bubble_id: int, address: AnyAddress):
        """
        get bubble info.
        """
        return self.function(InnerFunction.bubble_remoteRemove, bubble_id=bubble_id, address=address)

    def deposit_token(self, bubble_id: int, address: AnyAddress, amount: int, tokens: [dict]):
        """
        Staking token
        :param bubble_id:
        :param address:
        :param amount:
        :param tokens:a list of token asset, for example:
            [{'token_address': '', 'amount': 10 * 10 ** 6}, {'token_address': '', 'amount': 20 * 10 ** 6}]
        """
        asset_data = []
        asset_data.append(bytes.fromhex(remove_0x_prefix(address)))
        asset_data.append(amount)
        for token in tokens:
            token['token_address'] = bytes.fromhex(remove_0x_prefix(token['token_address']))
        asset_data.append([list(token.values()) for token in tokens])

        return self.function(InnerFunction.bubble_depositToken,
                             bubble_id=bubble_id,
                             acc_asset=asset_data
                             )

    def withdrew_token(self, bubble_id: int):
        """
        withdrew token.
        :param bubble_id: id of the bubble to be withdrew token
        """
        return self.function(InnerFunction.bubble_withdrewToken,
                             bubble_id=bubble_id)

    def settle_bubble(self,
                      tx_hash: Union[bytes, HexStr],
                      bubble_id: int,
                      settlement_info: [dict]):
        """
        The sub chain operation node submits settlement information to the main chain by calling this
        interface of the main chain operation node.

        :param tx_hash: Layer 1 settle bubble.
        :param settlement_info: List containing multiple account assets.
        [
        {'address': '', 'native_amount': '', 'tokens': [{'token_address': '', 'amount': 10 * 10 ** 6}, {'token_address': '', 'Amount': 20 * 10 ** 6}]},
        {'address': '', 'native_amount': '', 'tokens': [{'token_address': '', 'amount': 10 * 10 ** 6}, {'token_address': '', 'Amount': 20 * 10 ** 6}]},
        ]
        """
        settlement_data = []
        for account_asset in settlement_info:
            for token in account_asset['tokens']:
                token['token_address'] = bytes.fromhex(remove_0x_prefix(token['token_address']))
            tokens = [list(token.values()) for token in account_asset['tokens']]
            account_asset = [bytes.fromhex(account_asset['address']), account_asset['native_amount'], tokens]
            settlement_data.append(account_asset)

        return self.function(InnerFunction.bubble_settleBubble,
                             tx_hash=tx_hash,
                             bubble_id=bubble_id,
                             settlement_info=settlement_data)

    def get_origin_tx(self,
                      bubble_id: int,
                      tx_hash: Union[bytes, HexStr]):
        """
        Query the main chain hash based on the sub chain hash.
        :param bubble_id:
        :param tx_hash: Subchain Transaction Hash
        """
        return self.function(InnerFunction.bubble_getL1HashByL2Hash,
                             bubble_id=bubble_id,
                             tx_hash=tx_hash)

    def get_tx_records(self,
                       bubble_id: int,
                       tx_type: int):
        """
        Obtain the transaction hash list of the Bubble network on the main chain.
        :param txType: Bubble transaction type：0：StakingToken，1：WithdrewToken，2：SettleBubble
        """
        return self.function(InnerFunction.bubble_getBubTxHashList,
                             bubble_id=bubble_id,
                             tx_type=tx_type)

    def get_L1_hash_by_L2_hash(self, bubble_id: int, tx_hash: Union[bytes, HexStr]):
        """
        Obtain main chain Hash based on the sub chain Hash.
        """
        return self.function(InnerFunction.bubble_getL1HashByL2Hash, bubble_id=bubble_id, tx_hash=tx_hash)
