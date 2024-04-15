import time
import jwt

from decouple import config

JWT_SECRET = config("secret")
JSWT_ALGORITHM = config("algorithm")

# Function returns the generated tokens
def token_response(ime: str, prezime: str, token: str, isAdmin : bool):
    return {
        "ime" : ime,
        "prezime" : prezime,
        "isAdmin" : isAdmin,
        "token" : token
    }

# Function used for signing the JWT string
def signJWT(ime: str, prezime: str, userId : str, isAdmin : bool):
    payload = {
        "userId": userId,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JSWT_ALGORITHM)
    return token_response(ime, prezime, token, isAdmin)

# Function used to decode the JWT string
def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JSWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}