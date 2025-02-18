from fastapi import APIRouter, Form, UploadFile, File
import config
import utils
from fastapi import FastAPI, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from jose import JWTError, jwt
import httpx
import db
from fastapi import APIRouter, HTTPException, status, Depends


auth_and_regester = APIRouter()

templates = Jinja2Templates(directory="templates")
refresh_tokens_store = {}



##################################
#                                #
#             ROUTES             #
#                                #
##################################





@auth_and_regester.post("/send_otp")
async def send_otp(phone_number: str , user:str):


    url = f"https://2factor.in/API/V1/{config.F2_API_KEY}/SMS/{phone_number}/AUTOGEN"
    try:
        response = httpx.get(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send OTP via SMS") from e
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP via SMS: {response.text}")
    
    data = response.json()
    if data.get("Status") != "Success":
        raise HTTPException(status_code=500, detail=f"Failed to send OTP via SMS: {data.get('Details')}")
    
    request_id = data.get("Details")
    
    return {"message": "OTP sent successfully" , "Request_ID" : request_id }




@auth_and_regester.post("/verify_otp")
async def verify_otp(
    Phone:str,
    otp: str,
    request_id:str,
    user:str
):
    verify_url = f"https://2factor.in/API/V1/{config.F2_API_KEY}/SMS/VERIFY/{request_id}/{otp}"
    
    try:
        verify_response = httpx.get(verify_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to verify OTP") from e
    
    if verify_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to verify OTP")
    
    verify_data = verify_response.json()
    if verify_data.get("Status") != "Success":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP provided."
        )  

    access_token = utils.create_access_token(data={"sub": str(Phone)})
    refresh_token = utils.create_refresh_token(data={"sub": str(Phone)})

    refresh_tokens_store[str(Phone)] = refresh_token
    exists_ok = False
    if(user == 'MFO'):
        exists = await db.user_exist("Phone_number" , Phone , config.DB , 'MFO_main')
        if(exists):
            exists_ok = True
    else:
        exists = await db.user_exists("Phone_number" , Phone , config.DB , 'DRIVER_main')
        if(exists):
            exists_ok = True

    return {
        "message": "OTP verified successfully",
        "status" : "verified",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "Exists" : exists_ok
    }





@auth_and_regester.post("/refresh_token")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, config.JWT_SECRET_KEY, algorithms=[config.HASHING_ALGORITHM]
        )
        phone_number: str = payload.get("sub")
        if phone_number is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        if refresh_tokens_store.get(phone_number) != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        new_access_token = utils.create_access_token(data={"sub": phone_number})

        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
