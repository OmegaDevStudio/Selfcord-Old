

class DiscordException(Exception):
    pass

class LoginFailure(DiscordException):
    def __init__(self, message: str, status: int) -> None:
        self.message = message
        self.status = status
