"""Utility to download MediaPipe HandLandmarker model bundle.

Downloads the floating-point16 hand_landmarker.task model into `models/hand_landmarker.task`
so the Tasks API can load it.
"""
import os
import sys
import urllib.request

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"


def download_hand_landmarker(dest_path: str = "models/hand_landmarker.task") -> str:
    """Download the hand_landmarker.task model to dest_path.

    Returns the path to the model file on success.
    Raises RuntimeError on failure.
    """
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    if os.path.exists(dest_path):
        return dest_path

    print(f"Downloading hand_landmarker model from {MODEL_URL} -> {dest_path}")
    try:
        with urllib.request.urlopen(MODEL_URL) as resp, open(dest_path, "wb") as out:
            CHUNK = 8192
            while True:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                out.write(chunk)
    except Exception as e:
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except Exception:
                pass
        raise RuntimeError(f"Failed to download model: {e}") from e

    return dest_path


if __name__ == "__main__":
    try:
        path = download_hand_landmarker()
        print(f"Model downloaded to: {path}")
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
