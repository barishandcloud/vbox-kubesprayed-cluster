import uvicorn
from fastapi import FastAPI
from typing import Optional
from fastapi import Path, Query

app = FastAPI()
@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/employee/{name}")
async def get_employee(name:str, age:Optional[int]=None):
    return {"name":name, "age":age}

# @app.get("/employee/{name}/branch/{branch_id}")
# async def get_employee(branch_id:int, name:str=Path(None, min_length=10), brname:str=Query(None, min_length=5, max_length=10), age:Optional[int]=None):
#     employee={'name':name, 'Branch':brname, 'Branch ID':branch_id, 'age':age}
#     return employee

# @app.get("/employee/{name}/branch/{branch_id}")
# async def get_employee(branch_id: int, name: str = Path(..., min_length=10), brname: str = Query(None, min_length=5, max_length=10), age: Optional[int] = None):
#     employee = {'name': name, 'Branch': brname, 'Branch ID': branch_id, 'age': age}
#     return employee

# @app.get("/employee/{name}/branch/{branch_id}")
# async def get_employee(branch_id: int, brname:str, name: str = Path(..., regex="^[J]|[h]$"), age: Optional[int] = None):
#     employee = {'name': name, 'Branch': brname, 'Branch ID': branch_id, 'age': age}
#     return employee

# @app.get("/employee/{name}/branch/{branch_id}")
# async def get_employee(name:str, brname:str, branch_id:int=Path(..., gt=0, le=100), age:int=Query(None, ge=20, lt=61)):
#     employee={'name':name, 'Branch':brname, 'Branch ID':branch_id, 'age':age}
#     return employee

@app.get("/employee/{EmpName}/branch/{branch_id}")
async def get_employee(branch_id:int, brname:str, name:str=Path(...,title='Name of Employee',description='Length notmore than 10 chars',alias='EmpName',max_length=10), age:int=Query(None,include_in_schema=False)):
    employee={'name':name, 'Branch':brname, 'Branch ID':branch_id, 'age':age}
    return employee

@app.get("/items/")
async def read_items(skip: int = Query(0, ge=0), limit: int = Query(10, le=100)):
    return {"skip": skip, "limit": limit}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)    