# ADAS 1V Solution AEB/ACC Demo

## Overview
This project demonstrates:
- YOLOv8 object detection : Currently the model can detect 80 types of objects, with detection time = 4.9 ms
- Distance estimation using bounding boxes
- Time-to-Collision (TTC)
- AEB and ACC decision logic

## Run
pip install ultralytics opencv-python
python AEBACC.py

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
    A[Input Image] --> B[Perception]
    B --> C[Situation Interpretation]
    C --> D{Decision}
subgraph D1[Decision & Planning Phase]
    D -->|TTC < 1.5s| E[AEB Brake]
    D -->|TTC < 3s| F[ACC Slow Down]
    D -->|Else| G[Safe]
end
```
## Results
<img width="612" height="221" alt="image" src="https://github.com/user-attachments/assets/d83537dd-ff7c-4f24-ad55-6caca3c4b39c" />

<img width="620" height="242" alt="image" src="https://github.com/user-attachments/assets/f8244523-c39c-4064-84ea-ce673e6d5c3c" />

## SDV Ready
<details>
  <summary><b>ADAS System Structure</b></summary>

  <ul>
    <li><b>main.py</b> – Pipeline orchestration</li>

    <li>
      <b>config/</b>
      <ul>
        <li>config_loader.py – OTA config</li>
      </ul>
    </li>

    <li>
      <b>services/</b>
      <ul>
        <li>fcw_service.py – FCW logic</li>
        <li>acc_service.py – ACC logic</li>
        <li>aeb_service.py – AEB logic</li>
      </ul>
    </li>

    <li>
      <b>perception/</b>
      <ul>
        <li>detector.py – YOLO detection</li>
      </ul>
    </li>

    <li>
      <b>utils/</b>
      <ul>
        <li>helper modules</li>
      </ul>
    </li>

  </ul>
</details>

### Next Steps
  - To Make run on Renases V3H Plaform
  - monocular approximation to near true-depth estimation
  - Add FCW Feature





