
from datetime import datetime

import signal # for handling the sigint sent by crtl+c
import sys # for killing the program
import os # for checking whether the directory exists or not

from picamera import PiCamera
import time

def signal_handler(signal, frame):
    #camera.capture(output_name) would simply overwrite the last pic
    print("Received signal", signal)
    camera.stop_preview() # kill the preview
    sys.exit(0) # exit with no errors

# pass in the hour and minute the sun rises
# returns the number of seconds we have to wait
def wait_for_sun(r_hour, r_minute):
    c_hour = int( str(datetime.now().time())[0:2] )
    c_minute = int( str(datetime.now().time())[3:5] )
    
    wait = 0
    # handle the hours; remember military hours
    if c_hour >= 12: # if we are setting this in the evening (think before midnight)...
        wait += 3600*(24 - c_hour)
        wait += 3600 * r_hour
    elif c_hour < 12: # elif we are setting this in the AM hours (think after midnight)
        wait += 3600*(r_hour - c_hour)

    # handle the minutes
    if r_minute > c_minute:
        wait += 60*(r_minute - c_minute)
    elif r_minute < c_minute:
        wait -= 3600 # borrow an hour
        wait += 60*(60 - (c_minute - r_minute)) # add the remainder to wait
    # if they are equal, ignore

    return wait
        

# pass in the hour and minute the sun sets
# returns the number of shots we want to take 
def get_num_shots(s_hour, s_minute, shot_rate):
    # get current time info
    c_hour = int( str(datetime.now().time())[0:2] )
    c_minute = int( str(datetime.now().time())[3:5] )

    # then we calculate the total number of pictures we need to take!
    # need to make sure there is actually time to take pictures
    shots = 0 # must instantiate outside of if-statement
    if s_hour < c_hour: # if the set hour has already passed
        print("The sunset has already passed")
        sys.exit(0) # we don't take any pictures
    elif s_hour > c_hour:
        shots = 3600*(s_hour - c_hour)
        if s_minute > c_minute:
            shots += 60*(s_minute - c_minute)
        elif s_minute < c_minute:
            shots -= 3600 # take away an hour of shots for the borrow
            shots += 60*(60 - (c_minute - s_minute)) # add the remainder
        # if the difference between the minutes is 0, no worry
    # else if the hours are equal...
    elif s_minute > c_minute: # and the sun hasn't yet set...
        shots += 60*(s_minute - c_minute)

    shots /= shot_rate # ttl num seconds / seconds per shot = num shots
    return shots



signal.signal(signal.SIGINT, signal_handler) # register SIGINT

# set up camera object; up top b/c camera obj must
# exist in case we exit during the wait for sunset
camera = PiCamera() # create a PiCamera obj
camera.resolution = (3280, 2464) # full res of camera
#camera.exposure_mode = "backlight"
camera.exposure_compensation = 10


# SET UP STUFF START =============================================
directory = "pics/15_day_17.04.28/"
if not os.path.isdir(directory): # check if directory exists;
        # up top b/c we want to check before waiting overnight!
    print("Directory", directory, "does not exist. Exitting now.")
    sys.exit(0)
else:
    print("Directory", directory, "found.")

# user inputs when the sun is supposed to rise
r_hour = 6
r_min = 42 # half an hour earlier
# user inputs when the sun is supposed to set
s_hour = 20
s_min = 37 # half an hour later

# wait for the sunrise if we need to, otherwise comment out
#'''
wait_time = wait_for_sun(r_hour, r_min)
print("Seconds until sunrise:", wait_time)
time.sleep(wait_time)
#'''
# SET UP STUFF END ===============================================


# setup timelapse
camera.start_preview(alpha=200) # create a semi-transparent preview to watch
time.sleep(2) # give a small amount of time for camera to adjust exposure
shot_rate = 60 # x seconds per frame
num_shots = get_num_shots(s_hour, s_min, shot_rate)
print("number of pictures to take:", num_shots)

# start taking pictures
time_prev = time.time()
counter = 1 # start the counter at 1
while( counter <= num_shots ): # in case we fail to exit manually...
    output_name = directory + str(datetime.now().time())[0:2] + 'h' + str(datetime.now().time())[3:5] + 'm_' +  str(counter) + ".jpg"
    camera.capture(output_name) # take a picture
    print(output_name)
    counter += 1
    # the timer ensures that we don't include the code execution time with the wait time, so pictures ARE taken every minute
    while time.time() - time_prev < shot_rate: # while less seconds have passed than the seconds between each picture
        time.sleep(5) # the maximum amount of time by which the shots can
                      # deviate from when they are supposed to be taken
    time_prev += shot_rate # increment previous time by exactly the shot rate

print("The sun has set. We are finished taking pictures today!")
camera.stop_preview()
