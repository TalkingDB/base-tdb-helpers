import os
import secrets

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from talkingdb.clients.sqlite import sqlite_conn, GRAPH_DB
from talkingdb.models.auth.api_key import APIKeyModel

import bcrypt

security = HTTPBearer()


def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    api_key = credentials.credentials

    with sqlite_conn(GRAPH_DB) as conn:
        user_email = APIKeyModel.verify(
            conn=conn,
            api_key=api_key,
        )

    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "UNAUTHORIZED",
                "message": "Invalid API key",
            },
        )
    return user_email


def verify_service_secret(
    x_service_secret: str = Header(default="", alias="X-Service-Secret"),
) -> None:
    expected = os.getenv("TRUSTED_SERVICE_SECRET")

    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error_code": "SERVICE_UNAVAILABLE",
                "message": "Service-to-service authentication is not configured",
            },
        )

    if not x_service_secret or not secrets.compare_digest(x_service_secret, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "UNAUTHORIZED",
                "message": "Invalid service credential",
            },
        )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )