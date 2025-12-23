# Markerless Hand Range of Motion (ROM) Analysis Using Computer Vision

## Overview

This project presents a markerless computer vision–based system for automated estimation of hand joint Range of Motion (ROM) using a monocular RGB camera. The system extracts clinically relevant kinematic metrics without physical markers or wearable sensors, enabling non-invasive, low-cost hand motion assessment.

The pipeline integrates computer vision, biomechanical modeling, and time-series data analysis to estimate flexion angles of the Metacarpophalangeal (MCP), Proximal Interphalangeal (PIP), and Distal Interphalangeal (DIP) joints of the index finger. The project is designed for applications in tele-rehabilitation, biomechanics research, and healthcare analytics.

---

## Analysis of Dynamic Finger Joint Angles During a Monitored Session

### 1.0 Introduction and Overview

This section presents a detailed analytical interpretation of time-series kinematic data representing the dynamic flexion angles of the Metacarpophalangeal (MCP) and Proximal Interphalangeal (PIP) joints during a monitored session of approximately nine seconds. Analyzing such joint-level angular trajectories is essential for understanding coordinated finger motion, neuromuscular control strategies, and functional hand biomechanics.

Both joints begin the session in a partially flexed posture and subsequently exhibit periodic motion patterns. The analysis is structured to first examine the individual kinematic behavior of each joint, followed by a comparative assessment to understand their coordinated dynamics.

![resultt](https://github.com/user-attachments/assets/034ff256-5712-46bd-82cf-1b1bb0278a3e)
<img width="3573" height="2837" alt="Mind Map" src="https://github.com/user-attachments/assets/71d8245f-8b04-4352-897d-3b43408deaa9" />
<img width="1376" height="768" alt="image" src="https://github.com/user-attachments/assets/19847613-ace0-4533-ba50-dd7a357a9c81" />

---

### 2.0 Analysis of Metacarpophalangeal (MCP) Joint Dynamics

The Metacarpophalangeal (MCP) joint, commonly referred to as the knuckle joint, plays a primary role in flexion and extension of the finger relative to the palm. Its motion largely governs the gross articulation of the finger and is therefore a critical indicator of functional hand movement.

The following characteristics were observed for the MCP joint during the monitored session:

* **Observed Range of Motion (ROM):** 50.0°
* **Peak Flexion:** Approximately 65°
* **Trough Flexion:** Approximately 15°
* **Cyclical Behavior:** Smooth and periodic, completing approximately 1.5 cycles
* **Cycle Period:** Approximately 4.5 seconds (peak-to-peak)
* **Contextual Interpretation:** The observed peak flexion of ~65° remains well below the commonly accepted normal MCP flexion limit of 90°, indicating that the task involved controlled, sub-maximal motion rather than forceful or end-range exertion.

These characteristics suggest stable, repeatable joint control consistent with deliberate finger movement rather than abrupt or compensatory motion.

---

### 3.0 Analysis of Proximal Interphalangeal (PIP) Joint Dynamics

The Proximal Interphalangeal (PIP) joint, located between the proximal and middle phalanges, is primarily responsible for finger curling and fine-grained articulation. Its motion profile provides insight into precision control and grasp formation.

Analysis of the PIP joint revealed the following kinematic properties:

* **Observed Range of Motion (ROM):** 40.0°
* **Peak Flexion:** Approximately 50°
* **Trough Flexion:** Approximately 10°
* **Cyclical Behavior:** Smooth and periodic, completing approximately two full cycles
* **Cycle Period:** Approximately 4.0 seconds (peak-to-peak)

Compared to the MCP joint, the PIP joint exhibits a slightly higher movement frequency and a reduced angular range, consistent with its anatomical role in fine motor control.

---

### 4.0 Comparative Analysis of MCP and PIP Joint Kinematics

A comparative evaluation of MCP and PIP joint behavior provides deeper insight into inter-joint coordination and movement sequencing. While individual joint metrics are informative, their temporal relationship reveals the underlying biomechanical strategy.

#### Quantitative Comparison

| Metric                         | MCP Joint    | PIP Joint    |
| ------------------------------ | ------------ | ------------ |
| Observed Range of Motion (ROM) | 50.0°        | 40.0°        |
| Approximate Peak Flexion       | ~65°         | ~50°         |
| Approximate Trough Flexion     | ~15°         | ~10°         |
| Approximate Period             | ~4.5 seconds | ~4.0 seconds |

#### Qualitative Interpretation

Although both joints begin from a similar initial posture, their movements are clearly asynchronous. The PIP joint consistently reaches both peak and trough flexion before the MCP joint, indicating a measurable phase shift between their motion profiles.

This phase-lagged coordination produces a wave-like opening and closing pattern of the finger. Such sequential recruitment is biomechanically efficient for functional tasks such as grasping, where distal joint positioning precedes proximal force generation. The observed behavior aligns with established principles of human prehension and motor control.

---

### 5.0 Summary of Key Observations

The primary findings from this kinematic analysis are summarized below:

1. **Distinct Ranges of Motion:** The MCP joint demonstrated a larger angular displacement (50.0°) than the PIP joint (40.0°), reflecting its dominant role in gross finger articulation.
2. **Asynchronous Joint Coordination:** The MCP and PIP joints exhibited periodic but out-of-phase motion, with the MCP joint lagging behind the PIP joint, resulting in a sequential, wave-like articulation pattern.
3. **Sub-Maximal Flexion Behavior:** Peak MCP flexion remained well within normal physiological limits, indicating that the recorded task involved controlled, repetitive motion rather than maximal or force-driven exertion.

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

Indian Institute of Technology Patna

Interests: Data Analytics, Computer Vision, Machine Learning, Biomechanics

GitHub: [https://github.com/DataShubhAI](https://github.com/DataShubhAI)

LinkedIn:https://www.linkedin.com/in/shubham-yadav-98a0a4286/

---
