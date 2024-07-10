import curses
import pigpio
import sys
from time import sleep

# GPIO Pin Definitions for L298N Motor Driver
ENA = 17  # Enable A - Motor A PWM
IN1 = 23  # Motor A Input 1
IN2 = 24  # Motor A Input 2
ENB = 22  # Enable B - Motor B PWM
IN3 = 27  # Motor B Input 3
IN4 = 4   # Motor B Input 4

# GPIO Pin Definitions for Servos
SERVO1 = 6  # Pan servo
SERVO2 = 5  # Tilt servo

pi = pigpio.pi()

# Initial setup for GPIO
pi.set_mode(ENA, pigpio.OUTPUT)
pi.set_mode(ENB, pigpio.OUTPUT)
pi.set_mode(IN1, pigpio.OUTPUT)
pi.set_mode(IN2, pigpio.OUTPUT)
pi.set_mode(IN3, pigpio.OUTPUT)
pi.set_mode(IN4, pigpio.OUTPUT)

pi.set_mode(SERVO1, pigpio.OUTPUT)
pi.set_mode(SERVO2, pigpio.OUTPUT)

# Set the initial state for motors
pi.write(IN1, 0)
pi.write(IN2, 0)
pi.write(IN3, 0)
pi.write(IN4, 0)

# Initial servo positions (midpoint of 1500us)
servo1_position = 1000
servo2_position = 1000
pi.set_servo_pulsewidth(SERVO1, servo1_position)
pi.set_servo_pulsewidth(SERVO2, servo2_position)

# Function to display the screen
def display(stdscr):
    stdscr.addstr(0, 0, "SIMPLE DRIVE 2")
    rows, cols = stdscr.getmaxyx()
    screenDetailText = f"This screen is [{rows}] high and [{cols}] across."
    startingXPos = int((cols - len(screenDetailText)) / 2)
    stdscr.addstr(3, startingXPos, screenDetailText)
    stdscr.addstr(4, startingXPos, "Use arrow keys to drive")
    stdscr.addstr(5, cols - len("Press a key to quit."), "Press a key to quit.")
    stdscr.addstr(6, startingXPos, "Use 'W' and 'S' to control Pan Servo")
    stdscr.addstr(7, startingXPos, "Use 'A' and 'D' to control Tilt Servo")

# Function to control the motors
def control(key, throttle):
    if key == curses.KEY_RIGHT:
        # Right turn: Motor A forward, Motor B backward
        pi.write(IN1, 0)
        pi.write(IN2, 1)
        pi.set_PWM_dutycycle(ENA, throttle)  # Motor A PWM forward
        pi.write(IN3, 0)
        pi.write(IN4, 1)
        pi.set_PWM_dutycycle(ENB, throttle)  # Motor B PWM backward
    elif key == curses.KEY_LEFT:
        # Left turn: Motor A backward, Motor B forward
        pi.write(IN1, 1)
        pi.write(IN2, 0)
        pi.set_PWM_dutycycle(ENA, throttle)  # Motor A PWM backward
        pi.write(IN3, 1)
        pi.write(IN4, 0)
        pi.set_PWM_dutycycle(ENB, throttle)  # Motor B PWM forward
    elif key == curses.KEY_UP:
        # Move forward: Both motors forward
        pi.write(IN1, 0)
        pi.write(IN2, 1)
        pi.set_PWM_dutycycle(ENA, throttle)  # Motor A PWM forward
        pi.write(IN3, 1)
        pi.write(IN4, 0)
        pi.set_PWM_dutycycle(ENB, throttle)  # Motor B PWM forward
    elif key == curses.KEY_DOWN:
        # Move backward: Both motors backward
        pi.write(IN1, 1)
        pi.write(IN2, 0)
        pi.set_PWM_dutycycle(ENA, throttle)  # Motor A PWM backward
        pi.write(IN3, 0)
        pi.write(IN4, 1)
        pi.set_PWM_dutycycle(ENB, throttle)  # Motor B PWM backward
    else:
        # Stop
        brakes()

# Function to control the servos
def control_servo(key):
    global servo1_position, servo2_position
    step = 10
    if key == ord('w'):
        # Pan up
        servo1_position = min(servo1_position + step, 2500)
        pi.set_servo_pulsewidth(SERVO1, servo1_position)
    elif key == ord('s'):
        # Pan down
        servo1_position = max(servo1_position - step, 500)
        pi.set_servo_pulsewidth(SERVO1, servo1_position)
    elif key == ord('a'):
        # Tilt left
        servo2_position = min(servo2_position + step, 2500)
        pi.set_servo_pulsewidth(SERVO2, servo2_position)
    elif key == ord('d'):
        # Tilt right
        servo2_position = max(servo2_position - step, 500)
        pi.set_servo_pulsewidth(SERVO2, servo2_position)

# Function to stop all motors
def brakes():
    pi.set_PWM_dutycycle(ENA, 0)
    pi.set_PWM_dutycycle(ENB, 0)
    pi.write(IN1, 0)
    pi.write(IN2, 0)
    pi.write(IN3, 0)
    pi.write(IN4, 0)

# Main function to handle the user interface and motor control
def main(stdscr):
    stdscr.clear()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    throttle = 190  # Initial throttle setting (0=stopped, 255=max speed)
    rows, cols = stdscr.getmaxyx()
    controlXPos = int((cols // 2 - len("DRIVING")))

    while True:
        k = stdscr.getch()
        stdscr.clear()
        display(stdscr)
        
        if int(k) in list(range(1 + 48, 10 + 48)):
            throttle = (float(k) - 48) * 255 / 9  # Adjust throttle based on key input
        
        if k == curses.KEY_LEFT:
            stdscr.addstr(7, controlXPos, "DRIVING LEFT")
            control(k, throttle)
        elif k == curses.KEY_RIGHT:
            stdscr.addstr(7, controlXPos, "DRIVING RIGHT")
            control(k, throttle)
        elif k == curses.KEY_UP:
            stdscr.addstr(7, controlXPos, "DRIVING FORWARD")
            control(k, throttle)
        elif k == curses.KEY_DOWN:
            stdscr.addstr(7, controlXPos, "DRIVING BACKWARD")
            control(k, throttle)
        elif k in [ord('w'), ord('s'), ord('a'), ord('d')]:
            control_servo(k)
        elif k == -1:
            stdscr.addstr(7, controlXPos, "COASTING")
            brakes()

        stdscr.addstr(8, controlXPos, "    ")
        stdscr.addstr(8, controlXPos, str(k))
        stdscr.addstr(9, controlXPos, "Throttle = " + str(int(throttle / 255 * 9)))
        stdscr.refresh()
        sleep(0.01)  # Reduced sleep time to decrease latency

    # Cleanup on exit
    brakes()
    pi.set_servo_pulsewidth(SERVO1, 0)  # Turn off servo signals
    pi.set_servo_pulsewidth(SERVO2, 0)
    pi.stop()

curses.wrapper(main)
