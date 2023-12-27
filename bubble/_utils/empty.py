from bubble._utils.compat import (
    Literal,
)


class Empty:
    def __bool__(self) -> Literal[False]:
        return False


empty = Empty()