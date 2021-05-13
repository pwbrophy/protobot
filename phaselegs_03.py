from adafruit_servokit import ServoKit
import time


from easing_functions import *
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
        hbox0 = HBox()
        hbox0.attr_class = "HBox"
        hbox0.attr_editor_newclass = False
        hbox0.css_align_items = "center"
        hbox0.css_display = "flex"
        hbox0.css_flex_direction = "row"
        hbox0.css_height = "250px"
        hbox0.css_justify_content = "space-around"
        hbox0.css_left = "184.234375px"
        hbox0.css_position = "absolute"
        hbox0.css_top = "118.21875px"
        hbox0.css_width = "250px"
        hbox0.variable_name = "hbox0"
        button0 = Button()
        button0.attr_class = "Button"
        button0.attr_editor_newclass = False
        button0.css_height = "30px"
        button0.css_order = "-1"
        button0.css_position = "static"
        button0.css_top = "206.21875px"
        button0.css_width = "100px"
        button0.text = "button"
        button0.variable_name = "button0"
        hbox0.append(button0,'button0')
        #hbox0.children['button0'].onmousedown.do(self.onmousedown_button0)
        #hbox0.children['button0'].onmouseup.do(self.onmouseup_button0)

        hbox0.children['button0'].ontouchstart.do(self.onmousedown_button0)
        hbox0.children['button0'].ontouchend.do(self.onmouseup_button0)

        self.thread_alive_flag = True
        self.my_thread_result = 0
        # Here I start a parallel thread that executes my algorithm for a long time
        t = threading.Thread(target=self.my_intensive_long_time_algorithm)
        t.start()

        # returning the root widget
        self.hbox0 = hbox0
        return self.hbox0

    def my_intensive_long_time_algorithm(self):
        print("Turn on robot walking function")
        robot_walk_forwards()

    def onmousedown_button0(self, emitter, x, y):
        global robot_is_walking
        robot_is_walking = True

    def onmouseup_button0(self, emitter, x, y):
        global robot_is_walking
        robot_is_walking = False


def on_close(self):
        self.thread_alive_flag = False
        super(MyApp, self).on_close()

def robot_walk_forwards():

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

    # Initialise the starting positions for the hips
    hip_current_angle_a = hip_center
    hip_current_angle_b = hip_center

    knee_current_angle_a = knee_center
    knee_current_angle_b = knee_center

    # Center the legs
    robot_leg_functions.center_servos(hip_center, knee_center, kit)

    # Pause before starting walk
    time.sleep(2)

    # Phases
    phase_duration = 0.3
    pause_between_phases = 0

    number_of_phases = 4
    current_phase = 0

    # Walk gait
    walk_forwards_hip_phase_order = [hip_center, hip_forwards, hip_center, hip_backwards]
    walk_forwards_knee_phase_order = [knee_up, knee_center, knee_down, knee_center]

    hip_set_a = [0, 2, 4]
    hip_set_b = [1, 3, 5]
    knee_set_a = [6, 8, 10]
    knee_set_b = [7, 9, 11]

    right_hips = [0, 1, 2]
    left_hips = [3, 4, 5]

    print("Starting our loop!")
    while True:
        if robot_is_walking:

            # Reset our timer
            phase_start_time = time.time()

            for phase in range(number_of_phases):

                # Generate smooth curves for 'set A' of legs
                hip_curve_a = LinearInOut(start=hip_current_angle_a, end=walk_forwards_hip_phase_order[phase],
                                          duration=phase_duration)
                knee_curve_a = CubicEaseInOut(start=knee_current_angle_a, end=walk_forwards_knee_phase_order[phase],
                                              duration=phase_duration)

                # Advance the phase by 2 for the alternate legs
                phase_b = phase + 2

                if phase_b > number_of_phases - 1:
                    phase_b = phase_b - 4

                # Generate smooth curves for 'set B' of legs

                hip_curve_b = LinearInOut(start=hip_current_angle_b, end=walk_forwards_hip_phase_order[phase_b],
                                          duration=phase_duration)
                knee_curve_b = CubicEaseInOut(start=knee_current_angle_b, end=walk_forwards_knee_phase_order[phase_b],
                                              duration=phase_duration)

                # hip_curve = CubicEaseInOut(start=hip_current_angle, end=walk_forwards_hip_phase_order[phase], duration=phase_duration)
                # knee_curve = CubicEaseInOut(start=knee_current_angle, end=walk_forwards_knee_phase_order[phase], duration=phase_duration)

                while True:

                    time.sleep(0.01)

                    # Start a timer for the phase
                    current_time_from_zero = time.time() - phase_start_time

                    # Go through each hip in set A
                    for servo in hip_set_a:

                        # Calculate how much we need to move based on time
                        angle_for_this_servo = hip_curve_a.ease(current_time_from_zero)

                        # If it's a left hip then flip the angle
                        if servo in left_hips:
                            hip_offset = angle_for_this_servo - hip_center
                            angle_for_this_servo = hip_center - hip_offset

                        # Move the hip
                        kit.servo[servo].angle = angle_for_this_servo

                    for servo in hip_set_b:
                        # Calculate how much we need to move based on time
                        angle_for_this_servo = hip_curve_b.ease(current_time_from_zero)

                        # If it's a left hip then flip the angle
                        if servo in left_hips:
                            hip_offset = angle_for_this_servo - hip_center
                            angle_for_this_servo = hip_center - hip_offset

                        # Move the hip
                        kit.servo[servo].angle = angle_for_this_servo

                    # Calculate and move the knees
                    for servo in knee_set_a:
                        angle_for_this_servo = knee_curve_a.ease(current_time_from_zero)
                        kit.servo[servo].angle = angle_for_this_servo
                    for servo in knee_set_b:
                        angle_for_this_servo = knee_curve_b.ease(current_time_from_zero)
                        kit.servo[servo].angle = angle_for_this_servo

                    # When the phase ends
                    if phase_duration < current_time_from_zero:
                        # Set the current angle to the target angle for each sevo type
                        hip_current_angle_a = walk_forwards_hip_phase_order[phase]
                        hip_current_angle_b = walk_forwards_hip_phase_order[phase_b]
                        knee_current_angle_a = walk_forwards_knee_phase_order[phase]
                        knee_current_angle_b = walk_forwards_knee_phase_order[phase_b]

                        # Reset the timer
                        phase_start_time = time.time()

                        # Break out and go to the next phase
                        break

# starts the web server
start(MyApp, debug=False, address='192.168.86.22', port=8081, start_browser=False, multiple_instance=True)
