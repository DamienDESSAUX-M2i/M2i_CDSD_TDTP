class SignalException(Exception):
    def __init__(self, msg: str):
        self.msg: str = msg
    
    def display_message_error(self):
        print(self.msg)
