import os
import random
import time
from fastapi import FastAPI, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from MFO import mfo_router
import json
import db
from AuthAndRegester import auth_and_regester


app = FastAPI()

app.include_router(mfo_router, prefix="/mfo")
app.include_router(auth_and_regester)

os.makedirs("uploads", exist_ok=True)


@app.get("/")
async def home_page(request: Request):
    data = {"name": "Alinawaz"}
    return data
