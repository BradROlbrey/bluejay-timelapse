
from datetime import datetime

import signal # for handling the sigint sent by crtl+c
import sys # for killing the program
import os # for checking whether the directory exists or not

import RPi.GPIO as GPIO
from picamera import PiCamera
import time

def signal_handler(signal, frame):
    print("Received signal", signal)
    camera.stop_preview() # kill the preview
    GPIO.output(32, GPIO.LOW) # turn off the IR LEDs
    GPIO.cleanup() # release the GPIO stuff
    sys.exit(0) # exit with no errors
        

# pass in the hour and minute the sun sets
# returns the number of seconds we have to wait
def wait_for_set(s_hour, s_minute):
    # get current time info
    c_hour = int( str(datetime.now().time())[0:2] )
    c_minute = int( str(datetime.now().time())[3:5] )

    # then we calculate the total number of pictures we need to take!
    # need to make sure there is actually time to take pictures
    wait = 0 # must instantiate outside of if-statement
    if s_hour < c_hour: # if the set hour has already passed
            # only works if midnight has not passed yet; safer to just comment out
        print("The sunset has passed. No need to wait")
        return wait # we don't wait, and immediately start taking pictures
    elif s_hour > c_hour:
        wait = 3600*(s_hour - c_hour)
        if s_minute > c_minute:
            wait += 60*(s_minute - c_minute)
        elif s_minute < c_minute:
            wait -= 3600 # take away an hour of wait for the borrow
            wait += 60*(60 - (c_minute - s_minute)) # add the remainder
        # if the difference between the minutes is 0, no worry
    # else if the hours are equal...
    elif s_minute > c_minute: # and the sun hasn't yet set...
        wait += 60*(s_minute - c_minute)

    return wait

# pass in the hour and minute the sun rises
# returns the number of shots we want to take
def get_num_shots(r_hour, r_minute, shot_rate):
    c_hour = int( str(datetime.now().time())[0:2] )
    c_minute = int( str(datetime.now().time())[3:5] )
    
    total = 0
    # handle the hours; remember, military hours
    if c_hour >= 12: # if we are starting this in the evening (think before midnight)...
        total += 3600*(24 - c_hour)
        total += 3600 * r_hour
    elif c_hour < 12: # elif we are starting this in the AM hours (think after midnight)
        total += 3600*(r_hour - c_hour)

    # handle the minutes
    if r_minute > c_minute:
        total += 60*(r_minute - c_minute)
    elif r_minute < c_minute:
        total -= 3600 # borrow an hour
        total += 60*(60 - (c_minute - r_minute)) # add the remainder to total
    # if they are equal, ignore

    total /= shot_rate # ttl num seconds / seconds per shot = num shots
    return total



signal.signal(signal.SIGINT, signal_handler) # register SIGINT

# set up GPIO stuff
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

# set up camera object; up top b/c camera obj must
# exist in case we exit during the wait for sunset
camera = PiCamera() # create a PiCamera obj
camera.resolution = (3280, 2464) # full res of camera
camera.color_effects = (128,128) # black & white
camera.exposure_compensation = 5


# USER INPUT START =============================================
directory = "pics/15_night_17.04.28/"
if not os.path.isdir(directory): # check if directory exists
        # up top b/c we want to check before waiting overnight!
    print("Directory", directory, "does not exist. Exitting now.")
    GPIO.cleanup()
    sys.exit(0)
else:
    print("Directory", directory, "found.")

# user inputs when the sun is supposed to rise
r_hour = 7
r_min = 11 # stop taking pictures half an hour later
# user inputs when the sun is supposed to set
s_hour = 19
s_min = 37 # start taking pictures half an hour earlier

# wait for the sunset if we need to, otherwise comment out
#'''
wait_time = wait_for_set(s_hour, s_min)
print("Seconds until sunset:", wait_time)
time.sleep(wait_time)
#'''
# USER INPUT END ===============================================


# setup timelapse
camera.start_preview(alpha=200) # create a semi-transparent preview to watch
#time.sleep(2) # give small amount of time for camera to adjust exposure (handled here)
shot_rate = 60 # x seconds per frame
num_shots = get_num_shots(r_hour, r_min, shot_rate)
print("number of pictures to take:", num_shots)

# start taking pictures
time_prev = time.time()
counter = 1 # start the counter at 1
while( counter <= num_shots ): # while we still have pictures to take
    output_name = directory + str(datetime.now().time())[0:2] + 'h' + str(datetime.now().time())[3:5] + 'm_' +  str(counter) + ".jpg"

    GPIO.output(32, GPIO.HIGH) # turn on the leds
    time.sleep(9) # wait for the camera to adjust
    camera.capture(output_name) # take a picture
    time.sleep(3) # hold up for a bit; might not affect shot, but we'll wait just to be safe!
    GPIO.output(32, GPIO.LOW) # turn off the leds

    print(output_name)
    counter += 1
    while time.time() - time_prev < shot_rate: # while less seconds have passed than the seconds between each picture
        time.sleep(4) # the maximum amount of time by which the shots can
                      # deviate from when they are supposed to be taken
    time_prev += shot_rate # increment previous time by exactly the shot rate

print("The sun has risen. We are finished taking pictures tonight!")
camera.stop_preview()
GPIO.cleanup() # release the GPIO stuff

