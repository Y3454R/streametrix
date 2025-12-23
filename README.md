# Streametrix

I have planned to create a frame extraction from stream (RTSP/RTMP) benchmarking tool. I think, it's a chance to use Python as `glue-script` as it was intended to become.<br>
But for the first phase I built a utility to stream video files over RTSP using MediaMTX and FFmpeg. This tool automatically handles MediaMTX server startup and streams video content via RTSP protocol.

## Features

- 🚀 Automated MediaMTX server startup
- 📡 RTSP stream broadcasting
- 🎬 Configurable FFmpeg encoding settings
- ⚙️ Easy configuration management
- 🔄 Looping video playback
- 📊 TCP transport support

## Prerequisites

Before running the script, ensure you have:

1. **Python 3.7+**
2. **FFmpeg** - For video encoding and streaming
3. **MediaMTX** - RTSP server
4. **A video file** - MP4 format recommended

### Installation

#### 1. Install FFmpeg

**macOS (Homebrew):**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

#### 2. Download MediaMTX

Visit [MediaMTX Releases](https://github.com/bluenviron/mediamtx/releases) and download the binary for your OS.

For macOS:

```bash
# Extract and place in your desired location
tar -xzf mediamtx_*_darwin_amd64.tar.gz
# Move to your preferred directory, e.g., ~/Downloads/mediamtx/
```

#### 3. Prepare Your Video File

Place your video file (e.g., `demo.mp4`) in a known location.

## Configuration

Edit the `config.py` file to customize your setup:

```python
# MediaMTX Settings
MEDIAMTX_PATH = "/path/to/mediamtx"  # Path to MediaMTX binary
MEDIAMTX_DIR = "/path/to/mediamtx/dir"  # MediaMTX directory

# Video Settings
VIDEO_FILE = "/path/to/your/video.mp4"  # Your video file

# Network Settings
RTSP_HOST = "127.0.0.1"  # RTSP server host
RTSP_PORT = 8554         # RTSP server port
STREAM_PATH = "test"     # Stream path/name

# FFmpeg Encoding Settings
FFMPEG_SETTINGS = {
    "v_codec": "libx264",        # Video codec (h264, h265, etc.)
    "preset": "ultrafast",       # Encoding speed (ultrafast to slow)
    "tune": "zerolatency",       # Encoding tuning
    "pix_fmt": "yuv420p",        # Pixel format
    "bitrate": "2000k",          # Video bitrate
    "fps": 25,                   # Frames per second
    "enable_audio": True,        # Audio enabled/disabled
}

# MediaMTX Environment Variables
MTX_ENV = {
    "MTX_PATHS_ALL_ALLOWPUBLISHING": "yes",
    "MTX_LOGLEVEL": "info",
    "MTX_RTSPADDRESS": ":8554",
}
```

### Configuration Examples

**Low Latency Streaming:**

```python
FFMPEG_SETTINGS = {
    "v_codec": "libx264",
    "preset": "ultrafast",
    "tune": "zerolatency",
    "bitrate": "1000k",
    "fps": 30,
}
```

**High Quality Streaming:**

```python
FFMPEG_SETTINGS = {
    "v_codec": "libx264",
    "preset": "slow",
    "tune": "film",
    "bitrate": "5000k",
    "fps": 60,
}
```

**Audio Disabled:**

```python
FFMPEG_SETTINGS = {
    ...
    "enable_audio": False,
}
```

## Usage

### Basic Usage

Run the streaming script:

```bash
python run_mediamtx.py
```

The script will:

1. Start MediaMTX server
2. Connect FFmpeg
3. Begin streaming your video on loop
4. Print status messages

### Expected Output

```
🚀 Starting MediaMTX at 127.0.0.1:8554...
✅ MediaMTX is ready.
📡 Pushing to: rtsp://127.0.0.1:8554/test
```

### Viewing the Stream

**VLC Media Player:**

```
File → Open Network Stream
rtsp://127.0.0.1:8554/test
```

**FFmpeg:**

```bash
ffplay rtsp://127.0.0.1:8554/test -rtsp_transport tcp
```

**GStreamer:**

```bash
gst-play-1.0 rtsp://127.0.0.1:8554/test
```

### Stopping the Stream

Press `Ctrl+C` to stop the stream. The script will gracefully shut down both FFmpeg and MediaMTX.

## Troubleshooting

### MediaMTX Failed to Start

- Verify MediaMTX path in `config.py` is correct
- Check that port 8554 is not already in use: `lsof -i :8554`
- Ensure MediaMTX binary has execute permissions: `chmod +x /path/to/mediamtx`

### FFmpeg Connection Failed

- Confirm MediaMTX is running (check port)
- Verify video file exists and is valid
- Check FFmpeg is installed: `ffmpeg -version`

### Port Already in Use

Change `RTSP_PORT` in `config.py` to an available port:

```python
RTSP_PORT = 8555  # Try a different port
```

### No Audio in Stream

Ensure your video file contains audio and:

```python
FFMPEG_SETTINGS["enable_audio"] = True
```

### High CPU Usage

Reduce bitrate or preset in `config.py`:

```python
FFMPEG_SETTINGS = {
    "preset": "ultrafast",
    "bitrate": "1000k",  # Lower bitrate
}
```

## Project Structure

```
streametrix/
├── run_mediamtx.py      # Main streaming script
├── config.py            # Configuration settings
├── benchmark.py         # Performance testing
├── create_stream.py     # Stream creation utilities
└── README.md            # This file
```

## Performance Tips

1. **Reduce Encoding Time**: Use `ultrafast` preset for low-latency streams
2. **Lower Bandwidth**: Reduce bitrate for slower networks
3. **FPS Adjustment**: Lower FPS for reduced CPU/bandwidth usage
4. **Resolution**: Transcode to lower resolution in FFmpeg if needed

## License

This project uses MediaMTX and FFmpeg. Please refer to their respective licenses.

## Support

For issues or questions:

- Check FFmpeg documentation: [ffmpeg.org](https://ffmpeg.org)
- MediaMTX docs: [github.com/bluenviron/mediamtx](https://github.com/bluenviron/mediamtx)
- FFmpeg wiki: [trac.ffmpeg.org](https://trac.ffmpeg.org)
