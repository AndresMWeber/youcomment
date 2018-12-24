class EnvironmentError(Exception):
    """ Is raised when an environment variable variable was not found. """
    pass


class ConfigError(Exception):
    """ Is raised when a config variable was not found. """
    pass


class InvalidYoutubeURL(Exception):
    """ Is raised when a url is not a valid youtube link. """
    pass
