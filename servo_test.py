from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

servos = []

for servo in range(12):
    servos.append(servo)

for servo in servos:
    kit.servo[servo].angle = 0
    for i in range(1):
        for angle in range(0, 180, 3):
            kit.servo[servo].angle = angle
            time.sleep(0.01)
        for angle in range(180, 0, -3):
            kit.servo[servo].angle = angle
            time.sleep(0.01)
    if servo < 6:
        kit.servo[servo].angle = 90
    if servo > 5:
        kit.servo[servo].angle = 180
    time.sleep(1)
    kit.servo[servo].angle = None

