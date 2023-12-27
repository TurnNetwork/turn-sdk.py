from bubble.module import (
    Module,
)
from bubble.inner_contract import (
    Staking,
    Delegate,
    Slashing,
    Reward,
)


class DPos(Module):
    staking: Staking
    delegate: Delegate
    slashing: Slashing
    reward: Reward
