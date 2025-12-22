from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from app.core.config import CONFIG, TokenExpiredError, InvalidTokenError, TokenError

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, CONFIG.SECRET_KEY, algorithm=CONFIG.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, CONFIG.SECRET_KEY, algorithms=[CONFIG.ALGORITHM])
        if "sub" not in payload:
            raise InvalidTokenError("Token missing 'sub' claim")
        if payload.get("type") != "access":
            raise InvalidTokenError("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except jwt.PyJWTError:
        raise InvalidTokenError("Invalid token")
    
def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=CONFIG.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, CONFIG.SECRET_KEY, algorithm=CONFIG.ALGORITHM)
    return encoded_jwt

def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, CONFIG.SECRET_KEY, algorithms=[CONFIG.ALGORITHM])
        if "sub" not in payload:
            raise InvalidTokenError("Token missing 'sub' claim")
        if payload.get("type") != "refresh":
            raise InvalidTokenError("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except jwt.PyJWTError:
        raise InvalidTokenError("Invalid token")