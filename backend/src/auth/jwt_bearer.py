from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request : Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code = 401, detail="Invalid or Expired Token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code = 401, detail="Invalid or Expired Token!")

    def verify_jwt(self, jwt_token : str):
        isTokenValid : bool = False
        payload = decodeJWT(jwt_token)
        if payload:
            isTokenValid = True
        return isTokenValid
    
    async def get_current_user_id(self, request: Request) -> str:
        token = await self(request)

        payload = decodeJWT(token)
        
        if not payload:
            return None
        
        return payload.get("id")
