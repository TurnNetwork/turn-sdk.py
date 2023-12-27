from typing import (
    Union,
)

from eth_typing import (
    NodeID,
    HexStr,
)
from eth_typing.evm import (
    Address,
)
from eth_utils import remove_0x_prefix

from bubble.inner_contract import (
    InnerContract,
)

from bubble.types import Wei, BlockIdentifier, InnerFunction


class Delegate(InnerContract):
    ADDRESS = '0x1000000000000000000000000000000000000002'

    def delegate(self,
                 node_id: Union[NodeID, HexStr],
                 balance_type: int,
                 amount: Wei,
                 ):
        """
        Delegate the amount to the node and get the reward from the node.

        :param node_id: id of the candidate node to delegate
        :param balance_type: delegate balance type, including: free balance: 0, restricting: 1, locked balance and restricting: 2
        :param amount: delegate amount
        """
        return self.function(InnerFunction.delegate_delegate,
                             balance_type=balance_type,
                             node_id=node_id,
                             amount=amount
                             )

    def withdrew_delegate(self,
                          node_id: Union[NodeID, HexStr],
                          staking_block_identifier: BlockIdentifier,
                          amount: Wei,
                          ):
        """
        Withdrew delegates from sending address,
        and when the remaining delegates amount is less than the minimum threshold, all delegates will be withdrawn.

        :param node_id: id of the node to withdrew delegate
        :param staking_block_identifier: the identifier of the staking block when delegate
        :param amount: withdrew amount
        """
        block = self.web3.bub.get_block(staking_block_identifier)
        return self.function(InnerFunction.delegate_withdrewDelegate,
                             block_number=block['number'],
                             node_id=node_id,
                             amount=amount,
                             )

    def redeem_delegate(self):
        """
        redeem all unlocked delegates.
        """
        return self.function(InnerFunction.delegate_redeemDelegate)

    def get_delegate_list(self, address: Address):
        """
        Get all delegate information of the address.
        """
        return self.function(InnerFunction.delegate_getDelegateList, address=address)

    def get_delegate_info(self,
                          address: Address,
                          node_id: Union[NodeID, HexStr],
                          staking_block_identifier: BlockIdentifier,
                          ):
        """
        Get delegate information of the address.

        :param address: delegate address
        :param node_id: id of the node that has been delegated
        :param staking_block_identifier: the identifier of the staking block when delegate
        """
        block = self.web3.bub.get_block(staking_block_identifier)
        return self.function(InnerFunction.delegate_getDelegateInfo,
                             block_number=block['number'],
                             address=address,
                             node_id=node_id,
                             )

    def get_delegate_lock_info(self, address: Address):
        """
        Get locked delegate information of the address.
        """
        return self.function(InnerFunction.delegate_getDelegateLockInfo, address=address)
