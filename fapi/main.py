import os
import datetime
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

mongo_host = os.environ.get("MONGO_HOST", "192.168.56.101") 
pod_name = os.environ.get("POD_NAME", "unknown_pod")

app = FastAPI()

mongo_client = AsyncIOMotorClient({mongo_host}) 
db = mongo_client["employees"]  # database name
collection = db["employee_data"]  # collection name

def generate_employee_id(uid):
    return f"employee-{uid}"

def get_metadata():
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
    existing_employee = await collection.find_one({"UID": uid})

    if existing_employee:
        raise HTTPException(status_code=400, detail="EmployeeID already exists for this UID")

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
    existing_employee = await collection.find_one({"UID": uid})

    if existing_employee:
        existing_employee["_id"] = str(existing_employee["_id"])
        return existing_employee

    raise HTTPException(status_code=404, detail="Employee with this UID not found")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
