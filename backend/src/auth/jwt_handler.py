import time
import jwt

from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Function used for signing the JWT string
def signJWT(userId : str):
    payload = {
        "id": userId,
        "expiry": time.time() + 600
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token

# Function used to decode the JWT string
def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decode_token and decode_token.get('expiry', 0) >= time.time():
            return decode_token
        else:
            return None  # Token has expired or invalid
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token