from eth_utils.curried import (
    apply_formatters_to_dict,
    apply_formatter_if,
)

from bubble._utils.method_formatters import (
    to_integer_if_hex,
    to_integer_if_bytes,
    to_hex_if_bytes,
    apply_list_to_array_formatter,
    is_not_null,

)

from bubble.types import (
    InnerFunction,
)
from bubble._utils.normalizers import (
    abi_bytes_to_bytes,
    abi_address_to_bytes,
)

DEFAULT_PARAM_NORMALIZERS = [
    abi_bytes_to_bytes,
    abi_address_to_bytes,
]

DEFAULT_PARAM_ABIS = {
    'address': 'address',
    'node_id': 'bytes',
    'proposal_id': 'bytes',
}

CREATE_STAKING_PARAM_ABIS = {
    'benefit_address': 'address',
    'node_id': 'bytes',
    'version_sign': 'bytes',
    'bls_pubkey': 'bytes',
    'bls_proof': 'bytes',
}

CREATE_STAKING_L2_PARAM_ABIS = {
    'benefit_address': 'address',
    'node_id': 'bytes',
    'version_sign': 'bytes',
    'bls_pubkey': 'bytes',
    'bls_proof': 'bytes',
}

EDIT_CANDIDATE_PARAM_ABIS = {
    'benefit_address': 'address',
    'node_id': 'bytes',
}

EDIT_CANDIDATE_L2_PARAM_ABIS = {
    'benefit_address': 'address',
    'node_id': 'bytes',
}

WITHDREW_STAKING_L2_PARAM_ABIS = {
    'node_id': 'bytes',
}

CANDI_DATE_L2_PARAM_ABIS = {
    'node_id': 'bytes',
}

SETTLE_BUBBLE_PARAM_ABIS = {
    'tx_hash': 'bytes',
}

GET_L1HASH_BY_L2HASH_PARAM_ABIS = {
    'tx_hash': 'bytes',
}

MINT_TOKEN_PARAM_ABIS = {
    'tx_hash': 'bytes',
    'address': 'address',
}

GET_L2HASH_BY_L1HASH_PARAM_ABIS = {
    'tx_hash': 'bytes',
}

GET_DELEGATE_LIST_PARAM_ABIS = {
    'delegate_address': 'address',
}

GET_DELEGATE_INFO_PARAM_ABIS = {
    'delegate_address': 'address',
}

GET_DELEGATE_LOCK_INFO_PARAM_ABIS = {
    'delegate_address': 'address',
}

VOTE_PARAM_ABIS = {
    'version_sign': 'bytes',
}

DECLARE_VERSION_PARAM_ABIS = {
    'version_sign': 'bytes',
}

CREATE_RESTRICTING_PARAM_ABIS = {
    'release_address': 'address',
}

GET_RESTRICTING_INFO_PARAM_ABIS = {
    'release_address': 'address',
}

BIND_TEMP_PRIVATE_KEY_PARAM_ABIS = {
    'game_contract_address': 'address',
    'temp_address': 'address',
}

BEHALF_SIGNATURE_PARAM_ABIS = {
    'game_contract_address': 'address',
    'work_address': 'address',
}

INVALIDATE_TEMP_PRIVATE_KEY_PARAM_ABIS = {
    'game_contract_address': 'address',
    'temp_address': 'address',
}

ADD_LINE_OF_CREDIT_PARAM_ABIS = {
    'game_contract_address': 'address',
    'work_address': 'address',
}

GET_LINE_OF_CREDIT_PARAM_ABIS = {
    'game_contract_address': 'address',
    'work_address': 'address',
}

INNER_CONTRACT_PARAM_ABIS = {
    # restricting
    InnerFunction.restricting_createRestricting: CREATE_RESTRICTING_PARAM_ABIS,
    InnerFunction.restricting_getRestrictingInfo: GET_RESTRICTING_INFO_PARAM_ABIS,
    # staking
    InnerFunction.staking_createStaking: CREATE_STAKING_PARAM_ABIS,
    InnerFunction.staking_editStaking: EDIT_CANDIDATE_PARAM_ABIS,
    InnerFunction.delegate_getDelegateList: GET_DELEGATE_LIST_PARAM_ABIS,
    InnerFunction.delegate_getDelegateInfo: GET_DELEGATE_INFO_PARAM_ABIS,
    InnerFunction.delegate_getDelegateLockInfo: GET_DELEGATE_LOCK_INFO_PARAM_ABIS,
    # stakingL2
    InnerFunction.stakingL2_createStaking: CREATE_STAKING_L2_PARAM_ABIS,
    InnerFunction.stakingL2_editStaking: EDIT_CANDIDATE_L2_PARAM_ABIS,
    InnerFunction.stakingL2_withdrewStaking: WITHDREW_STAKING_L2_PARAM_ABIS,
    InnerFunction.stakingL2_getCandidateInfo: CANDI_DATE_L2_PARAM_ABIS,
    # bubble
    # InnerFunction.bubble_settleBubble: SETTLE_BUBBLE_PARAM_ABIS,
    InnerFunction.bubble_getL1HashByL2Hash: GET_L1HASH_BY_L2HASH_PARAM_ABIS,
    # InnerFunction.bubble_depositToken:
    # InnerFunction.bubble_settleBubble:
    # InnerFunction.bubble_getL1HashByL2Hash:
    # bubblel2
    InnerFunction.bubbleL2_mintToken: MINT_TOKEN_PARAM_ABIS,
    InnerFunction.bubbleL2_getL2HashByL1Hash: GET_L2HASH_BY_L1HASH_PARAM_ABIS,
    #temp_prikey
    InnerFunction.tempPrikey_bindTempPrivateKey: BIND_TEMP_PRIVATE_KEY_PARAM_ABIS,
    InnerFunction.tempPrikey_behalfSignature: BEHALF_SIGNATURE_PARAM_ABIS,
    InnerFunction.tempPrikey_invalidateTempPrivateKey: INVALIDATE_TEMP_PRIVATE_KEY_PARAM_ABIS,
    InnerFunction.tempPrikey_addLineOfCredit: ADD_LINE_OF_CREDIT_PARAM_ABIS,
    InnerFunction.tempPrikey_getLineOfCredit: GET_LINE_OF_CREDIT_PARAM_ABIS,
    # govern
    InnerFunction.proposal_vote: VOTE_PARAM_ABIS,
    InnerFunction.proposal_declareVersion: DECLARE_VERSION_PARAM_ABIS,
}



RESTRICTING_PLAN_FORMATTER = {
    'amount': to_integer_if_hex,
}

restricting_plan_formatter = apply_formatters_to_dict(RESTRICTING_PLAN_FORMATTER)

RESTRICTING_INFO_FORMATTER = {
    'balance': to_integer_if_hex,
    'Pledge': to_integer_if_hex,
    'debt': to_integer_if_hex,
    'plans': apply_formatter_if(is_not_null, apply_list_to_array_formatter(restricting_plan_formatter))
}

restricting_info_formatter = apply_formatters_to_dict(RESTRICTING_INFO_FORMATTER)

CANDIDATE_INFO_FORMATTER = {
    'Shares': to_integer_if_hex,
    'Released': to_integer_if_hex,
    'ReleasedHes': to_integer_if_hex,
    'RestrictingPlan': to_integer_if_hex,
    'RestrictingPlanHes': to_integer_if_hex,
    'DelegateTotal': to_integer_if_hex,
    'DelegateTotalHes': to_integer_if_hex,
    'DelegateRewardTotal': to_integer_if_hex,
}

candidate_info_formatter = apply_formatters_to_dict(CANDIDATE_INFO_FORMATTER)

VERIFIER_INFO_FORMATTER = {
    'Shares': to_integer_if_hex,
    'DelegateTotal': to_integer_if_hex,
    'DelegateRewardTotal': to_integer_if_hex,
}

verifier_info_formatter = apply_formatters_to_dict(VERIFIER_INFO_FORMATTER)

VALIDATOR_INFO_FORMATTER = {
    'Shares': to_integer_if_hex,
    'DelegateTotal': to_integer_if_hex,
    'DelegateRewardTotal': to_integer_if_hex,
}

validator_info_formatter = apply_formatters_to_dict(VALIDATOR_INFO_FORMATTER)

DELEGATE_INFO_FORMATTER = {
    'Released': to_integer_if_hex,
    'ReleasedHes': to_integer_if_hex,
    'RestrictingPlan': to_integer_if_hex,
    'RestrictingPlanHes': to_integer_if_hex,
    'CumulativeIncome': to_integer_if_hex,
    'LockReleasedHes': to_integer_if_hex,
    'LockRestrictingPlanHes': to_integer_if_hex,
}

delegate_info_formatter = apply_formatters_to_dict(DELEGATE_INFO_FORMATTER)

LOCKED_DELEGATE_INFO_FORMATTER = {
    "Released": to_integer_if_hex,
    "RestrictingPlan": to_integer_if_hex,
}

locked_delegate_info_formatter = apply_formatters_to_dict(LOCKED_DELEGATE_INFO_FORMATTER)

DELEGATE_LOCK_INFO_FORMATTER = {
    "Locks": apply_list_to_array_formatter(locked_delegate_info_formatter),
    "Released": to_integer_if_hex,
    "RestrictingPlan": to_integer_if_hex,
}

delegate_lock_info_formatter = apply_formatters_to_dict(DELEGATE_LOCK_INFO_FORMATTER)

DELEGATE_REWARD_FORMATTER = {
    'reward': to_integer_if_hex,
}

delegate_reward_formatter = apply_formatters_to_dict(DELEGATE_REWARD_FORMATTER)

CANDID_DATE_INFO_FORMATTER = {
    'NodeId': to_hex_if_bytes,
    'BlsPubKey': to_hex_if_bytes,
    'StakingAddress': to_hex_if_bytes,
    'BenefitAddress': to_hex_if_bytes,
}

candi_date_info_formatter = apply_formatters_to_dict(CANDID_DATE_INFO_FORMATTER)


# get_bubble_info_formatter =

GET_L1_HASH_FORMATTER = {
    'L1TxHash': to_hex_if_bytes,
}
get_l1_hash_formatter = apply_formatters_to_dict(GET_L1_HASH_FORMATTER)


GET_BUB_TXHASH_LIST_FAOMATTER = {
    'TxHash': to_hex_if_bytes,
}
get_bub_txhash_list_formatter = apply_formatters_to_dict(GET_BUB_TXHASH_LIST_FAOMATTER)


GET_L2_HASH_FORMATTER = {
    'L2TxHash': to_hex_if_bytes,
}
get_l2_hash_formatter = apply_formatters_to_dict(GET_L2_HASH_FORMATTER)

INNER_CONTRACT_RESULT_FORMATTERS = {
    InnerFunction.restricting_getRestrictingInfo: restricting_info_formatter,
    InnerFunction.staking_getCandidateList: apply_list_to_array_formatter(candidate_info_formatter),
    InnerFunction.staking_getVerifierList: apply_list_to_array_formatter(verifier_info_formatter),
    InnerFunction.staking_getValidatorList: apply_list_to_array_formatter(validator_info_formatter),
    InnerFunction.staking_getCandidateInfo: candidate_info_formatter,
    InnerFunction.staking_getBlockReward: to_integer_if_hex,
    InnerFunction.staking_getStakingReward: to_integer_if_hex,
    InnerFunction.delegate_getDelegateInfo: delegate_info_formatter,
    InnerFunction.reward_getDelegateReward: apply_list_to_array_formatter(delegate_reward_formatter),
    InnerFunction.delegate_getDelegateLockInfo: delegate_lock_info_formatter,
    # InnerFunction.stakingL2_getCandidateInfo: candi_date_info_formatter,
    # InnerFunction.bubble_getBubbleInfo: get_bubble_info_formatter,
    # InnerFunction.bubble_getL1HashByL2Hash: get_l1_hash_formatter,
    InnerFunction.bubble_getBubTxHashList: get_bub_txhash_list_formatter,
    # InnerFunction.bubbleL2_getL2HashByL1Hash: get_l2_hash_formatter,
}

WITHDREW_DELEGATE_EVENT_FORMATTER = {
    'delegateIncome': apply_formatter_if(is_not_null, to_integer_if_bytes),
    'released': to_integer_if_bytes,
    'restrictingPlan': to_integer_if_bytes,
    'lockReleased': to_integer_if_bytes,
    'lockRestrictingPlan': to_integer_if_bytes,
}

withdrew_delegate_event_formatter = apply_formatters_to_dict(WITHDREW_DELEGATE_EVENT_FORMATTER)

REDEEM_DELEGATE_EVENT_FORMATTER = {
    'released': to_integer_if_bytes,
    'restrictingPlan': to_integer_if_bytes,
}

redeem_delegate_event_formatter = apply_formatters_to_dict(REDEEM_DELEGATE_EVENT_FORMATTER)

WITHDRAW_DELEGATE_REWARD_EVENT_FORMATTER = {
    'NodeID': to_hex_if_bytes,
    'StakingNum': to_integer_if_bytes,
    'Reward': to_integer_if_bytes,
}

withdraw_delegate_reward_event_formatter = apply_formatters_to_dict(WITHDRAW_DELEGATE_REWARD_EVENT_FORMATTER)

ACC_TOKEN_ASSET_FORMATTER = {
    'TokenAddr': to_hex_if_bytes
}

acc_toKen_assets_formatter = apply_formatters_to_dict(ACC_TOKEN_ASSET_FORMATTER)

DEPOSIT_TOKEN_INFO_FORMATTER = {
    'Account': to_hex_if_bytes,
    'TokenAssets': apply_formatter_if(is_not_null, apply_list_to_array_formatter(acc_toKen_assets_formatter))
}

deposit_token_info_formatter = apply_formatters_to_dict(DEPOSIT_TOKEN_INFO_FORMATTER)


TOKEN_ASSET_FORMATTER = {
    'TokenAddr': to_hex_if_bytes
}

toKen_assets_formatter = apply_formatters_to_dict(TOKEN_ASSET_FORMATTER)

WITHDREW_TOKEN_INFO_FORMATTER = {
    'Account': to_hex_if_bytes,
    'TokenAssets': apply_formatter_if(is_not_null, apply_list_to_array_formatter(toKen_assets_formatter))
}

withdrew_token_info_formatter = apply_formatters_to_dict(WITHDREW_TOKEN_INFO_FORMATTER)

TOKENS_FORMATTER = {
    'token_address': to_hex_if_bytes,
}
tokens_formatter = apply_formatters_to_dict(TOKENS_FORMATTER)

SETTLE_MENT_INFO_FORMATTER = {
    'account': to_hex_if_bytes,
    'tokens': apply_formatter_if(is_not_null, apply_list_to_array_formatter(tokens_formatter))
}
settle_ment_info_formatter = apply_formatters_to_dict(SETTLE_MENT_INFO_FORMATTER)

SETTLE_BUBBLE_FORMATTER = {
    'L2SettleTxHash': to_hex_if_bytes,
    'settlementInfo': apply_formatter_if(is_not_null, apply_list_to_array_formatter(settle_ment_info_formatter))
}
settle_bubble_formatter = apply_formatters_to_dict(SETTLE_BUBBLE_FORMATTER)


TOKENS_L2_FORMATTER = {
    'token_address': to_hex_if_bytes,
}
tokens_formatter = apply_formatters_to_dict(TOKENS_L2_FORMATTER)

SETTLE_MENT_L2_INFO_FORMATTER = {
    'account': to_hex_if_bytes,
    'tokens': apply_formatter_if(is_not_null, apply_list_to_array_formatter(tokens_formatter))
}
settle_ment_L2_info_formatter = apply_formatters_to_dict(SETTLE_MENT_L2_INFO_FORMATTER)

SETTLE_BUBBLE_L2_FORMATTER = {
    'L2SettleTxHash': to_hex_if_bytes,
    'settlementInfo': apply_formatter_if(is_not_null, apply_list_to_array_formatter(settle_ment_info_formatter))
}
settle_bubble_L2_formatter = apply_formatters_to_dict(SETTLE_BUBBLE_L2_FORMATTER)


MINT_TOKENS_L2_FORMATTER = {
    'token_address': to_hex_if_bytes,
}
mint_tokens_formatter = apply_formatters_to_dict(MINT_TOKENS_L2_FORMATTER)

MINT_ACCOUNT_INFO_FORMATTER = {
    'account': to_hex_if_bytes,
    'tokens': apply_formatter_if(is_not_null, apply_list_to_array_formatter(mint_tokens_formatter))
}
mint_account_info_formatter = apply_formatters_to_dict(SETTLE_MENT_L2_INFO_FORMATTER)

MINT_TOKEN_FORMATTER = {
    'TxHash': to_hex_if_bytes,
    'AccountAsset': apply_formatter_if(is_not_null, apply_list_to_array_formatter(mint_account_info_formatter)),
}
mint_token_formatter = apply_formatters_to_dict(MINT_TOKEN_FORMATTER)

CREATA_BUBBLE_EVENT_FORMATTER = {
    'BubbleID': to_integer_if_bytes,
}
create_bubble_event_formatter = apply_formatters_to_dict(CREATA_BUBBLE_EVENT_FORMATTER)

INNER_CONTRACT_EVENT_FORMATTERS = {
    InnerFunction.delegate_withdrewDelegate: withdrew_delegate_event_formatter,
    InnerFunction.delegate_redeemDelegate: redeem_delegate_event_formatter,
    InnerFunction.reward_withdrawDelegateReward: apply_list_to_array_formatter(withdraw_delegate_reward_event_formatter),
    # InnerFunction.bubble_createBubble: create_bubble_event_formatter,
    InnerFunction.bubble_depositToken: deposit_token_info_formatter,
    InnerFunction.bubble_withdrewToken: withdrew_token_info_formatter,
    InnerFunction.bubble_settleBubble: settle_bubble_formatter,
    InnerFunction.bubbleL2_settleBubble: settle_bubble_L2_formatter,
    InnerFunction.bubbleL2_mintToken: mint_token_formatter,
}
