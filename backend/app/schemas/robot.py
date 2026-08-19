"""Robot schemas."""
from typing import Optional
from pydantic import BaseModel


class RobotSchema(BaseModel):
    id: int
    name: str
    status: str
    current_node_id: int
    current_heading: Optional[str] = None
    current_task_id: Optional[int] = None

class RobotUpdate(BaseModel):
    current_node_id: Optional[int] = None
    current_heading: Optional[str] = None
