import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_rom(csv_path: str = "data/rom_logs/session_data.csv"):
    # Load data
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print("No data file found. Run main.py first.")
        return

    # Normalize column names (accept both lowercase and expected headers)
    df_cols = {c.lower(): c for c in df.columns}
    # expected: timestamp, mcp_angle, pip_angle, dip_angle
    if 'mcp_angle' not in df_cols or 'pip_angle' not in df_cols:
        print("CSV does not contain required columns (mcp_angle, pip_angle).")
        return

    time_col = df_cols.get('timestamp')
    times = df[time_col] if time_col else df.index
    mcp = df[df_cols['mcp_angle']]
    pip = df[df_cols['pip_angle']]

    # Calculate Range of Motion (ROM)
    mcp_rom = mcp.max() - mcp.min()
    pip_rom = pip.max() - pip.min()
    
    print("Calculated ROM for Session:")
    print(f" Index MCP ROM: {mcp_rom:.2f} degrees")
    print(f" Index PIP ROM: {pip_rom:.2f} degrees")

    # Smoothing (Moving Average) for cleaner graphs
    window = max(1, int(len(mcp) * 0.05))  # 5% of samples or at least 1
    mcp_smooth = mcp.rolling(window=window, min_periods=1, center=False).mean()
    pip_smooth = pip.rolling(window=window, min_periods=1, center=False).mean()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(times, mcp_smooth, label=f"MCP Joint (ROM: {mcp_rom:.1f}°)", color='blue')
    plt.plot(times, pip_smooth, label=f"PIP Joint (ROM: {pip_rom:.1f}°)", color='orange')

    plt.title("Dynamic Finger Joint Angles during Session")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Flexion Angle (degrees)")
    plt.axhline(y=90, color='r', linestyle='--', alpha=0.3, label="Normal MCP Flexion Limit (90°)")
    plt.legend()
    plt.grid(True)

    out_dir = os.path.dirname('data/output_videos/rom_graph.png')
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    out_path = 'data/output_videos/rom_graph.png'
    plt.savefig(out_path)
    print(f"Saved plot to {out_path}")
    plt.show()

if __name__ == "__main__":
    plot_rom()