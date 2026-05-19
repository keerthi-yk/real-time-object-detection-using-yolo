# 🎯 Real-Time Object Detection using YOLOv8

> A real-time object detection system powered by **YOLOv8** that detects objects through a live webcam feed, estimates their distance, identifies their position in the frame, and announces them aloud using text-to-speech.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Known Issues](#known-issues)
- [License](#license)

---

## 📖 About the Project

This project is a real-time computer vision application that uses the **YOLOv8** (You Only Look Once) deep learning model to detect objects from a live webcam stream. It goes beyond basic detection by:

- **Estimating the distance** of detected objects from the camera using a focal-length-based formula.
- **Determining the spatial position** of each object (Left, Center, or Right) in the frame.
- **Announcing detections aloud** using a text-to-speech (TTS) engine — making it accessible and useful for assistive technology use cases.

This is ideal for learning computer vision, building accessibility tools, or prototyping smart surveillance systems.

---

## ✨ Features

- 🔍 **Real-time detection** via webcam using YOLOv8n (nano model — fast & lightweight)
- 📏 **Distance estimation** using pinhole camera model (focal length formula)
- 📍 **Positional awareness** — classifies objects as Left, Center, or Right
- 🔊 **Text-to-speech announcements** for each detected object
- 🟩 **Visual overlays** — bounding boxes, labels, distance, and position drawn on frame
- ⏱️ **Configurable run duration** (default: 60 seconds)
- 🛑 **Manual exit** by pressing `q`

---

## 🎬 Demo

```
[INFO] Starting Object Detection. Press 'q' to quit.
object: person detected on Center at 85.3 centimeters
object: bottle detected on Left at 42.1 centimeters
```

Each detected object is rendered on the live video frame with:
- A **green bounding box**
- **Label** (e.g., `person`, `bottle`, `car`)
- **Distance** in centimeters
- **Position** in the frame (Left / Center / Right)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Python 3.7+](https://www.python.org/) | Core language |
| [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) | Object detection model |
| [OpenCV](https://opencv.org/) | Video capture & frame rendering |
| [pyttsx3](https://pyttsx3.readthedocs.io/) | Offline text-to-speech |
| [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) | Audio I/O support |

---

## 📁 Project Structure

```
real-time-object-detection-using-yolo/
│
├── final_code.py                          # Main application script
├── yolov8n.pt                             # YOLOv8 nano pre-trained weights
├── yolov3.cfg                             # YOLOv3 configuration file (reference)
├── coco.names                             # COCO dataset class labels (80 classes)
├── PyAudio-0.2.11-cp37-cp37m-win_amd64.whl  # PyAudio wheel for Windows (Python 3.7)
└── README.md                              # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.7 or higher**
- A working **webcam**
- Windows / Linux / macOS

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/keerthi-yk/real-time-object-detection-using-yolo.git
   cd real-time-object-detection-using-yolo
   ```

2. **Create a virtual environment** *(recommended)*

   ```bash
   python -m venv venv
   source venv/bin/activate        # On Linux/macOS
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install ultralytics opencv-python pyttsx3
   ```

4. **Install PyAudio** *(Windows users)*

   If you're on Windows with Python 3.7, use the pre-built wheel included in the repo:

   ```bash
   pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
   ```

   For other platforms:

   ```bash
   pip install pyaudio
   ```

   > **Linux users:** You may need to install PortAudio first:
   > ```bash
   > sudo apt-get install portaudio19-dev
   > ```

5. **YOLOv8 weights**

   The `yolov8n.pt` model file is included in the repository. If it's missing, Ultralytics will automatically download it on first run.

---

### Running the Project

```bash
python final_code.py
```

- The webcam feed will open in a new window.
- Detected objects will be highlighted with bounding boxes and announced via TTS.
- The program runs for **60 seconds** by default, or press **`q`** to quit early.

---

## ⚙️ How It Works

### 1. Object Detection
YOLOv8 processes each frame from the webcam and returns bounding box coordinates, class labels, and confidence scores for all detected objects.

### 2. Distance Estimation
Distance is estimated using the **pinhole camera model**:

```
Distance (cm) = (Known Object Width × Focal Length) / Pixel Width of Object
```

| Parameter | Value |
|---|---|
| `KNOWN_WIDTH` | 20 cm (assumed average object width) |
| `FOCAL_LENGTH` | 615 pixels (calibrated for standard webcam) |

> **Note:** These constants are approximations. For higher accuracy, calibrate your specific camera using a reference object of known size.

### 3. Position Detection
The horizontal center of the bounding box is compared against frame thirds:

```
Left    → center_x < frame_width / 3
Center  → frame_width / 3 ≤ center_x ≤ 2 × frame_width / 3
Right   → center_x > 2 × frame_width / 3
```

### 4. Text-to-Speech Announcement
For every detected object, the system speaks:
> *"[Object] detected on [Position] at [Distance] centimeters"*

---

## 🔧 Configuration

You can tweak these constants in `final_code.py` to suit your setup:

```python
KNOWN_WIDTH = 20      # Estimated real-world width of objects in cm
FOCAL_LENGTH = 615    # Camera focal length in pixels (calibrate for accuracy)
```

To change the **run duration** (default 60 seconds):

```python
detect_objects(duration=60)   # Change 60 to any number of seconds
```

To use a **more accurate (but slower) model**, swap `yolov8n.pt` with a larger variant:

```python
model = YOLO("yolov8s.pt")   # Small model — better accuracy
model = YOLO("yolov8m.pt")   # Medium model — even better accuracy
```

Available YOLOv8 model sizes: `n` (nano) → `s` (small) → `m` (medium) → `l` (large) → `x` (extra-large)

---

## ⚠️ Known Issues

- **TTS blocking:** `pyttsx3.runAndWait()` is synchronous and may cause slight frame delays when many objects are detected. Consider using threading for smoother performance.
- **Distance accuracy:** The focal length and known width constants are approximations. Accuracy varies by camera and object type. Camera calibration is recommended for precise measurements.
- **PyAudio on Windows:** Only a Python 3.7 wheel is bundled. For Python 3.8+, download the appropriate wheel from [Christoph Gohlke's repository](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for the state-of-the-art detection model
- [COCO Dataset](https://cocodataset.org/) for the 80-class object labels
- [OpenCV](https://opencv.org/) for computer vision utilities

---

*Built with ❤️ by [keerthi-yk](https://github.com/keerthi-yk)*
