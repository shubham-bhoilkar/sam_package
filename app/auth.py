from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
import configparser

config = configparser.ConfigParser()
config.read('/home/neuralit/shubham_workarea/Ace Refund/app/config.ini')

secret_key = config['INFO']['secret_key']
algorithm = config['INFO']['algorithm']
access_token_expire_mins = config['INFO']['access_token_expire_mins']

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Functions for password hashing and verification
def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise e

def verify_password(plain_password: str, hashed_password: str, log) -> bool:
    try:
        log.info("Request to verify the password")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        log.error(f"Unable to verify the content.{e}",exc_info = True)

# Function to create a JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, log=None):
    try:
        log.info("Request to create access token")
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=access_token_expire_mins)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt
    
    except Exception as e:
        log.error(f"Unable to create access token.{e}",exc_info= True)
        return False

# Function to verify a JWT
def verify_token(token: str, log):
    try:
        log.info()
        payload = jwt.decode(token, secret_key, algorithm= algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise JWTError
        return username
    except JWTError:
        log.error(f"Error during verifying the token",exc_info = True)
        return None
