from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from auth import verify_password, create_access_token,verify_token
from logging.handlers import RotatingFileHandler
from models import User
from schemas import Token
import logging

log_file_path = 'pass'

def setup_logging(log_file_path):
    logger =logging.getLogger('ACE\ REFUND')
    logger.setLevel(logging.DEBUG)
    file_handler =RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s -%(name)s -%(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logging(log_file_path)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        logger.info("User Login request.")
        user = User(form_data.username)
        if not user or not verify_password(form_data.password, user.hased_password, logger):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Invalid username or password",
                headers ={"WWW-Authenticate": "Bearer"}
            )
        access_token = create_access_token(
            data = {"sub":user.username}, expires_delta= timedelta(minutes =30)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        logger.error(f"Error during logging user.{e}",exc_info= True)
        return False

@app.get("/users/me")
def read_users_me(token: str =Depends(oauth2_scheme)):
    try:
        logger.info("User verification initiated")
        username = verify_token(token, logger)
        if username is None:
            logger.info("User verified succesfully.")
            raise HTTPException(
                status_code =status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate":"Bearer"}
            )
        return {"username":username}
    except Exception as e:
        logger.error(f"Unable to verify the user.{e}",exc_info= True)
        return False
