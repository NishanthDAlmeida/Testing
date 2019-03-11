import serial
import time
import sys
from jenkinsapi import jenkins


# Configuration
JENKINS_URL = 'http://localhost:8080/job/Myproject1/configure'
DEVICE_PATH = 'COM4'
BAUD_RATE = 9600

SUCCESS = 'g'
FAILURE = 'r'
BUILDING = 'y'
QUERY_FREQUENCY = 30 # Frequency to query jenkins, in seconds.


# The view name to filter by. If None, then check all jobs.
VIEW_NAME = None

# Connect to the Arduino board.
ser = serial.Serial(DEVICE_PATH, BAUD_RATE)

# Sleep to allow Arduino board to configure serial communication.
time.sleep(2)

j = jenkins.Jenkins(JENKINS_URL)
current_state = ''


def change_light(state):
    global current_state
    if state != current_state:
        ser.write(state)
        current_state = state


def check_jenkins():
    try:
        if VIEW_NAME:
            job_names = j.views[VIEW_NAME].keys()

        jobs = j.get_jobs()
        for (name, job) in jobs:
            if not job.is_enabled():
                continue
            if job_names:
                if name not in job_names:
                    continue
            if not job._data['lastBuild']:
                # If a job has never been built, skip it.
                continue
            last_build = job.get_last_build()
            if last_build and last_build.is_running():
                change_light(BUILDING)
                return
            elif not job.get_last_build().is_good():
                change_light(FAILURE)
                return
        change_light(SUCCESS)
    except:
        change_light(FAILURE)
        print "Unable to query jenkins:", sys.exc_info()[0]


if __name__ == "__main__":
    while(1):
        # Main application loop.
        check_jenkins()
        time.sleep(QUERY_FREQUENCY)
