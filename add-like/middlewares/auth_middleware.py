import os, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

bearer_scheme = HTTPBearer()

def get_current_responsible(
    cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> str:
    """
    Validates the Bearer token, decodes the JWT, and returns the responsibleId (extracted from userId).
    Throws 401/403 errors if the token is missing, invalid, or expired..
    """
    token = cred.credentials 
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    responsible_id = payload.get("userId") 
    if not responsible_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No userId in token"
        )
    return responsible_id
