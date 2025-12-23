# config.py
import os

# --- Path Configurations ---
# Use absolute paths or resolve them relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MediaMTX Settings
MEDIAMTX_PATH = "/Users/adibasubah/Downloads/mediamtx/mediamtx"
MEDIAMTX_DIR = os.path.dirname(MEDIAMTX_PATH)

# Video Settings
VIDEO_FILE = "/Users/adibasubah/rtmp/demo.mp4"

# --- Network Settings ---
RTSP_HOST = "127.0.0.1"
RTSP_PORT = 8554
STREAM_PATH = "test"
RTSP_URL = f"rtsp://{RTSP_HOST}:{RTSP_PORT}/{STREAM_PATH}"

# --- FFmpeg Encoding Settings ---
FFMPEG_SETTINGS = {
    "v_codec": "libx264",
    "preset": "ultrafast",
    "tune": "zerolatency",
    "pix_fmt": "yuv420p",
    "bitrate": "2000k",
    "fps": 25,
    "enable_audio": True,  # Toggle this to True/False easily
}

# --- MediaMTX Environment Variables ---
# These override the mediamtx.yml settings
MTX_ENV = {
    "MTX_PATHS_ALL_ALLOWPUBLISHING": "yes",
    "MTX_LOGLEVEL": "info",
    "MTX_RTSPADDRESS": f":{RTSP_PORT}",
}
