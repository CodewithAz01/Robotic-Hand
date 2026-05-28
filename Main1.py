import sys
import cv2
import mediapipe as mp
import serial
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QTextEdit
)
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer


class RoboticHandUI(QWidget):

    def __init__(self):
        super().__init__()

        # ------------------ WINDOW ------------------
        self.setWindowTitle("AI Robotic Hand Controller")
        self.setGeometry(100, 50, 1300, 800)

        # ------------------ SERIAL ------------------
        self.bt = None
        self.bluetooth_connected = False

        try:
            self.bt = serial.Serial('COM10', 115200, timeout=1)
            time.sleep(2)
            self.bluetooth_connected = True
            print("[INFO] HC-05 Connected")
        except:
            print("[ERROR] HC-05 Not Connected")

        # ------------------ MEDIAPIPE ------------------
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8,
            max_num_hands=1
        )

        self.finger_tips = [4, 8, 12, 16, 20]

        # ------------------ CAMERA ------------------
        self.cap = cv2.VideoCapture(0)
        self.camera_running = False

        # ------------------ MAIN LAYOUT ------------------
        main_layout = QHBoxLayout()

        # ------------------ LEFT PANEL ------------------
        left_layout = QVBoxLayout()

        title = QLabel("AI ROBOTIC HAND")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: white;
            padding: 15px;
        """)

        self.video_label = QLabel()
        self.video_label.setFixedSize(850, 650)
        self.video_label.setStyleSheet("""
            background-color: #1e1e1e;
            border-radius: 20px;
            border: 3px solid #00e5ff;
        """)

        self.status_box = QTextEdit()
        self.status_box.setFixedHeight(100)
        self.status_box.setReadOnly(True)
        self.status_box.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255,255,255,0.08);
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
        """)

        left_layout.addWidget(title)
        left_layout.addWidget(self.video_label)
        left_layout.addWidget(self.status_box)

        # ------------------ RIGHT PANEL ------------------
        right_layout = QVBoxLayout()

        # BUTTON STYLE
        button_style = """
            QPushButton {
                background-color: qlineargradient(
                    spread:pad,
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #00c6ff,
                    stop:1 #0072ff
                );
                color: white;
                border-radius: 18px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #00e5ff;
            }
        """

        # ------------------ CONTROL BUTTONS ------------------
        self.start_btn = QPushButton("▶ Start Camera")
        self.start_btn.setStyleSheet(button_style)
        self.start_btn.clicked.connect(self.start_camera)

        self.stop_btn = QPushButton("⏹ Stop Camera")
        self.stop_btn.setStyleSheet(button_style)
        self.stop_btn.clicked.connect(self.stop_camera)

        self.thumb_btn = QPushButton("👍 Thumbs Up")
        self.thumb_btn.setStyleSheet(button_style)
        self.thumb_btn.clicked.connect(self.thumbs_up)

        self.spider_btn = QPushButton("🕷 Spider Gesture")
        self.spider_btn.setStyleSheet(button_style)
        self.spider_btn.clicked.connect(self.spider_gesture)

        self.fist_btn = QPushButton("✊ Fist")
        self.fist_btn.setStyleSheet(button_style)
        self.fist_btn.clicked.connect(self.fist_gesture)

        self.open_btn = QPushButton("🖐 Open Hand")
        self.open_btn.setStyleSheet(button_style)
        self.open_btn.clicked.connect(self.open_hand)

        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.setStyleSheet(button_style)
        self.reset_btn.clicked.connect(self.reset_hand)

        self.exit_btn = QPushButton("❌ Exit")
        self.exit_btn.setStyleSheet(button_style)
        self.exit_btn.clicked.connect(self.close_application)

        # ADD BUTTONS
        right_layout.addStretch()
        right_layout.addWidget(self.start_btn)
        right_layout.addWidget(self.stop_btn)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.thumb_btn)
        right_layout.addWidget(self.spider_btn)
        right_layout.addWidget(self.fist_btn)
        right_layout.addWidget(self.open_btn)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.reset_btn)
        right_layout.addWidget(self.exit_btn)
        right_layout.addStretch()

        # ------------------ MAIN LAYOUT ADD ------------------
        main_layout.addLayout(left_layout, 70)
        main_layout.addLayout(right_layout, 30)

        self.setLayout(main_layout)

        # ------------------ WINDOW STYLE ------------------
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    spread:pad,
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #141e30,
                    stop:1 #243b55
                );
            }
        """)

        # ------------------ TIMER ------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.last_send_time = 0
        self.send_interval = 0.05

    # ==========================================================
    # CAMERA START
    # ==========================================================

    def start_camera(self):
        self.camera_running = True
        self.timer.start(20)
        self.log("Camera Started")

    # ==========================================================
    # CAMERA STOP
    # ==========================================================

    def stop_camera(self):
        self.camera_running = False
        self.timer.stop()
        self.video_label.clear()
        self.log("Camera Stopped")

    # ==========================================================
    # UPDATE FRAME
    # ==========================================================

    def update_frame(self):

        if not self.camera_running:
            return

        success, img = self.cap.read()

        if not success:
            return

        img = cv2.flip(img, 1)

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        h, w, c = img.shape

        if results.multi_hand_landmarks:

            for handLms, handType in zip(results.multi_hand_landmarks, results.multi_handedness):

                self.mp_draw.draw_landmarks(
                    img,
                    handLms,
                    self.mp_hands.HAND_CONNECTIONS
                )

                lmList = []
                x_list, y_list = [], []

                for id, lm in enumerate(handLms.landmark):

                    px, py = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, px, py])
                    x_list.append(px)
                    y_list.append(py)

                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)

                cv2.rectangle(
                    img,
                    (xmin - 20, ymin - 20),
                    (xmax + 20, ymax + 20),
                    (0, 255, 255),
                    3
                )

                handLabel = handType.classification[0].label

                fingers = []

                # THUMB
                if handLabel == "Right":
                    fingers.append(1 if lmList[4][1] < lmList[3][1] else 0)
                else:
                    fingers.append(1 if lmList[4][1] > lmList[3][1] else 0)

                # OTHER FINGERS
                for id in range(1, 5):
                    fingers.append(
                        1 if lmList[self.finger_tips[id]][2] < lmList[self.finger_tips[id]-2][2] else 0
                    )

                # SEND DATA
                if time.time() - self.last_send_time > self.send_interval:

                    data_str = ''.join(str(bit) for bit in fingers) + '\n'

                    if self.bluetooth_connected:
                        self.bt.write(data_str.encode())

                    self.last_send_time = time.time()

                cv2.putText(
                    img,
                    f"Fingers: {fingers}",
                    (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 0),
                    2
                )

        # CONVERT IMAGE
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w

        convert_to_qt = QImage(
            rgb_image.data,
            w,
            h,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        pixmap = QPixmap.fromImage(convert_to_qt)

        self.video_label.setPixmap(
            pixmap.scaled(
                self.video_label.width(),
                self.video_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
        )

    # ==========================================================
    # SEND COMMAND
    # ==========================================================

    def send_command(self, command):

        if self.bluetooth_connected:
            self.bt.write((command + '\n').encode())
            self.log(f"Sent Command: {command}")

    # ==========================================================
    # GESTURES
    # ==========================================================

    def thumbs_up(self):
        self.send_command("10000")

    def spider_gesture(self):
        self.send_command("11001")

    def fist_gesture(self):
        self.send_command("00000")

    def open_hand(self):
        self.send_command("11111")

    def reset_hand(self):
        self.send_command("11111")
        self.log("Hand Reset")

    # ==========================================================
    # LOG BOX
    # ==========================================================

    def log(self, message):
        self.status_box.append(f"[INFO] {message}")

    # ==========================================================
    # EXIT
    # ==========================================================

    def close_application(self):

        self.timer.stop()

        if self.cap.isOpened():
            self.cap.release()

        if self.bluetooth_connected:
            self.bt.close()

        self.close()


# ==========================================================
# MAIN
# ==========================================================

app = QApplication(sys.argv)
window = RoboticHandUI()
window.show()
sys.exit(app.exec())
