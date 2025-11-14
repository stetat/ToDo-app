from typing import Annotated, Union
from pydantic import Field, BaseModel, HttpUrl
from enum import Enum

class Status(str, Enum):
    done = "done"
    active = "active"
    incomplete = "incomplete"
    archived = "archived"

class TaskIn(BaseModel):
    status: Status
    image: Annotated[Union[HttpUrl, None], Field()] = None
    name: Annotated[str, Field(default="test",
                               title="task's name",
                               min_length=1,
                               max_length=200,
                               )]
    description: Annotated[str, Field(default="None",
                                      title="task's detailed explanation",
                                      min_length=1,
                                      max_length=5000)]
    
    model_config = {
        "json_schema_extra" : {
            "examples" : [
                {
                    "status": "done",
                    "images": "some image url",
                    "name": "finish 8th lab",
                    "description": "go thorugh 8 to 10th problems"                
                },
                {
                    "status": "archived",
                    "images": "some image url",
                    "name": "finish 10th lab",
                    "description": "go thorugh 8 to 1000th problems"                
                }
            ]
        }
    }

class TaskInDB(TaskIn):
    id: int
    
    