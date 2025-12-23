import os
import cv2
import time
import numpy as np
import pandas as pd
from hand_detector import HandDetector
from geometry_utils import calculate_angle

import argparse

def main():
    parser = argparse.ArgumentParser(description='Hand ROM demo')
    parser.add_argument('--duration', '-d', type=float, default=None, help='Run time in seconds (auto-exit).')
    parser.add_argument('--video', '-v', default=0, help='Video source (0 for webcam or path to file)')
    parser.add_argument('--no-save', dest='save', action='store_false', help='Do not save CSV')
    args = parser.parse_args()

    # --- CONFIGURATION ---
    VIDEO_SOURCE = args.video
    SAVE_DATA = args.save
    OUTPUT_CSV = "data/rom_logs/session_data.csv"
    RUN_DURATION = args.duration

    cap = cv2.VideoCapture(int(VIDEO_SOURCE) if str(VIDEO_SOURCE).isdigit() else VIDEO_SOURCE)
    detector = HandDetector(max_hands=1)

    # Store data for plotting
    data_log = []
    start_time = time.time()

    print("System Active. Press 'q' to quit.")

    while True:
        if RUN_DURATION is not None and (time.time() - start_time) > RUN_DURATION:
            print('Duration elapsed; exiting')
            break

        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        lm_list = detector.find_positions(img)

        if len(lm_list) != 0:
            # Convert landmark list to a lookup by id: {id: (x, y)}
            positions = {entry[0]: (entry[1], entry[2]) for entry in lm_list}

            # Landmarks used for index finger: Wrist(0), MCP(5), PIP(6), DIP(7), Tip(8)
            required = [0, 5, 6, 7, 8]
            if all(k in positions for k in required):
                # 1. MCP Angle (Formed by Wrist, MCP, PIP)
                mcp_angle = calculate_angle(positions[0], positions[5], positions[6])

                # 2. PIP Angle (Formed by MCP, PIP, DIP)
                pip_angle = calculate_angle(positions[5], positions[6], positions[7])

                # 3. DIP Angle (Formed by PIP, DIP, Tip)
                dip_angle = calculate_angle(positions[6], positions[7], positions[8])

                # --- VISUALIZATION ---
                # Display angles on the screen near the joints
                cv2.putText(img, f'MCP: {int(mcp_angle)}', (positions[5][0]-30, positions[5][1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(img, f'PIP: {int(pip_angle)}', (positions[6][0]-30, positions[6][1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Log Data
                if SAVE_DATA:
                    timestamp = round(time.time() - start_time, 2)
                    data_log.append([timestamp, mcp_angle, pip_angle, dip_angle])
        else:
            # If detector is running in mock mode, synthesize demo data so we can demo plotting
            try:
                if detector.mode == 'mock':
                    t = time.time() - start_time
                    # simple synthetic angles (varying sine waves)
                    mcp_angle = 40 + 25 * np.sin(2 * np.pi * 0.2 * t)
                    pip_angle = 30 + 20 * np.sin(2 * np.pi * 0.25 * t + 0.5)
                    dip_angle = 20 + 10 * np.sin(2 * np.pi * 0.3 * t + 1.0)

                    cv2.putText(img, f'MCP: {int(mcp_angle)}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                    cv2.putText(img, f'PIP: {int(pip_angle)}', (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

                    if SAVE_DATA:
                        timestamp = round(time.time() - start_time, 2)
                        data_log.append([timestamp, mcp_angle, pip_angle, dip_angle])
            except Exception:
                pass

        # Show FPS
        cv2.imshow("IIT Patna - Hand ROM Estimation", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
    # Save Data to CSV
    if SAVE_DATA and len(data_log) > 0:
        # Ensure output directory exists
        out_dir = os.path.dirname(OUTPUT_CSV)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        df = pd.DataFrame(data_log, columns=['timestamp', 'mcp_angle', 'pip_angle', 'dip_angle'])
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Data saved to {OUTPUT_CSV}")
    else:
        print('No data recorded.')

if __name__ == "__main__":
    main()