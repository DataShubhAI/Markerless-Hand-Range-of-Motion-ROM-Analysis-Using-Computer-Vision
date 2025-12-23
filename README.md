# Markerless Hand Range of Motion (ROM) Analysis Using Computer Vision

## Overview

This project presents a markerless computer vision–based system for automated estimation of hand joint Range of Motion (ROM) using a monocular RGB camera. The system extracts clinically relevant kinematic metrics without physical markers or wearable sensors, enabling non-invasive, low-cost hand motion assessment.

The pipeline integrates computer vision, biomechanical modeling, and time-series data analysis to estimate flexion angles of the Metacarpophalangeal (MCP), Proximal Interphalangeal (PIP), and Distal Interphalangeal (DIP) joints of the index finger. The project is designed for applications in tele-rehabilitation, biomechanics research, and healthcare analytics.

---
## Analysis of Dynamic Finger Joint Angles During a Monitored Session

1.0 Introduction and Overview

This document provides a detailed narrative interpretation of graphical data representing the dynamic flexion angles of the Metacarpophalangeal (MCP) and Proximal Interphalangeal (PIP) joints over a nine-second period. The strategic analysis of such data is fundamental to understanding the complex, coordinated patterns of finger movement. The analysis begins with both joints in a state of partial flexion, from which they initiate their distinct cyclical patterns. This analysis will first deconstruct the individual movement characteristics of each joint before conducting a comparative assessment of their dynamics. We begin with a detailed examination of the MCP joint.

2.0 Analysis of Metacarpophalangeal (MCP) Joint Dynamics

The Metacarpophalangeal (MCP) joint, commonly known as the knuckle joint, facilitates the primary flexion and extension of the finger relative to the palm. Tracking its motion is crucial for assessing large-scale finger articulation. This section breaks down the specific kinematic patterns observed for the MCP joint during the monitored session.

The key dynamic characteristics of the MCP joint, represented by the blue line in the source data, are as follows:

* Observed Range of Motion (ROM): A measured range of motion of 50.0°.
* Peak and Trough Flexion: An approximate peak flexion of ~65° and trough flexion of ~15°.
* Cyclical Pattern: A smooth, periodic motion completing approximately 1.5 cycles, with an approximate cycle period of 4.5 seconds (peak-to-peak).
* Contextual Performance: The peak flexion of ~65° remains significantly below the indicated "Normal MCP Flexion Limit" of 90°, suggesting the task did not require the joint's maximum flexion capacity.

We now proceed to the analysis of the second joint involved in this coordinated movement, the PIP joint.

3.0 Analysis of Proximal Interphalangeal (PIP) Joint Dynamics

The Proximal Interphalangeal (PIP) joint is the second joint of the finger, responsible for curling the middle phalanx. Its movement profile provides critical insight into the finer aspects of finger articulation and grip formation. This section will analyze its specific kinematics as depicted in the data.

Based on the orange line data from the provided graph, the key dynamic characteristics of the PIP joint are synthesized below:

* Observed Range of Motion (ROM): A measured range of motion of 40.0°.
* Peak and Trough Flexion: An approximate peak flexion of ~50° and trough flexion of ~10°.
* Cyclical Pattern: A smooth, periodic motion completing two full cycles, with an approximate cycle period of 4.0 seconds (peak-to-peak).

The following section will now compare and contrast the dynamic behaviors of both the MCP and PIP joints to understand their interplay.

4.0 Comparative Analysis of MCP and PIP Joint Kinematics

Understanding the relationship, timing, and magnitude differences between the MCP and PIP joints is critical for interpreting the overall coordination of the finger's motion. While individual joint analysis provides valuable data, a comparative view reveals the nature of the neuromuscular control strategy employed. The table below provides a direct quantitative comparison of the key metrics for both joints.

Metric	MCP Joint	PIP Joint
Observed Range of Motion (ROM)	50.0°	40.0°
Approximate Peak Flexion	~65°	~50°
Approximate Trough Flexion	~15°	~10°
Approximate Period	~4.5 seconds	~4.0 seconds

Beyond these quantitative differences, a qualitative analysis of the two waveforms reveals a crucial relationship. Although beginning from a nearly identical posture, the movements of the two joints are clearly asynchronous, or out of phase. In each cycle, the PIP joint consistently reaches its peak and trough flexion before the MCP joint. This phase shift creates a wave-like closing and opening of the finger. This sequential recruitment of joints is biomechanically efficient for tasks like grasping, allowing the distal parts of the finger to first position themselves around an object before the larger, more powerful proximal joint provides clamping force.

5.0 Summary of Key Observations

The primary takeaways from the kinematic analysis are as follows:

1. Distinct Ranges of Motion: The MCP joint demonstrated a greater range of motion (50.0°) compared to the PIP joint (40.0°), indicating it undergoes a larger angular displacement during the activity.
2. Asynchronous Coordination: The relationship between the joints is periodic but asynchronous, with a clear phase lag where the MCP joint's movements follow the PIP joint's movements, producing a sequential, wave-like articulation.
3. Sub-maximal Flexion: The MCP joint's peak flexion remained well within its normal physiological limits, indicating the observed task was a controlled, cyclical motion rather than a forceful, maximum-exertion grip.

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
