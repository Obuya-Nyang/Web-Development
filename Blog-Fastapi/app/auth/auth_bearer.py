from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT

'''
The JWTBearer class is a subclass of FastAPI's HTTPBearer class that will be used to persist authentication on our routes.
In the __init__ method, we enable automatic error reporting by setting the boolean auto_error to True.
In the __call__ method, we define a variable called credentials of type HTTPAuthorizationCredentials, which is created when the JWTBearer class is invoked. We then proceeded to check if the credentials passed in during the course of invoking the class are valid:
    1. If the credential scheme isn't a bearer scheme, we raised an exception for an invalid token scheme.
    2. If a bearer token was passed, we verified that the JWT is valid.
    3. If no credentials were received, we raised an invalid authorization error.
'''
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error:bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
    
    # verify if a token is valid
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid