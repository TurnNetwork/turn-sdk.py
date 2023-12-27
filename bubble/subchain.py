from bubble.module import (
    Module,
)
from bubble.inner_contract import (
    StakingL2,
    Bubble,
    BubbleL2,
    TempPrivateKey,
)


class SubChain(Module):
    stakingL2: StakingL2
    bubble: Bubble
    bubbleL2: BubbleL2
    temp_private_key: TempPrivateKey

    
