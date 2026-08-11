from jose import jwt
from datetime import datetime
from datetime import timedelta
from jose import JWTError

SECRET_KEY = "animeproject_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_HOURS = 12


def create_access_token(data: dict):

    payload = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )

    payload.update(
        {"exp": expire}
    )

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        return username

    except JWTError:

        return None