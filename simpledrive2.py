import curses
import pigpio
import sys
from time import sleep

def display(stdscr):
    stdscr.addstr(0, 0, "SIMPLE DRIVE 2")
    rows, cols = stdscr.getmaxyx()
    screenDetailText = "This screen is [" + str(rows) + "] high and [" + str(cols) + "] across."
    startingXPos = int ( (cols - len(screenDetailText))/2 )
    stdscr.addstr(3, startingXPos, screenDetailText)
    stdscr.addstr(4, startingXPos, "use arrow keys to drive")
    stdscr.addstr(5, curses.COLS - len("Press a key to quit."), "Press a key to quit.")

pi = pigpio.pi()

pi.set_PWM_dutycycle(17,64)
pi.set_PWM_dutycycle(22,64)
sleep(0.5)
pi.set_PWM_dutycycle(17,0)
pi.set_PWM_dutycycle(22,0)
pi.set_PWM_dutycycle(23,0)
pi.set_PWM_dutycycle(27,0)


def control(key, throttle):
    if key == curses.KEY_RIGHT:
        pi.set_PWM_dutycycle(17,throttle) #RFWD
        #pi.set_PWM_dutycycle(27,throttle/4.) #LBWD
    elif key == curses.KEY_LEFT:
        #pi.set_PWM_dutycycle(23,throttle/4.4) #RBWD
        pi.set_PWM_dutycycle(22, throttle) #LFWD
    elif key == curses.KEY_UP:
        pi.set_PWM_dutycycle(17,throttle)
        pi.set_PWM_dutycycle(22, throttle)
    elif key == curses.KEY_DOWN:
        pi.set_PWM_dutycycle(23,throttle)
        pi.set_PWM_dutycycle(27,throttle)
def brakes():
    pi.set_PWM_dutycycle(17,0)
    pi.set_PWM_dutycycle(22,0)
    pi.set_PWM_dutycycle(23,0)
    pi.set_PWM_dutycycle(27,0)

def main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    throttle = 190; #0=stopped, 255= hauling ass
    rows, cols = stdscr.getmaxyx()
    controlXPos = int( (cols//2 - len("DRIVING")))
    while(True):
        k = stdscr.getch()
        stdscr.clear()
        display(stdscr)
        if int(k) in list(range(1+48,10+48)):
            throttle = (float(k)-48) * 255/9
        if k==curses.KEY_LEFT: 
            stdscr.addstr(7, controlXPos,"DRIVING LEFT")
            control(k,throttle)
        elif k==curses.KEY_RIGHT:
            stdscr.addstr(7, controlXPos, "DRIVING RIGHT")
            control(k,throttle)
        elif k==curses.KEY_UP:
            stdscr.addstr(7, controlXPos, "DRIVING FORWARD")
            control(k,throttle)

        elif k==curses.KEY_DOWN:
            stdscr.addstr(7, controlXPos, "DRIVING BACKWARD")
            control(k,throttle)
        elif k==-1:
            stdscr.addstr(7, controlXPos, "COASTING        ")
            brakes()
        stdscr.addstr(8,controlXPos, "    ")
        stdscr.addstr(8,controlXPos, str(k))
        stdscr.addstr(9,controlXPos,"Throttle = "+str(int(throttle/255*9)))
        stdscr.refresh()
        sleep(0.1)
    


curses.wrapper(main)
