from typing import (
    Union
)

from eth_typing import (
    NodeID,
    HexStr,
)

from bubble.inner_contract.formatters import (
    InnerFunction,
)
from bubble.types import (
    Version,
    BlockIdentifier,
)
from bubble.inner_contract import (
    InnerContract,
)


class Proposal(InnerContract):
    ADDRESS = '0x1000000000000000000000000000000000000005'

    def submit_version_proposal(self,
                                node_id: Union[NodeID, HexStr],
                                pip_number: str,
                                version: Version,
                                voting_rounds: int,
                                ):
        """
        Submit a version proposal to promote version upgrade of the chain.

        :param node_id: the node id of the verifier who submitted the proposal
        :param pip_number: generally, it is the pull request id of github.com/BubbleNet/PIPs project
        :param version: the version you want to upgrade to
        :param voting_rounds: the number of voting consensus rounds, it will be converted to the block number,
            and the voting end block number will be 20 blocks earlier than this
        """
        return self.function(InnerFunction.proposal_submitVersionProposal,
                             node_id=node_id,
                             pip_number=pip_number,
                             version=version,
                             voting_rounds=voting_rounds,
                             )

    def submit_param_proposal(self,
                              node_id: Union[NodeID, HexStr],
                              pip_number: str,
                              module: str,
                              name: str,
                              value: str,
                              ):
        """
        Submit a parameter proposal to change the value of the governable parameter.
        Use 'self.govern_param_list' to get all governable parameters.

        :param node_id: the node id of the verifier who submitted the proposal
        :param pip_number: generally, it is the pull request id of github.com/BubbleNet/PIPs project
        :param module: the module to which the parameter belongs
        :param name: parameter name
        :param value: new parameter value
        """
        return self.function(InnerFunction.proposal_submitParamProposal,
                             node_id=node_id,
                             pip_number=pip_number,
                             module=module,
                             name=name,
                             value=value,
                             )

    def submit_text_proposal(self,
                             node_id: Union[NodeID, HexStr],
                             pip_number: str,
                             ):
        """
        Submit a text proposal to collect votes from verifiers.
        This proposal will not have any impact on the chain.

        :param node_id: the node id of the verifier who submitted the proposal
        :param pip_number: generally, it is the pull request id of github.com/BubbleNet/PIPs project
        """
        return self.function(InnerFunction.proposal_submitTextProposal, node_id=node_id, pip_number=pip_number)

    def submit_cancel_proposal(self,
                               node_id: Union[NodeID, HexStr],
                               pip_number: str,
                               voting_rounds: int,
                               proposal_id: Union[bytes, HexStr],
                               ):
        """
        Submit a cancel proposal to cancel another proposal.
        The proposal to be cancelled must be during the voting period, and is not a text proposal or a cancel proposal.

        :param node_id: the node id of the verifier who submitted the proposal
        :param pip_number: generally, it is the pull request id of github.com/BubbleNet/PIPs project
        :param voting_rounds: the number of voting consensus rounds, it will be converted to the block number,
            and the voting end block number will be 20 blocks earlier than this
        :param proposal_id: hash id of the proposal to be cancelled
        """
        return self.function(InnerFunction.proposal_submitCancelProposal,
                             node_id=node_id,
                             pip_number=pip_number,
                             voting_rounds=voting_rounds,
                             proposal_id=proposal_id,
                             )

    def vote(self,
             node_id: Union[NodeID, HexStr],
             proposal_id: Union[bytes, HexStr],
             option: int,
             node_version: Version,
             version_sign: Union[bytes, HexStr],
             ):
        """
        To vote on a proposal, the proposal must be in the voting period.
        When the voting conditions are met, the proposal will be passed and become effective.

        :param node_id: the node id of the verifier who submitted the vote
        :param proposal_id: hash id of the proposal to be voted on
        :param option: voting option, include: Yeas: 1, Nays: 2, Abstentions: 3
        :param node_version: node version, obtained by rpc 'admin_getProgramVersion' interface
        :param version_sign: node version signature, obtained by rpc 'admin_getProgramVersion' interface
        """
        return self.function(InnerFunction.proposal_vote,
                             node_id=node_id,
                             proposal_id=proposal_id,
                             option=option,
                             node_version=node_version,
                             version_sign=version_sign,
                             )

    def declare_version(self,
                        node_id: Union[NodeID, HexStr],
                        node_version: Version,
                        version_sign: Union[bytes, HexStr],
                        ):
        """
        Declare the version of the node to the chain.
        When the node version is the same as the current version of the blockchain,
        the node will be able to participate in the consensus.

        :param node_id: the node id of the candidate who submitted the version declare
        :param node_version: node version, obtained by rpc 'admin_getProgramVersion' interface
        :param version_sign: node version signature, obtained by rpc 'admin_getProgramVersion' interface
        """
        return self.function(InnerFunction.proposal_declareVersion,
                             node_id=node_id,
                             node_version=node_version,
                             version_sign=version_sign,
                             )

    def get_proposal(self, proposal_id: Union[bytes, HexStr]):
        """
        Get details of the proposal

        :param proposal_id: hash id of the proposal
        """
        return self.function(InnerFunction.proposal_getProposal, proposal_id=proposal_id)

    def get_proposal_votes(self,
                           proposal_id: Union[bytes, HexStr],
                           block_identifier: BlockIdentifier = 'latest',
                           ):
        """
        Get the voting information for the proposal based on the block identifier.

        :param proposal_id: hash id of the proposal
        :param block_identifier: block identifier
        """
        block = self.web3.bub.get_block(block_identifier)
        return self.function(InnerFunction.proposal_getProposalVotes,
                             proposal_id=proposal_id,
                             block_hash=block['hash'],
                             )

    def get_proposal_result(self, proposal_id: Union[bytes, HexStr]):
        """
        Get proposal results, you can query only after the proposal is complete.
        use 'self.get_proposal_votes' to get current voting information.

        :param proposal_id: proposal id
        """
        return self.function(InnerFunction.proposal_getProposalResult, proposal_id=proposal_id)

    def proposal_list(self):
        """
        Get proposal list for the chain
        """
        return self.function(InnerFunction.proposal_proposalList)

    def get_chain_version(self):
        """
        Query the chain effective version of the node
        """
        return self.function(InnerFunction.proposal_getChainVersion)

    def get_govern_param(self, module: str, name: str):
        """
        Get the current value of the governable parameter
        Use 'self.govern_param_list' to get all governable parameters.

        :param module: the module to which the parameter belongs
        :param name: parameter name
        """
        return self.function(InnerFunction.proposal_getGovernParam, module=module, name=name)

    def govern_param_list(self, module: str = ''):
        """
        get all governable parameters.

        :param module: optionally, specify a module name
        """
        return self.function(InnerFunction.proposal_governParamList, module=module)
