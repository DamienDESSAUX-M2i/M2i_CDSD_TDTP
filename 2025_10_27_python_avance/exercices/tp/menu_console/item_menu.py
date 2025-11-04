from typing import Callable


class ItemMenu:
    def __init__(
            self,
            signal: str,
            action: Callable,
            msg: str
            ):
        self._signal: str = signal
        self._action: Callable = action
        self._msg: str = msg
    
    @property
    def signal(self) -> str:
        return self._signal
    
    @signal.setter
    def signal(self, signal: str) -> None:
        if type(signal) is not str:
            raise TypeError("'signal' must be a string.")
        self._signal = signal
        
    @property
    def action(self) -> Callable:
        return self._action
    
    @action.setter
    def action(self, action: Callable) -> None:
        if type(action) is not Callable:
            raise TypeError("'action' must be a callable.")
        self._action = action
        
    @property
    def msg(self) -> str:
        return self._msg
    
    @msg.setter
    def msg(self, msg: str) -> None:
        if type(msg) is not str:
            raise TypeError("'msg' must be a string.")
        self._msg = msg