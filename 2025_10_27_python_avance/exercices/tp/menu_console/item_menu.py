from typing import Callable


class ItemMenu:
    def __init__(
            self,
            signal: str,
            action: Callable,
            msg: str
            ):
        self.signal: str = signal
        self.action: Callable = action
        self.msg: str = msg