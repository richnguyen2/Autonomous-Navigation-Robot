import { ReactFlow, applyNodeChanges, applyEdgeChanges, addEdge, Background } from '@xyflow/react';
import { useState, useEffect } from 'react';
import PathNode from '../components/PathNode';
import LocationNode from '../components/LocationNode';
import CreateTaskModal from '../components/CreateTaskModal';
import TaskList from '../components/TaskList';
import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import RobotSim from '../components/RobotSim';
import RobotNode from '../components/RobotNode';
import OccupantNode from '../components/OccupantNode';

const nodeTypes = {
    robot: RobotNode,
    grid_cell: PathNode,
    location: LocationNode,
    occupant: OccupantNode,
};

const mult = 15;

const MapPage = () => {
    const queryClient = useQueryClient();
    const [expandedNodeId, setExpandedNodeId] = useState(null);
    const [activeCreateTaskModalId, setActiveCreateTaskModalId] = useState(null);

    const {
        data: tasks = [],
        isLoading: isTasksLoading
    } = useQuery({
        queryKey: ['tasks', 'active'],
        queryFn: api.getActiveTasks,
    });

    const standbyMutation = useMutation({
        mutationFn: (taskId) => api.standbyTask(taskId),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tasks', 'active'] });
            queryClient.invalidateQueries({ queryKey: ['robot', 'path'] });
        },

        onError: (error) => {
            console.error("Standby failed:", error.message);
            alert(`Could not update task status: ${error.message}`);
        }
    });

    const {
        data: nodes = [],
        isLoading: isNodesLoading
    } = useQuery({
        queryKey: ['nodes', 'location'],
        queryFn: api.getLocations,

        select: (rawNodes) => rawNodes.map(node => {
            const isExpanded = expandedNodeId === node.id.toString();
            return {
                id: node.id.toString(),
                type: node.node_type,
                position: { x: node.x_coord * mult, y: node.y_coord * mult },
                zIndex: isExpanded ? 1000 : 600,
                data: {
                    label: node.label ?? "",
                    expandedNodeId,
                    setExpandedNodeId,
                    openTaskModal: (nodeId) => setActiveCreateTaskModalId(nodeId)
                },
                draggable: false
            }
        })
    });

    const {
        data: occupants = [],
        isLoading: isOccupantsLoading
    } = useQuery({
        queryKey: ['nodes', 'occupants'],
        queryFn: api.getOccupants,

        select: (rawNodes) => rawNodes.map(node => {
            return {
                id: node.id.toString(),
                type: 'occupant',
                position: { x: node.x_coord * mult, y: node.y_coord * mult },
                zIndex: 600,
                data: {},
                draggable: false
            }
        })
    });

    const {
        data: pathData = { nodes: [], edges: [] },
    } = useQuery({
        queryKey: ['robot', 'path'],
        queryFn: api.getRobotPath,
        select: (newPath) => {
            const pathNodes = newPath.nodes.map(node => ({
                id: node.id.toString(),
                type: 'grid_cell',
                position: { x: node.x_coord * mult, y: node.y_coord * mult },
                data: {},
                draggable: false,
                zIndex: 500
            }));

            const pathEdges = newPath.edges.map(edge => ({
                id: `edge-${edge.id}`,
                source: edge.source.toString(),
                target: edge.target.toString(),
                style: { stroke: 'black', strokeWidth: 2 },
                animated: true,
                zIndex: 400
            }));

            return { nodes: pathNodes, edges: pathEdges };
        }
    });

    const { data: robotNodeData } = useQuery({
        queryKey: ['robot', 'node'],
        queryFn: api.getRobotNode,
    });

    // Only for Simulated Robot! Will remove later
    const updateRobotPositionMutation = useMutation({
        mutationFn: (newPosition) => api.updateRobot(newPosition),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['robot', 'node'] });
        },

        onError: (error) => {
            console.error("Failed to update robot position:", error.message);
            alert(`Could not update robot position: ${error.message}`);
        }
    });

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/ws/robot");

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'POSITION_UPDATED') {
                queryClient.setQueryData(['robot', 'node'], message.payload);
            }
        };

        return () => ws.close();
    }, [queryClient]);

    const completeTaskMutation = useMutation({
        mutationFn: (taskId) => api.completeTask(taskId),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tasks', 'active'] });
            queryClient.invalidateQueries({ queryKey: ['robot', 'path'] });
            queryClient.invalidateQueries({ queryKey: ['robot', 'node'] });
        },

        onError: (error) => {
            console.error("Failed to complete task:", error.message);
            alert(`Could not complete task: ${error.message}`);
        }
    });

    const robotNode = robotNodeData ? {
        id: 'robot',
        type: 'robot',
        position: { x: robotNodeData.x_coord * mult, y: robotNodeData.y_coord * mult },
        data: {},
        draggable: false,
        zIndex: 700
    } : null;

    const combinedNodes = [...pathData.nodes, ...nodes, ...occupants, robotNode].filter(Boolean);

    return (
        <div className="w-full h-screen overflow-hidden">
            <div className="absolute inset-0 z-0">
                {(isNodesLoading || isOccupantsLoading) ? (
                    <p>Loading map...</p>
                ) : (
                    <>
                        <ReactFlow
                            nodes={combinedNodes}
                            // edges={pathData.edges}
                            nodeTypes={nodeTypes}
                            nodesConnectable={false}
                            onPaneClick={() => {
                                setExpandedNodeId(null);
                            }}
                            fitView
                        >
                            <Background />
                        </ReactFlow>
                        {activeCreateTaskModalId && (
                            <div className="fixed inset-0 backdrop-blur-xs z-[9999] flex items-center justify-center">
                                <CreateTaskModal
                                    activeCreateTaskModalId={activeCreateTaskModalId}
                                    setActiveCreateTaskModalId={setActiveCreateTaskModalId}
                                />
                            </div>
                        )}
                    </>
                )}
            </div>
            <div className="absolute top-4 right-4 z-10 p-4 border border-2 rounded-xl bg-white">
                {isTasksLoading ? (
                    <p>Loading tasks...</p>
                ) : (
                    <TaskList
                        tasks={tasks}
                        onCancel={standbyMutation.mutate}
                    />
                )}
            </div>
            <div className="absolute bottom-4 right-4 z-10 rounded-xl bg-white">
                <RobotSim
                    pathData={pathData}
                    currentTask={tasks.find(t => t.status === 'in_progress')}
                    refetchTasks={() => {
                        queryClient.invalidateQueries({ queryKey: ['tasks', 'active'] });
                        queryClient.invalidateQueries({ queryKey: ['robot', 'path'] })
                    }}
                    updatePosition={updateRobotPositionMutation.mutateAsync}
                />
            </div>
        </div>
    );
}

export default MapPage
