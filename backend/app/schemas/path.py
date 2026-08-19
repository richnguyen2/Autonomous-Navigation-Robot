from pydantic import BaseModel
from typing import List
from app.schemas import NodeSchema, EdgeSchema

class PathData(BaseModel):
    nodes: List[NodeSchema]
    edges: List[EdgeSchema]
    commands: List[str]

class PathResponseSchema(BaseModel):
    data: PathData