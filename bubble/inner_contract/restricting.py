from eth_typing import AnyAddress

from bubble.types import InnerFunction
from bubble.inner_contract import (
    InnerContract,
)


class Restricting(InnerContract):
    ADDRESS = '0x1000000000000000000000000000000000000001'

    def create_restricting(self,
                           release_address: AnyAddress,
                           plans: [dict],
                           ):
        """
        Create a restricting

        :param release_address: released to account
        :param plans: a list of restricting plan, for example:
            [{'Epoch': 2, 'Amount': Web3.toWei(1, 'ether')}, {'Epoch': 8, 'Amount': Web3.toWei(3, 'ether')}]

            restricting plan is defined as follows:
            {
                Epoch: int   # the amount will be released to release address when the epoch ends
                Amount: Wei  # restricting amount
            }
        """
        return self.function(InnerFunction.restricting_createRestricting,
                             release_address=release_address,
                             plans=[list(plan.values()) for plan in plans],
                             )

    def get_restricting_info(self, release_address: AnyAddress):
        """
        Get the restricting information.

        :param release_address: release address for the restricting
        """
        return self.function(InnerFunction.restricting_getRestrictingInfo, release_address=release_address)
