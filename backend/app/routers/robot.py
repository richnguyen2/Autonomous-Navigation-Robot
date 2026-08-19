"""Robot endpoints."""
from typing import Optional
from app.models import Robot, Task, Edge, Node
from app.utils.astar import run_astar_grid
from app.utils.get_commands_from_path import get_commands_from_path
from app.schemas.path import PathResponseSchema
from app.schemas.response import ResponseSchema
from app.schemas.robot import RobotUpdate
from app.schemas.node import NodeSchema
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.database import SessionDep
from app.services.websocket_manager import manager
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/robot", tags=["robot"])

@router.get("/node", response_model=ResponseSchema[NodeSchema])
async def get_robot_node(session: SessionDep) -> dict:
    """Return the node that the robot is on"""
    robot = session.exec(select(Robot).where(Robot.name == "Bot-01")).first()
    if not robot:
        raise HTTPException(status_code=404, detail="Virtual simulation robot asset not found.")
    node = robot.current_node
    if not node:
        raise HTTPException(status_code=404, detail="Robot position node not found in grid.")
    return {"data": node}

@router.patch("/next-task", response_model=Optional[dict])
async def get_next_task(session: SessionDep) -> Optional[dict]:
    """Sets the first pending task to in progress"""
    statement = select(Task).where(Task.status == "pending").order_by(Task.dispatched_at)
    task = session.exec(statement).first()
    if not task:
        return None

    task.status = "in_progress"
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "task_id": task.id,
        "name": task.name,
        "x_coord": task.node.x_coord,
        "y_coord": task.node.y_coord,
    }

@router.patch("/update", response_model=ResponseSchema[RobotUpdate])
async def update_robot(robot_update: RobotUpdate, session: SessionDep) -> Optional[dict]:
    """Updates the robots location"""
    robot = session.exec(select(Robot).where(Robot.name == "Bot-01")).first()
    if not robot:
        raise HTTPException(status_code=404, detail="Robot asset not found.")

    update_data = robot_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(robot, key, value)

    session.add(robot)
    session.commit()
    session.refresh(robot)

    node = robot.current_node

    await manager.broadcast({
        "type": "ROBOT_MOVED", 
        "payload": jsonable_encoder(node)
    })
    return {"data": robot}

@router.get("/path", response_model=PathResponseSchema)
async def get_robot_active_path(session: SessionDep):
    """Uses A* to find an optimal path from the robot's position to target Node"""
    robot = session.exec(select(Robot).where(Robot.name == "Bot-01")).first()
    if not robot:
        raise HTTPException(status_code=404, detail="Virtual simulation robot asset not found.")

    active_task = session.exec(
        select(Task).where(Task.status == "in_progress")
    ).first()

    if not active_task or not robot.current_node_id:
        return {"data": {"nodes": [], "edges": []}}

    node_id_sequence = run_astar_grid(session, robot.current_node_id, active_task.node_id)
    if not node_id_sequence:
        return {"data": {"nodes": [], "edges": []}}

    nodes_lookup = {n.id: n for n in session.exec(select(Node).where(Node.id.in_(node_id_sequence))).all()}
    ordered_path_nodes = [nodes_lookup[node_id] for node_id in node_id_sequence if node_id in nodes_lookup]

    commands = get_commands_from_path(session, ordered_path_nodes)
    # print("Generated Commands:", commands)
    ordered_path_edges = []
    for i in range(len(node_id_sequence) - 1):
        u = node_id_sequence[i]
        v = node_id_sequence[i + 1]
        
        matching_edge = session.exec(
            select(Edge).where(Edge.source == u, Edge.target == v)
        ).first()
        
        if matching_edge:
            ordered_path_edges.append(matching_edge)

    return {
        "data": {
            "nodes": ordered_path_nodes,
            "edges": ordered_path_edges,
            "commands": commands
        }
    }