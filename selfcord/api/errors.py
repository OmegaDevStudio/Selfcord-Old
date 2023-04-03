class DiscordException(Exception):
    pass


class LoginFailure(DiscordException):
    def __init__(self, message: dict, status: int) -> None:
        super().__init__()
        self.message = message
        self.status = status


class ReconnectWebsocket(DiscordException):
    def __init__(self, message: str) -> None: self.message = message


class RuntimeDiscordError(DiscordException):
    def __init__(self, message: str) -> None: self.message = message


class Funny(DiscordException):
    def __init__(self, *args: object) -> None: super().__init__(*args)
