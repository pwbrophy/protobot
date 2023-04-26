from adafruit_servokit import ServoKit
import time
import robot_leg_functions
from remi.gui import *
from remi import start, App

import threading

global robot_is_walking
robot_is_walking = False

global robot_is_stopping
robot_is_stopping = False

global turning_speed
turning_speed = 0

global moving_speed
moving_speed = 0


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        svg0 = Svg()
        svg0.attr_class = "Svg"
        svg0.attr_editor_newclass = False
        svg0.css_height = "200px"
        svg0.css_left = "150.0px"
        svg0.css_position = "absolute"
        svg0.css_top = "135.0px"
        svg0.css_width = "200px"
        svg0.variable_name = "svg0"
        svgcircle0 = SvgCircle()
        svgcircle0.attr_class = "SvgCircle"
        svgcircle0.attr_cx = 100.0
        svgcircle0.attr_cy = 100.0
        svgcircle0.attr_editor_newclass = False
        svgcircle0.attr_fill = "rgb(200,200,200)"
        svgcircle0.attr_r = "100.0"
        svgcircle0.attr_stroke = "rgb(0,0,0)"
        svgcircle0.css_left = "190.875px"
        svgcircle0.css_top = "165.90625px"
        svgcircle0.variable_name = "svgcircle0"
        svg0.append(svgcircle0,'svgcircle0')
        svg0.ontouchstart.do(self.walk_forwards_begin)
        svg0.ontouchend.do(self.walk_forwards_end)
        svg0.ontouchmove.do(self.update_movement)



        self.thread_alive_flag = True
        self.my_thread_result = 0
        # Here I start a parallel thread that executes my algorithm for a long time!
        t = threading.Thread(target=turn_on_robot_locomotion)
        t.start()

        # returning the root widget
        self.svg0 = svg0
        return self.svg0

    def walk_forwards_begin(self, emitter, x, y):
        self.update_turning(x, y)
        global robot_is_walking
        robot_is_walking = True

        global robot_is_stopping
        robot_is_stopping = False

    def walk_forwards_end(self, emitter, x, y):
        global robot_is_walking
        robot_is_walking = False

    def update_movement(self, emitter, x, y):
        self.update_turning(x, y)
        # print("xpos is", x_pos)

    def update_turning(self, x, y):
        x_pos = float(x)
        y_pos = float(y)

        global turning_speed
        global moving_speed

        if 0.0 < x_pos < 200:
            x_pos = x_pos - 100
            x_pos = x_pos / 100
            turning_speed = x_pos

        if 0.0 < y_pos < 200:
            y_pos = y_pos / 200
            moving_speed = y_pos

def on_close(self):
    self.thread_alive_flag = False
    super(MyApp, self).on_close()


def turn_on_robot_locomotion():

    kit = ServoKit(channels=16)

    number_of_servos = 12

    global robot_is_walking
    robot_is_walking = False
    global robot_is_stopping

    robot_is_stopping = False

    # Define hip positions
    hip_forwards = 0
    hip_center = 90
    hip_backwards = 180

    # Define knee positions
    knee_up = 0
    knee_center = 160
    knee_down = 180

    # Center the legs
    robot_leg_functions.center_servos(hip_center, knee_down, kit)

    # Pause before starting walk
    # time.sleep(2)

    # Phases
    phase_duration = 0.6
    phase_duration_max = 1.4
    phase_duration_min = 0.4
    phase = 0
    phase_duration_multiplier = [1, 1, 1, 1]

    # Walk forwards gait
    walk_forwards_hip_phase_order = [hip_center, hip_forwards, hip_center, hip_backwards]
    walk_forwards_knee_phase_order = [knee_up, knee_center, knee_down, knee_center]
    # Smoothing 0 - ease both, 1 - ease out from current, 2 = ease in to next, 3 = linear
    walk_forwards_hip_smooth = [1, 2, 1, 2]
    walk_forwards_knee_smooth = [2, 1, 2, 1]

    # Stopping gait raised leg
    stop_raised_hip_phase_order = [-1, hip_center, -1, -1]
    stop_raised_knee_phase_order = [-1, knee_down, -1, -1]
    # Smoothing 0 - ease both, 1 - ease out from current, 2 = ease in to next, 3 = linear
    stop_raised_hip_smooth = [0, 0, 0, 0]
    stop_raised_knee_smooth = [0, 0, 0, 0]

    # Stopping gait down leg
    stop_down_hip_phase_order = [-1, hip_center, -1, -1]
    stop_down_knee_phase_order = [-1, -1, -1,-1]
    # Smoothing 0 - ease both, 1 - ease out from current, 2 = ease in to next, 3 = linear
    stop_down_hip_smooth = [0, 0, 0, 0]
    stop_down_knee_smooth = [0, 0, 0, 0]

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

    use_current_position = False

    turning_speed_smooth = 0

    print("Starting our loop!")
    while True:
        if robot_is_walking:
            # Set our timer for the first loop
            phase_start_time = time.time()
            # Calculate the phase duration based on input
            phase_range = phase_duration_max - phase_duration_min
            phase_duration = ((moving_speed * phase_range) + phase_duration_min)*phase_duration_multiplier[phase]

            global turning_speed

            for servo in range(0, number_of_servos):  # Generate curve for each servo
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
                                                                                        knee_center,
                                                                                        2,
                                                                                        turning_speed,
                                                                                        use_current_position
                                                                                        )

            use_current_position = False

            while True:  # This loop cycles through each servo and moves it towards the target until the phase ends

                # Sleep a bit so that we don't hammer the processor
                time.sleep(0.005)

                # Start a timer for the phase
                current_time_from_zero = time.time() - phase_start_time

                # Go through each servo
                for servo in range(0, number_of_servos):

                    # Calculate how much we need to move based on time
                    angle_for_this_servo = servo_curves[servo].ease(current_time_from_zero)

                    # Move the servo
                    angle_for_this_servo = max(0, min(angle_for_this_servo, 180))
                    hacked_angle_for_this_servo = 180-angle_for_this_servo
                    if servo <=5:
                        kit.servo[servo].angle = angle_for_this_servo
                    if servo > 5:
                        kit.servo[servo].angle = hacked_angle_for_this_servo

                    # Record the current angle for each servo ha
                    servo_current_position[servo] = angle_for_this_servo

                # When the phase ends
                if phase_duration <= current_time_from_zero:

                    # Reset the timer
                    phase_start_time = time.time()

                    # Move to the next phase
                    phase += 1
                    phase = phase % 4

                    # Break out and go to the next phase
                    break

                if not robot_is_walking:

                    # Stop the robot
                    robot_is_stopping = True

                    break

        if robot_is_stopping:
            print("robot has started stopping!")
            current_walking_phase = phase
            phase = 0
            use_current_position = True


            # Check which phase we're in and which legs are up or down
            if current_walking_phase == 0 or current_walking_phase == 1:
                LegsWhichAreUp = True
                LegsWhichAreDown = False

            if current_walking_phase == 2 or current_walking_phase == 3:
                LegsWhichAreUp = False
                LegsWhichAreDown = True

            # This is used to stop the steering
            # turning_while_stopping = turning_speed

            while True:  # Cycle through each phase until the robot has finished stopping

                if not robot_is_stopping:
                    break

                # Set our timer for the first loop
                phase_start_time = time.time()

                for servo in range(0, number_of_servos):  # Generate curve for each servo
                    # If this servo is part of a set which is raised, used the raised stop gait
                    if servo_params[servo][1] == LegsWhichAreUp:
                        hip_phase_order = stop_raised_hip_phase_order
                        hip_smooth = stop_raised_hip_smooth
                        knee_phase_order = stop_raised_knee_phase_order
                        knee_smooth = stop_raised_knee_smooth

                    # If this servo is part of a set which is down, use the down stop gait

                    if servo_params[servo][1] == LegsWhichAreDown:
                        hip_phase_order = stop_down_hip_phase_order
                        hip_smooth = stop_down_hip_smooth
                        knee_phase_order = stop_down_knee_phase_order
                        knee_smooth = stop_down_knee_smooth

                    this_servo_current_position = servo_current_position[servo]
                    this_servo_params = servo_params[servo]

                    # servo number | start position | servo parameters | phase
                    servo_curves[servo] = robot_leg_functions.generate_servo_movement_curve(this_servo_current_position,
                                                                                            this_servo_params,
                                                                                            phase,
                                                                                            hip_phase_order,
                                                                                            hip_smooth,
                                                                                            knee_phase_order,
                                                                                            knee_smooth,
                                                                                            phase_duration,
                                                                                            hip_center,
                                                                                            knee_center,
                                                                                            0,
                                                                                            0,
                                                                                            use_current_position
                                                                                            )


                use_current_position = False

                while True:  # This loop cycles through each servo and moves it towards the target until the phase ends

                    # Sleep a bit so that we don't hammer the processor
                    # time.sleep(0.005)

                    # Start a timer for the phase
                    current_time_from_zero = time.time() - phase_start_time

                    # Go through each servo
                    for servo in range(0, number_of_servos):

                        # Calculate how much we need to move based on time
                        angle_for_this_servo = servo_curves[servo].ease(current_time_from_zero)
                        angle_for_this_servo = max(0, min(angle_for_this_servo, 180))
                        hacked_angle_for_this_servo = 180-angle_for_this_servo
                        if servo <=5:
                            kit.servo[servo].angle = angle_for_this_servo
                        if servo > 5:
                            kit.servo[servo].angle = hacked_angle_for_this_servo

                        # Record the current angle for each servo ha
                        servo_current_position[servo] = angle_for_this_servo

                    # When the phase ends
                    if phase_duration < current_time_from_zero:

                        # Reset the timer
                        phase_start_time = time.time()

                        if phase == 3:
                            robot_is_stopping = False
                            use_current_position = True
                            for servo in range(0, number_of_servos):  # Turn off all the servos
                                kit.servo[servo].angle = None
                            break
                        # Move to the next phase
                        phase += 1
                        break

# starts the web server
start(MyApp, debug=False, address='192.168.86.40', port=8081, start_browser=False, multiple_instance=False)


