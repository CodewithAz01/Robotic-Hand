# 🤖 AI Robotic Hand Controller

A real-time AI-powered robotic hand controlled using **MediaPipe hand tracking**, **Python**, **PyQt6 GUI**, **Arduino UNO**, **HC-05 Bluetooth module**, and **Servo Motors**.

This project detects human hand gestures using a webcam and mirrors the finger movements on a robotic hand in real time.

---

# 📸 Features

✅ Real-time hand tracking using MediaPipe
✅ Finger gesture detection
✅ Bluetooth communication with HC-05
✅ Robotic hand finger movement control
✅ Modern PyQt6 graphical user interface
✅ Live webcam feed inside UI
✅ Gesture buttons for predefined actions
✅ Open Hand / Fist / Spider Gesture support
✅ Start & Stop camera controls
✅ Reset hand feature
✅ Attractive modern interface

---

# 🛠 Hardware Used

| Component              | Quantity |
| ---------------------- | -------- |
| Arduino UNO R3         | 1        |
| HC-05 Bluetooth Module | 1        |
| SG90 Servo Motors      | 5        |
| 5V 4A Power Supply     | 1        |
| 1000uF Capacitor       | 1        |
| Breadboard             | 1        |
| Jumper Wires           | Multiple |

---

# 💻 Software & Libraries Used

## Python Libraries

* OpenCV
* MediaPipe
* PyQt6
* PySerial

Install all required libraries:

```bash
pip install opencv-python mediapipe pyqt6 pyserial
```

---

# 🧠 How It Works

1. The webcam captures the user's hand.
2. MediaPipe detects hand landmarks.
3. Finger states are calculated.
4. Python sends finger data via Bluetooth.
5. HC-05 receives the data on Arduino UNO.
6. Arduino controls 5 servo motors.
7. The robotic hand mimics the user's hand movement in real time.

---

# 🔌 Bluetooth Communication

The project uses:

* HC-05 Bluetooth Module
* Baud Rate: `115200`

Python sends data like:

```text
10101
```

Each digit represents one finger:

| Finger | Value  |
| ------ | ------ |
| 1      | Open   |
| 0      | Closed |

---

# 🎮 Predefined Gestures

| Gesture           | Command |
| ----------------- | ------- |
| 👍 Thumbs Up      | `10000` |
| ✊ Fist            | `00000` |
| 🖐 Open Hand      | `11111` |
| 🕷 Spider Gesture | `10101` |

---

# 🧩 Project Structure

```text
project-folder/
│
├── robotic_hand_ui.py
├── arduino_code.ino
├── requirements.txt
└── README.md
```

---

# ⚡ Arduino Wiring

## HC-05 Connections

| HC-05 | Arduino UNO |
| ----- | ----------- |
| TX    | Pin 10      |
| RX    | Pin 11      |
| VCC   | 5V          |
| GND   | GND         |

## Servo Connections

| Finger | Arduino Pin |
| ------ | ----------- |
| Thumb  | 7           |
| Index  | 2           |
| Middle | 5           |
| Ring   | 4           |
| Pinky  | 3           |

---

# 🚀 Running the Project

## Step 1 — Upload Arduino Code

Upload the Arduino sketch using Arduino IDE.

---

## Step 2 — Pair HC-05

Pair HC-05 with your computer.

Default password:

```text
1234
```

or

```text
0000
```

---

## Step 3 — Run Python Application

```bash
python robotic_hand_ui.py
```

---

# 🖥 PyQt6 User Interface

The application includes:

* Live camera feed
* Gesture controls
* Bluetooth communication
* Real-time hand tracking
* Robotic hand commands

---

# 📦 Convert to EXE

Using PyInstaller:

```bash
pyinstaller --onefile --windowed --collect-all mediapipe --collect-all PyQt6 robotic_hand_ui.py
```

---

# 🔮 Future Improvements

* Voice command control
* ESP32 wireless control
* Flex sensor glove
* Mobile app integration
* AI gesture learning
* 3D printed robotic hand
* Web dashboard
* Wi-Fi control

---

# 🙌 Credits

Developed using:

* Python
* Arduino
* OpenCV
* MediaPipe
* PyQt6

---

# 📜 License

This project is open-source and free to use for learning and educational purposes.

# 🚀 Created by Abdullah Zahid 
