from __future__ import annotations


class DiscordException(Exception):
    pass


class LoginFailure(DiscordException):
    def __init__(self, message: dict, status: int) -> None:
        self.message = message
        self.status = status


class ReconnectWebsocket(DiscordException):
    def __init__(self, message: str) -> None:
        self.message = message


class RuntimeError(DiscordException):
    def __init__(self, message: str) -> None:
        self.message = message


class Funnu(DiscordException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
