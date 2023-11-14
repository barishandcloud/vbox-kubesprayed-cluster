import os
import datetime
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

mongo_host = os.environ.get("MONGO_HOST", "192.168.56.101") 
pod_name = os.environ.get("POD_NAME", "unknown_pod")

app = FastAPI()

# MongoDB connection
mongo_client = AsyncIOMotorClient(f"mongodb://{mongo_host}:27017/")  # Replace with your MongoDB server details
db = mongo_client["employees"]  # Replace with your database name
collection = db["employee_data"]  # Replace with your collection name

def generate_employee_id(uid):
    return f"employee-{uid}"

def get_metadata():
    # Get current date and time
    current_datetime = datetime.datetime.now()
    date_today = current_datetime.strftime("%Y-%m-%d")
    time_now = current_datetime.strftime("%H:%M:%S")
    timestamp_now = current_datetime.timestamp()
    
    return {
        "inserted_by": pod_name,
        "timestamp": timestamp_now,
        "metainfo": {"date": date_today, "time": time_now}
    }

@app.put("/update_employee/{uid}")
async def update_employee(uid: str):
    # Check if the UID exists in the database
    existing_employee = await collection.find_one({"UID": uid})

    if existing_employee:
        raise HTTPException(status_code=400, detail="EmployeeID already exists for this UID")

    # If the UID doesn't exist, create a new entry with metadata
    employee_id = generate_employee_id(uid)
    metadata = get_metadata()
    
    new_employee = {
        "UID": uid,
        "EmployeeID": employee_id,
        "inserted_by": metadata["inserted_by"],
        "timestamp": metadata["timestamp"],
        "metainfo": metadata["metainfo"]
    }
    
    await collection.insert_one(new_employee)
    return {"message": "New employee created"}

@app.get("/get_employee/{uid}")
async def get_employee(uid: str):
    # Check if the UID exists in the database
    existing_employee = await collection.find_one({"UID": uid})

    if existing_employee:
        existing_employee["_id"] = str(existing_employee["_id"])
        return existing_employee

    # If the UID doesn't exist, raise an HTTP 404 (Not Found) exception
    raise HTTPException(status_code=404, detail="Employee with this UID not found")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
