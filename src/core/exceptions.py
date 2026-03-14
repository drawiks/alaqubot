class AlaquBotException(Exception):
    pass


class ConfigurationError(AlaquBotException):
    pass


class APIError(AlaquBotException):
    pass


class AuthenticationError(AlaquBotException):
    pass


class CommandError(AlaquBotException):
    pass
