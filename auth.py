import os
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from secrets import SECRET


class Auth:

    _hasher = CryptContext(schemes=['bcrypt'])
    _secret = SECRET
    _algorithm = "HS256"

    def encode_password(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify_password(self, password: str, encoded_password: str) -> bool:
        return self._hasher.verify(password, encoded_password)

    def encode_token(self, username: str) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": username,
        }
        return jwt.encode(payload=payload, key=self._secret, algorithm=self._algorithm)

    def decode_token(self, jwt_token: str) -> str:
        try:
            payload = jwt.decode(jwt=jwt_token, key=self._secret, algorithms=[self._algorithm])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(status_code=401, detail="Scope for the token is invalid")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")