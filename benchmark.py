import subprocess
import time
import socket
import os

# Import your new config
import config


def wait_for_port(host, port, timeout=10):
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
    # 1. Cleanup old config
    old_yml = os.path.join(config.MEDIAMTX_DIR, "mediamtx.yml")
    if os.path.exists(old_yml):
        os.remove(old_yml)

    mtx_proc = None
    ffmpeg_proc = None

    try:
        print(f"🚀 Starting MediaMTX at {config.RTSP_HOST}:{config.RTSP_PORT}...")
        mtx_proc = subprocess.Popen(
            [config.MEDIAMTX_PATH],
            env={
                **os.environ,
                **config.MTX_ENV,
            },  # Merge system env with our config env
            cwd=config.MEDIAMTX_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        if not wait_for_port(config.RTSP_HOST, config.RTSP_PORT):
            print("❌ MediaMTX failed to start.")
            return

        print("✅ MediaMTX is ready.")

        # 2. Construct FFmpeg Command from config
        ffmpeg_cmd = [
            "ffmpeg",
            "-re",
            "-stream_loop",
            "-1",
            "-i",
            config.VIDEO_FILE,
            "-c:v",
            config.FFMPEG_SETTINGS["v_codec"],
            "-preset",
            config.FFMPEG_SETTINGS["preset"],
            "-tune",
            config.FFMPEG_SETTINGS["tune"],
            "-pix_fmt",
            config.FFMPEG_SETTINGS["pix_fmt"],
            "-b:v",
            config.FFMPEG_SETTINGS["bitrate"],
            "-r",
            str(config.FFMPEG_SETTINGS["fps"]),
        ]

        if not config.FFMPEG_SETTINGS["enable_audio"]:
            ffmpeg_cmd.append("-an")

        ffmpeg_cmd.extend(["-f", "rtsp", "-rtsp_transport", "tcp", config.RTSP_URL])

        print(f"📡 Pushing to: {config.RTSP_URL}")
        ffmpeg_proc = subprocess.Popen(ffmpeg_cmd)

        while ffmpeg_proc.poll() is None:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if ffmpeg_proc:
            ffmpeg_proc.terminate()
        if mtx_proc:
            mtx_proc.terminate()


if __name__ == "__main__":
    main()
