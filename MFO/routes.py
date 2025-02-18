from fastapi import APIRouter , Form , UploadFile , File
import os
import db
import asyncio
import config
import utils
import datetime
from bson import ObjectId

mfo_router = APIRouter()


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





##################################
#                                #
#             ROUTES             #
#                                #
##################################


@mfo_router.post("/signup")
async def signup(
    Name: str = Form(...),
    Phone: int = Form(...),
    Email: str = Form(...),
    Business_name: str = Form(...),
    GST_number: str = Form(...),
    Aadhar_card: UploadFile = File(...),
    PAN_card: UploadFile = File(...),
):
    data = {}
    data_docs = {}

    data['Name'] = Name
    data['Phone'] = Phone
    data['Email'] = Email
    data['Business_name'] = Business_name
    data['GST_number'] = GST_number
    data["Created_At"] = datetime.datetime.now()

    
    aadhar_filename = f"{Phone}_{Aadhar_card.filename}"
    pan_filename = f"{Phone}_{PAN_card.filename}"
    
    with open(f"uploads/{aadhar_filename}", "wb") as f:
        f.write(await Aadhar_card.read())
    
    with open(f"uploads/{pan_filename}", "wb") as f:
        f.write(await PAN_card.read())
    
    data_docs['Aadhar_card'] = aadhar_filename
    data_docs['PAN_card'] = pan_filename
    docs_id = await db.insertData(data_docs , config.DB , 'MFO_docs' , config.MFO_DOCS_DB_STRUCTURE)
    data['Docs_id'] = docs_id
    data_id = await db.insertData(data , config.DB , 'MFO_main' , config.MFO_DB_STRUCTURE)
    return {"message": f"Signup successful for {Name} "}



def objectid_to_str(user_data):
    if isinstance(user_data, dict):
        for key, value in user_data.items():
            if isinstance(value, ObjectId):
                user_data[key] = str(value)  # Convert ObjectId to string
            elif isinstance(value, dict):
                user_data[key] = objectid_to_str(value)  # Recursively handle nested dicts
    return user_data

@mfo_router.post("/get_main_data")
async def get_main_data(Phone_number):
    user = await db.get_data("Phone" , int(Phone_number) , config.DB , "MFO_main")
    data = {}
    if(user == False):
        return {
        "massage": "User do not exists"
        }
    user = objectid_to_str(user)
    data['main'] = user
    docs = await db.get_data('_id' , ObjectId(user['Docs_id']), config.DB , "MFO_docs")
    data['docs'] = objectid_to_str(docs)
    return data
    
    
