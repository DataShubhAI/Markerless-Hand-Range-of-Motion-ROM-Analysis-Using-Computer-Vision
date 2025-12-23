# Markerless Hand Range of Motion (ROM) Analysis Using Computer Vision

## Overview

This project presents a markerless computer vision–based system for automated estimation of hand joint Range of Motion (ROM) using a monocular RGB camera. The system extracts clinically relevant kinematic metrics without physical markers or wearable sensors, enabling non-invasive, low-cost hand motion assessment.

The pipeline integrates computer vision, biomechanical modeling, and time-series data analysis to estimate flexion angles of the Metacarpophalangeal (MCP), Proximal Interphalangeal (PIP), and Distal Interphalangeal (DIP) joints of the index finger. The project is designed for applications in tele-rehabilitation, biomechanics research, and healthcare analytics.

---

## Objectives

* Perform real-time, markerless hand joint tracking from video input
* Compute joint flexion angles using vector-based geometric methods
* Log and analyze time-series kinematic data
* Reduce measurement noise using signal smoothing techniques
* Compare 2D projected and 3D depth-aware angle estimation approaches

---

## Technical Approach

### Hand Landmark Detection

* Uses Google MediaPipe Hand Landmark model
* Detects 21 anatomical keypoints per hand
* Provides normalized 2D coordinates with relative depth (z)

### Joint Angle Computation

* Angles computed using dot product formulation between limb vectors
* Supports both 2D and 3D coordinate inputs
* Maps geometric angles to clinically meaningful flexion values

### Time-Series Data Analysis

* Continuous logging of joint angles with timestamps
* Session data exported as CSV for downstream analysis
* Enables longitudinal and trend-based motion analysis

### Signal Smoothing

* Adaptive moving average filter applied to angle trajectories
* Reduces inference jitter while preserving physiological motion patterns

### 2D vs 3D Analysis Trade-Offs

* 2D Mode: Faster, simpler, but sensitive to camera perspective
* 3D Mode: Uses inferred depth for improved robustness to hand rotation
* Codebase structured to support both approaches

---

## Project Structure

```text
HAND_ROM_ASSMNT/
│
├── main.py                 # Real-time ROM estimation and data logging
├── hand_detector.py        # MediaPipe hand detection interface
├── geometry_utils.py       # Vector-based joint angle calculations
├── plot_results.py         # Time-series smoothing and visualization
├── download_model.py       # Automatic model download and setup
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── data/
│   ├── rom_logs/
│   │   └── session_data.csv
│   └── output_videos/
│       └── rom_graph.png
│
└── models/
    └── hand_landmarker.task
```

---

## Installation

Install required dependencies using:

```bash
pip install -r requirements.txt
```

---

## Usage

Run live hand ROM assessment using a webcam:

```bash
python main.py
```

Run the system for a fixed duration (in seconds):

```bash
python main.py --duration 30
```

Generate plots and ROM metrics from recorded session data:

```bash
python plot_results.py
```

---

## Outputs

* CSV file containing time-stamped joint angle data
* Smoothed and raw ROM trajectory plots
* Peak-to-peak ROM measurements for each joint

---

## Example Metrics

* Index MCP joint ROM (degrees)
* Index PIP joint ROM (degrees)
* Index DIP joint ROM (degrees)
* Session duration and temporal trends

---
## Future Enhancements

* Enforce full 3D angle computation across the pipeline
* Camera calibration for metric reconstruction
* Multi-finger and multi-hand support
* Advanced filtering techniques (Kalman, Savitzky–Golay)
* Integration with rehabilitation and analytics dashboards

---
## Author

Shubham Yadav
B.S. in Computer Science and Data Analysis
Indian Institute of Technology Patna

Interests: Data Analytics, Computer Vision, Machine Learning, Biomechanics
GitHub: [https://github.com/DataShubhAI](https://github.com/DataShubhAI)

---
