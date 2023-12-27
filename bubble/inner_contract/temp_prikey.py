import rlp

from eth_typing.evm import (
    AnyAddress,
)
from bubble.types import (
    InnerFunction,
)

from bubble.inner_contract import (
    InnerContract,
)


class TempPrivateKey(InnerContract):
    ADDRESS = '0x1000000000000000000000000000000000000021'

    def bind_temp_pri_key(self,
                          game_contract_address: AnyAddress,
                          temp_address: AnyAddress,
                          period: int,
                          ):
        """
        Bind the temporary address of the work address to one of the sections of the game.
        """
        return self.function(InnerFunction.tempPrikey_bindTempPrivateKey,
                             game_contract_address=game_contract_address,
                             temp_address=temp_address,
                             period=period,
                             )

    def behalf_signature(self,
                         work_address: AnyAddress,
                         game_contract_address: AnyAddress,
                         period: bytes,
                         call_data: bytes,
                         ):
        """
        During a certain segment of the game, the temporary address agent signs the transaction by working address,
        and the contract owner pays the gas fee
        """
        # data = []
        # for input_value in call_data:
        #     data.append(rlp.encode(input_value))
        # rlp.encode(call_data)

        return self.function(InnerFunction.tempPrikey_behalfSignature,
                             work_address=work_address,
                             game_contract_address=game_contract_address,
                             period=period,
                             call_data=call_data,
                             )

    def invalidate_temp_private_key(self,
                                    game_contract_address: AnyAddress,
                                    temp_address: AnyAddress,
                                    ):
        """
        Dissolves the binding between the working address and the temporary address for a section of the game process.
        """
        return self.function(InnerFunction.tempPrikey_invalidateTempPrivateKey,
                             game_contract_address=game_contract_address,
                             temp_address=temp_address,
                             )

    def add_line_of_credit(self,
                           game_contract_address: AnyAddress,
                           work_address: AnyAddress,
                           add_value: int
                           ):
        """
        After the credit limit of the player is used up, the game operator will increase the credit limit for the player.
        """
        return self.function(InnerFunction.tempPrikey_addLineOfCredit,
                             game_contract_address=game_contract_address,
                             work_address=work_address,
                             add_value=add_value,
                             )

    def get_line_of_credit(self,
                           game_contract_address: AnyAddress,
                           ):
        """
        Check the player's remaining credit line.
        """
        return self.function(InnerFunction.tempPrikey_getLineOfCredit,
                             game_contract_address=game_contract_address)

