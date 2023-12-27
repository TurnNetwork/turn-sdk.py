from eth_typing import HexStr, AnyAddress
from eth_utils import remove_0x_prefix

from bubble.types import InnerFunction
from bubble.inner_contract import (
    InnerContract,
)


class Reward(InnerContract):
    ADDRESS = '0x1000000000000000000000000000000000000006'

    def withdraw_delegate_reward(self):
        """
        withdraw all delegate rewards from sending address
        """
        return self.function(InnerFunction.reward_withdrawDelegateReward)

    def get_delegate_reward(self,
                            address: AnyAddress,
                            node_ids: [HexStr] = None,
                            ):
        """
        Get the delegate reward information of the address, it can be filtered by node id.
        """
        return self.function(InnerFunction.reward_getDelegateReward,
                             address=address,
                             node_ids=[bytes.fromhex(remove_0x_prefix(node_id)) for node_id in node_ids],
                             is_call=True,
                             )
