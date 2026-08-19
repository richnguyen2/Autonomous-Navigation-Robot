# Autonomous Mobile Robot

## Overview

Developed an autonomous mobile robot integrating perception, localization, path planning, and low-level motion control. The system combines stereo vision for object detection and depth estimation, a discrete Bayes filter for robot localization, and closed-loop motor control for executing motion commands.

**System Architecture:**  
Perception → Localization → Path Planning → Motion Control → Robot

## Repository Structure

```text
mobile-robot-maid/
├── frontend/    # Web interface
├── backend/     # API server
└── robot/       # Robot software

frontend/
Web interface for monitoring robot status and sending commands.

backend/
API server responsible for communication between the frontend and robot.

robot/
Software running on the Raspberry Pi and Arduino that handles perception,
localization, planning, and motor control.
```

## Key Components - Robot/

## Demo


### Perception — Object Detection & Depth Estimation
- Detected landmarks using SIFT feature matching and homography-based image transformation
- Rectified stereo camera views to align corresponding points horizontally
- Estimated object depth using stereo disparity

### Discrete Bayes Localization
- Estimated the robot's position using a discrete Bayes filter
- Updated the belief distribution through prediction and measurement steps
- Used sensor observations to improve localization accuracy

### Low-Level Motion Control
- Implemented closed-loop control for differential-drive motion
- Used IMU feedback to reduce heading error during straight-line motion and turning
- Controlled motor commands for forward motion and turning

## Team

Kevin Nguyen, Richard Nguyen
