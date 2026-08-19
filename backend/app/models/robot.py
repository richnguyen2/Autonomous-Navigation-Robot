from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Robot(SQLModel, table=True):
    """Tracks Robot's State."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="Bot-01")
    status: str = Field(default="idle") # idle, routing, working
    
    current_node_id: int = Field(foreign_key="node.id", nullable=False)
    current_heading: Optional[str] = Field(default=None) # NORTH, SOUTH, EAST, WEST
    
    current_task_id: Optional[int] = Field(default=None, foreign_key="task.id")

    current_node: Optional["Node"] = Relationship()
    current_task: Optional["Task"] = Relationship()