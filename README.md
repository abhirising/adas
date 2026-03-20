# ADAS 1V Solution AEB/ACC Demo

## Overview
This project demonstrates:
- YOLOv8 object detection
- Distance estimation using bounding boxes
- Time-to-Collision (TTC)
- AEB and ACC decision logic

## Run
pip install ultralytics opencv-python
python your_script.py

## Results
<img width="612" height="221" alt="image" src="https://github.com/user-attachments/assets/d83537dd-ff7c-4f24-ad55-6caca3c4b39c" />

## Env Setup
### System Setup
- Ubuntu 20.04.6 LTS
### Conda Installation
- Download Miniconda -->         wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
- Install -->                  bash Miniconda3-latest-Linux-x86_64.sh
- Restart terminal or run -->   source ~/.bashrc
- Verify -->                 conda --version

### Yolo & Dependencies Installation
  - pip install ultralytics
  - pip install opencv-python numpy

### Flowchart
```mermaid
flowchart LR
    A[Input Image / Camera] --> B[Perception]
    B --> C[Situation Interpretation]
    C --> D{Decision}
subgraph D1[Decision & Planning Phase]
    D -->|TTC < 1.5s| E[AEB Brake]
    D -->|TTC < 3s| F[ACC Slow Down]
    D -->|Else| G[Safe]
end



