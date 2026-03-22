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
  <summary>ADAS System Structure</summary>

  <ul>
    <li><b>main.py</b> – Pipeline orchestration</li>

    <li>
      <details>
        <summary>config/</summary>
        <ul>
          <li><b>config_loader.py</b> – OTA config</li>
        </ul>
      </details>
    </li>

    <li>
      <details>
        <summary>services/</summary>
        <ul>
          <li><b>fcw_service.py</b> – Forward Collision Warning</li>
          <li><b>acc_service.py</b> – Adaptive Cruise Control</li>
          <li><b>aeb_service.py</b> – Automatic Emergency Braking</li>
        </ul>
      </details>
    </li>

    <li>
      <details>
        <summary>perception/</summary>
        <ul>
          <li><b>detector.py</b> – YOLO Detection</li>
        </ul>
      </details>
    </li>

    <li>
      <details>
        <summary>utils/</summary>
        <ul>
          <li>(helper modules)</li>
        </ul>
      </details>
    </li>

  </ul>
</details>

### Next Steps
  - To Make run on Renases V3H Plaform
  - monocular approximation to near true-depth estimation
  - Add FCW Feature





