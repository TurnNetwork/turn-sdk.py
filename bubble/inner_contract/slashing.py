from typing import (
    Union,
)

from eth_typing import (
    NodeID,
    HexStr,
)

from bubble.types import (
    InnerFunction, BlockIdentifier,
)
from bubble.inner_contract import (
    InnerContract,
)


class Slashing(InnerContract):
    ADDRESS = '0x1000000000000000000000000000000000000004'

    def report_duplicate_sign(self, report_type: int, data: str):
        """
        Report a node signs the illegal consensus message after it signs the correct consensus message.

        :param report_type: duplicate sign type, prepareBlock: 1, prepareVote: 2, viewChange: 3
        :param data: a JSON string of evidence, format reference RPC bub_Evidences
        """
        return self.function(InnerFunction.slashing_reportDuplicateSign, report_type=report_type, data=data)

    def check_duplicate_sign(self,
                             report_type: int,
                             node_id: Union[NodeID, HexStr],
                             block_identifier: BlockIdentifier,
                             ):
        """
        get whether the node has been reported for duplicate-signed from someone

        :param report_type: duplicate sign type, prepareBlock: 1, prepareVote: 2, viewChange: 3
        :param node_id: node id to report
        :param block_identifier: duplicate-signed block identifier
        """
        block = self.web3.bub.get_block(block_identifier)
        return self.function(InnerFunction.slashing_checkDuplicateSign,
                             report_type=report_type,
                             node_id=node_id,
                             block_number=block['number'],
                             )
