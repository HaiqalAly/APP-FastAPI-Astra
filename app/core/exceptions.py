from typing import Optional

class AuthenticationError(Exception):
    """Base exception for all auth issues."""

    default_message = "Authentication failed"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


# Token related exceptions
class TokenError(AuthenticationError):
    default_message = "An error occurred with the token"


class TokenExpiredError(TokenError):
    default_message = "Token has expired"


class InvalidTokenError(TokenError):
    default_message = "Invalid token"


# User related exceptions
class InvalidCredentialsError(AuthenticationError):
    default_message = "Invalid username or password"


class InactiveUserError(AuthenticationError):
    default_message = "User account is inactive"


class InsufficientPermissionsError(AuthenticationError):
    default_message = "Not enough permissions"


class UserAlreadyExistsError(AuthenticationError):
    def __init__(self, field: str, message: str | None = None):
        self.field = field
        msg = message or f"{field.capitalize()} already exists"
        super().__init__(msg)


class InvalidPasswordConfirmationError(AuthenticationError):
    default_message = "Invalid password confirmation"


class InvalidConfirmationTextError(AuthenticationError):
    default_message = "Confirmation text must be 'DELETE MY ACCOUNT'"