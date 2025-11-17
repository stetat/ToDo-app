from fastapi import FastAPI, Body, Query, status, responses, HTTPException, Response, Path
import json
from pydantic import HttpUrl
from typing import Annotated, Any, Union
from models import TaskIn, TaskInDB
from db import data
from google import genai




app = FastAPI()
client = genai.Client()
next_id = {"id": 1}

# I immitate databse through data list from db file
# next_id serves as a correct id counter


@app.get("/gemini/", status_code=status.HTTP_202_ACCEPTED)
async def gemini_help(taskID: Annotated[int, Query(ge=1, le=100)]):
    taskDesc = data[taskID-1].description
    input = "Give a concise advise on how to solve this problem. Do not solve it, if its illegal in any way, discriminates religion, race or offends someone. Give me pure advice, no filter-related words" + taskDesc
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=input
    )
    return response.text

@app.get("/tasks/", response_model=Union[list[TaskInDB]], status_code=status.HTTP_200_OK)
async def get_tasks() -> Any:
    return data

@app.get("/tasks/{item_id}", response_model=TaskInDB, status_code=status.HTTP_200_OK)
async def get_task_by_id(item_id: Annotated[int, Path()]) -> Any:
    if(item_id < 1 or item_id >= len(data)):
        raise HTTPException(status_code=404, detail="Invalid ID")

    for i, item in enumerate(data):
        if item.id==item_id:
            return data[i]
        

@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
async def create_task(item: Annotated[TaskIn, Body(title="get_task_data",
                                                 description="receiving a json with item's data")]) -> Response:
    item_tmp = item.model_dump()

    
    itemInDB = TaskInDB(**item_tmp, id=next_id["id"])
    next_id["id"] += 1
    data.append(itemInDB)
    return responses.JSONResponse("Task has been added")

@app.put("/tasks/", status_code=status.HTTP_202_ACCEPTED)
async def add_image(id: int, image: HttpUrl) -> Response:
    if(id < 1 or id >= len(data)):
        raise HTTPException(status_code=404, detail="Invalid ID")
    
    for i, item in enumerate(data):
        if item.id==id:
            item.image=image
    return responses.JSONResponse("Image has been added")


@app.delete("/tasks/delete/", status_code=status.HTTP_200_OK)
async def delete_task(item_id: Annotated[int, Query()]) -> Response:
    if(item_id < 1 or item_id >= len(data)):
        raise HTTPException(status_code=404, detail="Invalid ID")
    
 
    reIterate = 0
    for i, item in enumerate(data):
        if item.id == item_id:
            data.pop(i)
            next_id["id"] = item.id
            reIterate = i
            break

    for i, item in enumerate(data):
        if i >= reIterate:
            item.id = next_id["id"]
            next_id["id"] += 1

    
    return responses.JSONResponse("Task has been deleted")
    
    


