########################################
#                                      #
#       DATABASE CONFIGURATIONS        #
#                                      #
########################################

# CLIENT_URL = 'mongodb://localhost:27017/'
DB = 'myDB'
CLIENT_URL = "mongodb+srv://chandan:DONB3AU6Kh4jBWck@cluster0.wu3zr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# localhost = 10.5.48.246


JWT_SECRET_KEY = "z9wCq_dQmG45vT6X1N5pzJWy7gfp87iLJfkS7sUqkcT3w=="
HASHING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 
REFRESH_TOKEN_EXPIRE_MINUTES = 60 

########################################
#                                      #
#    DOCUMENTS SAVING DIRECTORIES      #
#                                      #
########################################

MFO_UPLOAD_FOLDER = 'MFO_Images'
DRIVER_UPLOAD_FOLDER = 'DRIVER_Images'






########################################
#                                      #
#           API CREDENTIALS            #
#                                      #
########################################

APPYFLOW_GST_API = 'JwQUHPGmb1ZUIzX4TXTmIrjMkKl1'

F2_API_KEY = "c73b4fd2-ede2-11ef-8b17-0200cd936042"


########################################
#                                      #
#         DATABASE STRUCTURES          #
#                                      #
########################################

MFO_DB_STRUCTURE = {
    "Name" :"",
    "Phone": "",
    "Email" :"",
    "Business_name" :"",
    "GST_number": "",
    "Operating_address" : "",
    "Vehicle_IDs" : [],
    "Driver_IDs":[],
    "Invited_drivers": [],
    "Business_image" :"",
    "Owner_image": "",
    "Created_At":"",
    "Last_updated_At": "",
    "timestamp":True,
    "Docs_id": ""
}


MFO_DOCS_DB_STRUCTURE = {
    "Aadhar_card" : "",
    "PAN_card" : "",
    "GST_doc": "",
    "MSME" : "",
}



DRIVER_DB_STRUCTURE = {
    "Name" : "",
    "Phone" : "",
    "Vehicle_IDs" : [],
    "Assigned_vehicle_IDs" : [],
    "Status" : "",
    "MFO_IDs" : [],
    "Driver_image" : "",
    "Created_At" : "",
    "Docs_id": ""
}


DRIVER_DOCS_DB_STRUCTURE = {
    "License" : "",
    "Aadhar_card" : "",
    "PAN_card" : "",
}



VEHICLE_DB_STRUCTURE = {
    "Number":"",
    "Number_plate":"",
    "RC" : "",
    "Insurance": "",
    "ICE" : "",
    "Assigned_driver_IDs" : [],
    "Current_assigned_driver" : "",
    "Added_At":"",
    "Owner_ID":""
}