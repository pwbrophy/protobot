from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
from easing_functions import *
import numpy as np

import robot_leg_functions

hip_center = 90
hip_forwards = 60
hip_backwards = 120

knee_center = 80
knee_up = 40
knee_down = 90

hip_current_angle_a = hip_center
hip_current_angle_b = hip_center

knee_current_angle_a = knee_center
knee_current_angle_b = knee_center

robot_leg_functions.center_servos()

time.sleep(2)

phase_duration = 0.3
pause_between_phases = 0

phase_start_time = time.time()
number_of_servos = 12
number_of_phases = 4
current_phase = 0

walk_forwards_hip_phase_order = [hip_center, hip_forwards, hip_center, hip_backwards]
walk_forwards_knee_phase_order = [knee_up, knee_center, knee_down, knee_center]

hip_set_a = [0, 2, 4]
hip_set_b = [1, 3, 5]
knee_set_a = [6, 8, 10]
knee_set_b = [7, 9, 11]

right_hips = [0, 1, 2]
left_hips = [3, 4, 5]

while True:
    for phase in range(number_of_phases):
        # Generate smooth curves

        hip_curve_a = LinearInOut(start=hip_current_angle_a, end=walk_forwards_hip_phase_order[phase],
                                  duration=phase_duration)
        knee_curve_a = CubicEaseInOut(start=knee_current_angle_a, end=walk_forwards_knee_phase_order[phase],
                                      duration=phase_duration)

        phase_b = phase + 2

        if phase_b > number_of_phases - 1:
            phase_b = phase_b - 4

        hip_curve_b = LinearInOut(start=hip_current_angle_b, end=walk_forwards_hip_phase_order[phase_b],
                                  duration=phase_duration)
        knee_curve_b = CubicEaseInOut(start=knee_current_angle_b, end=walk_forwards_knee_phase_order[phase_b],
                                      duration=phase_duration)

        # hip_curve = CubicEaseInOut(start=hip_current_angle, end=walk_forwards_hip_phase_order[phase], duration=phase_duration)
        # knee_curve = CubicEaseInOut(start=knee_current_angle, end=walk_forwards_knee_phase_order[phase], duration=phase_duration)

        while True:
            current_time_from_zero = time.time() - phase_start_time

            for servo in hip_set_a:
                angle_for_this_servo = hip_curve_a.ease(current_time_from_zero)
                if servo in left_hips:
                    hip_offset = angle_for_this_servo - hip_center
                    angle_for_this_servo = hip_center - hip_offset
                kit.servo[servo].angle = angle_for_this_servo
            for servo in hip_set_b:
                angle_for_this_servo = hip_curve_b.ease(current_time_from_zero)
                if servo in left_hips:
                    hip_offset = angle_for_this_servo - hip_center
                    angle_for_this_servo = hip_center - hip_offset
                kit.servo[servo].angle = angle_for_this_servo

            for servo in knee_set_a:
                angle_for_this_servo = knee_curve_a.ease(current_time_from_zero)
                kit.servo[servo].angle = angle_for_this_servo
            for servo in knee_set_b:
                angle_for_this_servo = knee_curve_b.ease(current_time_from_zero)
                kit.servo[servo].angle = angle_for_this_servo

            if phase_duration < current_time_from_zero:
                hip_current_angle_a = walk_forwards_hip_phase_order[phase]
                hip_current_angle_b = walk_forwards_hip_phase_order[phase_b]
                knee_current_angle_a = walk_forwards_knee_phase_order[phase]
                knee_current_angle_b = walk_forwards_knee_phase_order[phase_b]
                phase_start_time = time.time()
                time.sleep(pause_between_phases)
                break
