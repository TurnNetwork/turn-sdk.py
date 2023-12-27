# [ BEACON endpoints ]

GET_GENESIS = "/bub/v1/beacon/genesis"
GET_HASH_ROOT = "/bub/v1/beacon/states/{0}/root"
GET_FORK_DATA = "/bub/v1/beacon/states/{0}/fork"
GET_FINALITY_CHECKPOINT = "/bub/v1/beacon/states/{0}/finality_checkpoints"
GET_VALIDATORS = "/bub/v1/beacon/states/{0}/validators"
GET_VALIDATOR = "/bub/v1/beacon/states/{0}/validators/{1}"
GET_VALIDATOR_BALANCES = "/bub/v1/beacon/states/{0}/validator_balances"
GET_EPOCH_COMMITTEES = "/bub/v1/beacon/states/{0}/committees"
GET_BLOCK_HEADERS = "/bub/v1/beacon/headers"
GET_BLOCK_HEADER = "/bub/v1/beacon/headers/{0}"
GET_BLOCK = "/bub/v2/beacon/blocks/{0}"
GET_BLOCK_ROOT = "/bub/v1/beacon/blocks/{0}/root"
GET_BLOCK_ATTESTATIONS = "/bub/v1/beacon/blocks/{0}/attestations"
GET_ATTESTATIONS = "/bub/v1/beacon/pool/attestations"
GET_ATTESTER_SLASHINGS = "/bub/v1/beacon/pool/attester_slashings"
GET_PROPOSER_SLASHINGS = "/bub/v1/beacon/pool/proposer_slashings"
GET_VOLUNTARY_EXITS = "/bub/v1/beacon/pool/voluntary_exits"

# [ CONFIG endpoints ]

GET_FORK_SCHEDULE = "/bub/v1/config/fork_schedule"
GET_SPEC = "/bub/v1/config/spec"
GET_DEPOSIT_CONTRACT = "/bub/v1/config/deposit_contract"

# [ DEBUG endpoints ]

GET_BEACON_STATE = "/bub/v1/debug/beacon/states/{0}"
GET_BEACON_HEADS = "/bub/v1/debug/beacon/heads"

# [ NODE endpoints ]

GET_NODE_IDENTITY = "/bub/v1/node/identity"
GET_PEERS = "/bub/v1/node/peers"
GET_PEER = "/bub/v1/node/peers/{0}"
GET_HEALTH = "/bub/v1/node/health"
GET_VERSION = "/bub/v1/node/version"
GET_SYNCING = "/bub/v1/node/syncing"
