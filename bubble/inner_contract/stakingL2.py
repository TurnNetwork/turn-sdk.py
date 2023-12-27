from typing import (
    Union,
)

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


class StakingL2(InnerContract):
    ADDRESS = '0x2000000000000000000000000000000000000001'

    def create_staking(self,
                       node_id: Union[NodeID, HexStr],
                       amount: Wei,
                       benefit_address: AnyAddress,
                       name: str,
                       detail: str,
                       electron_uri: URI,
                       p2p_uri: URI,
                       node_version: Version,
                       bls_pubkey: Union[BLSPubkey, HexStr],
                       is_operator: bool,
                       rpc_uri: URI,
                       ):
        """
        Staking a node to be candidate.
        """
        return self.function(InnerFunction.stakingL2_createStaking,
                             node_id=node_id,
                             amount=amount,
                             benefit_address=benefit_address,
                             name=name,
                             detail=detail,
                             electron_uri=electron_uri,
                             rpc_uri=rpc_uri,
                             p2p_uri=p2p_uri,
                             node_version=node_version,
                             bls_pubkey=bls_pubkey,
                             is_operator=is_operator,
                             )

    def edit_staking(self,
                     node_id: Union[NodeID, HexStr],
                     benefit_address: AnyAddress = None,
                     node_name: str = None,
                     detail: str = None,
                     rpc_uri: str = None,
                     ):
        """
        edit staking information.

        :param node_id: id of node that has been staking
        :param benefit_address: the address that accepts the staking reward
        :param external_id: custom external id, will be attached to the staking information
        :param node_name: custom node name, will be attached to the staking information
        :param website: custom node website, will be attached to the staking information
        :param details: custom node detail, will be attached to the staking information
        """
        return self.function(InnerFunction.stakingL2_editStaking,
                             node_id=node_id,
                             benefit_address=benefit_address,
                             node_name=node_name,
                             detail=detail,
                             rpc_uri=rpc_uri,
                             )

    # def increase_staking(self,
    #                      node_id: Union[NodeID, HexStr],
    #                      balance_type: int,
    #                      amount: Wei,
    #                      ):
    #     """
    #     Increase the amount of staking.

    #     :param balance_type: balance type of increase staking, including: 0: free balance, 1: restricting
    #     :param node_id: id of node that has been staking
    #     :param amount: increase staking amount
    #     """
    #     return self.function(InnerFunction.staking_increaseStaking,
    #                          node_id=node_id,
    #                          balance_type=balance_type,
    #                          amount=amount,
    #                          )

    def withdrew_staking(self, node_id: Union[NodeID, HexStr]):
        """
        Revoke the staking of the node and withdraw the staking amount.

        :param node_id: id of the node to be withdrew staking
        """
        return self.function(InnerFunction.stakingL2_withdrewStaking, node_id=node_id)

    def get_candidate_list(self):
        """
        Gets all staking node information.
        """
        return self.function(InnerFunction.stakingL2_getCandidateList)

    def get_candidate_info(self, node_id: Union[NodeID, HexStr]):
        """
        Get staking node information.

        :param node_id: staking node id
        """
        return self.function(InnerFunction.stakingL2_getCandidateInfo, node_id=node_id)

    # def get_block_reward(self):
    #     """
    #     get the current block reward, which is updated every epoch.
    #     """
    #     return self.function(InnerFunction.staking_getBlockReward)
    #
    # def get_staking_reward(self):
    #     """
    #     get the current staking reward, which is updated every epoch.
    #     """
    #     return self.function(InnerFunction.staking_getStakingReward)
    #
    # def get_avg_block_time(self):
    #     """
    #     Get the average block time over history.
    #     """
    #     return self.function(InnerFunction.staking_getAvgBlockTime)
