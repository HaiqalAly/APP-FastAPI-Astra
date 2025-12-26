from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from app.core.config import CONFIG
from app.core.exceptions import InvalidTokenError, TokenExpiredError

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def _create_token(data: dict, expires_delta: timedelta | None, token_type: str, default_minutes: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=default_minutes))
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, CONFIG.SECRET_KEY, algorithm=CONFIG.ALGORITHM)

def _verify_token(token: str, expected_type: str) -> dict:
    try:
        payload = jwt.decode(token, CONFIG.SECRET_KEY, algorithms=[CONFIG.ALGORITHM])
        if "sub" not in payload:
            raise InvalidTokenError("Token missing 'sub' claim")
        if payload.get("type") != expected_type:
            raise InvalidTokenError(f"Invalid token type: expected {expected_type}")
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.PyJWTError:
        raise InvalidTokenError()

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    return _create_token(data, expires_delta, "access", CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)

def verify_access_token(token: str) -> dict:
    return _verify_token(token, "access")

def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    return _create_token(data, expires_delta, "refresh", CONFIG.REFRESH_TOKEN_EXPIRE_MINUTES)

def verify_refresh_token(token: str) -> dict:
    return _verify_token(token, "refresh")