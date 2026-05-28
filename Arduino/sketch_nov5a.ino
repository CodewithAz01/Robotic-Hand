#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial BTSerial(10, 11);  // RX | TX

Servo thumb, indexF, middleF, ringF, pinky;

void setup() {

  Serial.begin(115200);
  BTSerial.begin(115200);

  thumb.attach(7);
  indexF.attach(2);
  middleF.attach(5);
  ringF.attach(4);
  pinky.attach(3);

  openAllFingers();

  Serial.println("Robotic Hand Ready");
}

void loop() {

  if (BTSerial.available()) {

    String data = BTSerial.readStringUntil('\n');
    data.trim();

    Serial.println(data);

    // =========================
    // PYTHON MEDIAPIPE MODE
    // =========================
    if (data.length() == 5) {

      for (int i = 0; i < 5; i++) {

        int angle = (data[i] == '1') ? 0 : 180;

        switch (i) {

          case 0:
            thumb.write(angle);
            break;

          case 1:
            indexF.write(angle);
            break;

          case 2:
            middleF.write(angle);
            break;

          case 3:
            ringF.write(angle);
            break;

          case 4:
            pinky.write(angle);
            break;
        }
      }
    }

    // =========================
    // MOBILE APP MODE
    // =========================

    else {

      // THUMB
      if (data == "T1") thumb.write(180);
      if (data == "T0") thumb.write(0);

      // INDEX
      if (data == "I1") indexF.write(180);
      if (data == "I0") indexF.write(0);

      // MIDDLE
      if (data == "M1") middleF.write(180);
      if (data == "M0") middleF.write(0);

      // RING
      if (data == "R1") ringF.write(180);
      if (data == "R0") ringF.write(0);

      // PINKY
      if (data == "P1") pinky.write(180);
      if (data == "P0") pinky.write(0);
    }
  }
}

void openAllFingers() {

  thumb.write(0);
  indexF.write(0);
  middleF.write(0);
  ringF.write(0);
  pinky.write(0);
}