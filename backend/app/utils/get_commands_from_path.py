from sqlmodel import Session, select
from app.models import Robot, Node
from fastapi import HTTPException
from typing import List

def get_commands_from_path(session: Session, path_nodes: List[Node]) -> List[str]:
    commands = []
    
    statement = select(Robot).where(Robot.name == "Bot-01")
    robot = session.exec(statement).first()
    if not robot:
        raise HTTPException(status_code=404, detail="Robot asset not found.")
    current_heading = robot.current_heading
    if current_heading is None:
        current_heading = "NORTH"
    print(f"Current Robot Heading: {current_heading}")

    for i in range(len(path_nodes) - 1):
        curr_n = path_nodes[i]
        next_n = path_nodes[i+1]
        
        dx = next_n.x_coord - curr_n.x_coord
        dy = next_n.y_coord - curr_n.y_coord
        
        if dx == 0 and dy == -1: desired = "NORTH"
        elif dx == 1 and dy == 0: desired = "EAST"
        elif dx == 0 and dy == 1: desired = "SOUTH"
        elif dx == -1 and dy == 0: desired = "WEST"
        
        # Logic to turn
        if current_heading != desired:
            commands.extend(get_turn_commands(current_heading, desired))
            current_heading = desired
        
        commands.append("forward")
        
    return commands

def get_turn_commands(current: str, desired: str) -> list[str]:
    # Normalize inputs to uppercase
    current = current.upper()
    desired = desired.upper()
    
    headings = ["NORTH", "EAST", "SOUTH", "WEST"]
    
    # Add a safety check to debug exactly what's failing
    if current not in headings:
        raise ValueError(f"Invalid current heading: {current}")
    if desired not in headings:
        raise ValueError(f"Invalid desired heading: {desired}")
        
    diff = headings.index(desired) - headings.index(current)
    if diff == 1 or diff == -3: return ["turn_right"]
    if diff == -1 or diff == 3: return ["turn_left"]
    return ["turn_right", "turn_right"]