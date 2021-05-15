from adafruit_servokit import ServoKit
import time

import numpy as np

import robot_leg_functions

from remi.gui import *
from remi import start, App

import threading


# Walking state
global robot_is_walking
robot_is_walking = False

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        svg0 = Svg()
        svg0.attr_class = "Svg"
        svg0.attr_editor_newclass = False
        svg0.css_height = "255.0px"
        svg0.css_left = "60.0px"
        svg0.css_position = "absolute"
        svg0.css_top = "60.0px"
        svg0.css_width = "270.0px"
        svg0.variable_name = "svg0"
        svgcircle0 = SvgCircle()
        svgcircle0.attr_class = "SvgCircle"
        svgcircle0.attr_cx = 135.0
        svgcircle0.attr_cy = 120.0
        svgcircle0.attr_editor_newclass = False
        svgcircle0.attr_fill = "rgb(200,200,200)"
        svgcircle0.attr_r = "90.0"
        svgcircle0.attr_stroke = "rgb(0,0,0)"
        svgcircle0.css_left = "190.875px"
        svgcircle0.css_top = "165.90625px"
        svgcircle0.variable_name = "svgcircle0"
        svg0.append(svgcircle0,'svgcircle0')
        svg0.ontouchstart.do(self.walk_forwards_begin)
        svg0.ontouchend.do(self.walk_forwards_end)

        self.thread_alive_flag = True
        self.my_thread_result = 0
        # Here I start a parallel thread that executes my algorithm for a long time
        t = threading.Thread(target=turn_on_robot_locomotion)
        t.start()

        # returning the root widget
        self.svg0 = svg0
        return self.svg0

    def walk_forwards_begin(self, emitter, x, y):
        global robot_is_walking
        robot_is_walking = True

    def walk_forwards_end(self, emitter, x, y):
        global robot_is_walking
        robot_is_walking = False


def on_close(self):
    self.thread_alive_flag = False
    super(MyApp, self).on_close()


def turn_on_robot_locomotion():

    kit = ServoKit(channels=16)

    number_of_servos = 12
    global robot_is_walking
    robot_is_walking = False

    # Define hip positions
    hip_center = 90
    hip_forwards = 60
    hip_backwards = 120

    # Define knee positions
    knee_center = 80
    knee_up = 40
    knee_down = 90

    # Center the legs
    robot_leg_functions.center_servos(hip_center, knee_center, kit)

    # Pause before starting walk
    time.sleep(2)

    # Phases
    phase_duration = 0.3
    number_of_phases = 4
    phase = 0

    # Walk forwards gait
    walk_forwards_hip_phase_order = [hip_center, hip_forwards, hip_center, hip_backwards]
    walk_forwards_knee_phase_order = [knee_up, knee_center, knee_down, knee_center]
    # Smoothing 0 - ease both, 1 - ease out from current, 2 = ease in to next, 3 = linear
    walk_forwards_hip_smooth = [2, 1, 2, 1]
    walk_forwards_knee_smooth = [0, 0, 0, 0]

    # Set each servo parameters
    servo_params = []

    for servo in range(0, number_of_servos):
        servo_params.append(0)

    # Hip = True /// Set A = True /// Right = True
    servo_params[0] = [True, True, True]
    servo_params[1] = [True, False, True]
    servo_params[2] = [True, True, True]
    servo_params[3] = [True, False, False]
    servo_params[4] = [True, True, False]
    servo_params[5] = [True, False, False]
    servo_params[6] = [False, True, True]
    servo_params[7] = [False, False, True]
    servo_params[8] = [False, True, True]
    servo_params[9] = [False, False, False]
    servo_params[10] = [False, True, False]
    servo_params[11] = [False, False, False]

    # Initialise the list of servo current angles
    servo_current_position = []

    for servo in range(0, number_of_servos):
        servo_current_position.append(0)

    # Set the starting angle for all of the hips
    for hip in range(0, 6):
        servo_current_position[hip] = hip_center

    # Set the starting angle for all of the knees
    for knee in range(6, 12):
        servo_current_position[knee] = knee_center

    # Initialise our list which stores the servo curves
    servo_curves = []
    for servo in range(0, number_of_servos):
        servo_curves.append(0)

    print("Starting our loop!")
    while True:
        if robot_is_walking:
            # Set our timer for the first loop
            phase_start_time = time.time()

            # Generate curve for each servo
            for servo in range(0, number_of_servos):
                this_servo_current_position = servo_current_position[servo]
                this_servo_params = servo_params[servo]
                # servo number | start position | servo parameters | phase
                servo_curves[servo] = robot_leg_functions.generate_servo_movement_curve(this_servo_current_position,
                                                                                        this_servo_params,
                                                                                        phase,
                                                                                        walk_forwards_hip_phase_order,
                                                                                        walk_forwards_hip_smooth,
                                                                                        walk_forwards_knee_phase_order,
                                                                                        walk_forwards_knee_smooth,
                                                                                        phase_duration,
                                                                                        hip_center,
                                                                                        knee_center
                                                                                        )

            while True:
                # Sleep a bit so that we don't hammer the processor
                time.sleep(0.005)

                # Start a timer for the phase
                current_time_from_zero = time.time() - phase_start_time

                # Go through each servo
                for servo in range(0, number_of_servos):

                    # Calculate how much we need to move based on time
                    angle_for_this_servo = servo_curves[servo].ease(current_time_from_zero)

                    # Apply turning multiplier
                    servo_params_for_turning = servo_params[servo]
                    # Right hips
                    if servo_params_for_turning[0] and servo_params_for_turning[2]:
                        if servo == 1:
                            print("this servo is moving to ",angle_for_this_servo," and the center is ", hip_center)
                        offset = angle_for_this_servo - hip_center
                        if servo == 1:
                            print("offset is", offset)
                        offset = offset*(-1)
                        if servo == 1:
                            print("multiplied offset is ", offset)
                        angle_for_this_servo = hip_center + offset
                        if servo == 1:
                            print("final angle for servo is ",angle_for_this_servo)
                    # Left hips
                    #if servo_params_for_turning[0] and not servo_params_for_turning[2]:
                    #    offset = angle_for_this_servo - hip_center
                    #    #offset = offset*(1)
                    #    angle_for_this_servo = hip_center + offset

                    # Move the servo
                    kit.servo[servo].angle = angle_for_this_servo

                    # Record the current angle for each servo
                    servo_current_position[servo] = angle_for_this_servo

                # When the phase ends
                if phase_duration < current_time_from_zero or not robot_is_walking:

                    # Reset the timer
                    phase_start_time = time.time()

                    # Move to the next phase
                    phase += 1
                    phase = phase % 4

                    # Break out and go to the next phase
                    break

# starts the web server
start(MyApp, debug=False, address='192.168.86.22', port=8081, start_browser=False, multiple_instance=True)
