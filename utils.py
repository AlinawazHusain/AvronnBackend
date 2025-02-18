import aiohttp
import config
import config
import datetime
from jose import jwt
from datetime import datetime, timedelta


async def getGSTAddress(gst_number):

    api_url = "https://appyflow.in/api/verifyGST"
    params = {
        "key_secret": config.APPYFLOW_GST_API,
        "gstNo": gst_number,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                address = data["taxpayerInfo"]["pradr"]["addr"]
                final_address = ""
                for i in address:
                    final_address += address[i] + " " if address[i] != "" else ""
                return final_address
            else:
                return "Error to fetch address from API"


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET_KEY, algorithm=config.HASHING_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES),
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET_KEY, algorithm=config.HASHING_ALGORITHM
    )
    return encoded_jwt
