class TokenError(Exception):
    """Sorry, an error occurred with the token."""
    pass

class TokenExpiredError(TokenError):
    """The token has expired."""
    pass

class InvalidTokenError(TokenError):
    """The token is invalid."""
    pass