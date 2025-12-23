import subprocess
import time
import socket
import os

# --- Configuration ---
MEDIAMTX_PATH = "/Users/adibasubah/Downloads/mediamtx/mediamtx"
VIDEO_FILE = "/Users/adibasubah/rtmp/demo.mp4"
RTSP_URL = "rtsp://127.0.0.1:8554/test"


def wait_for_port(host: str, port: int, timeout: int = 10):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (ConnectionRefusedError, OSError):
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.5)


def main():
    # 1. Cleanup old config files that cause crashes
    config_file = os.path.join(os.path.dirname(MEDIAMTX_PATH), "mediamtx.yml")
    if os.path.exists(config_file):
        os.remove(config_file)
        print(f"🧹 Removed old config: {config_file}")

    # 2. Prepare Environment Variables
    # MTX_PATHS_ALL_ALLOWPUBLISHING=yes tells MediaMTX to allow any stream
    env = os.environ.copy()
    env["MTX_PATHS_ALL_ALLOWPUBLISHING"] = "yes"
    env["MTX_LOGLEVEL"] = "info"

    mtx_proc = None
    ffmpeg_proc = None

    try:
        print("🚀 Starting MediaMTX via Env Vars...")
        mtx_proc = subprocess.Popen(
            [MEDIAMTX_PATH],
            env=env,
            cwd=os.path.dirname(MEDIAMTX_PATH),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        # Give it a second to fail or start
        time.sleep(1)
        if mtx_proc.poll() is not None:
            print("❌ MediaMTX failed to start. Logs:")
            print(mtx_proc.stdout.read())
            return

        if not wait_for_port("127.0.0.1", 8554):
            print("❌ MediaMTX started but port 8554 is not responding.")
            return

        print("✅ MediaMTX is ready.")

        # 3. Start FFmpeg
        ffmpeg_cmd = [
            "ffmpeg",
            "-re",
            "-stream_loop",
            "-1",
            "-i",
            VIDEO_FILE,
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-tune",
            "zerolatency",
            "-pix_fmt",
            "yuv420p",
            "-an",  # Keep audio off to isolate video success
            "-f",
            "rtsp",
            "-rtsp_transport",
            "tcp",
            RTSP_URL,
        ]

        print(f"📡 Pushing to: {RTSP_URL}")
        ffmpeg_proc = subprocess.Popen(ffmpeg_cmd)

        print("Streaming active. Press Ctrl+C to stop.")
        while ffmpeg_proc.poll() is None:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if ffmpeg_proc:
            ffmpeg_proc.terminate()
        if mtx_proc:
            mtx_proc.terminate()
        print("Done.")


if __name__ == "__main__":
    main()
