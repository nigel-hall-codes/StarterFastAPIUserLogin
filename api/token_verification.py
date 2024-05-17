import os
import pdb

import jwt
from fastapi import HTTPException
import pdb
def verify_token(auth_token):
    try:

        # pdb.set_trace()
        # Define your secret key used to sign and verify JWTs
        SECRET_KEY = os.getenv("USER_API_SECRET")


        # Verify and decode the token
        decoded_token = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])

        # You can perform additional checks here, such as verifying user roles or permissions
        # Example: if decoded_token["role"] != "admin":
        #             return False

        return decoded_token

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token verification error: {str(e)}")
