""" Simple script for the FLYING CAT AND MOUSE game tutorial

This will command the flying cat, using the pose sensor of the mouse, to follow
after the latter."""

import math
from pymorse import Morse
import time
# Use sockets through pymorse interface


""" The minimal distance to maintain between the mouse and the cat. """
minDist = 5.0

""" The height for the flying cat. """
# NB: this is the absolute height not the one relative to the ground...
# TODO: use sensors (laser?) to take into account the ground and the obstacle
height= 3.5 


def where_is(agentPose_stream):
    """ Read data from the [mouse|cat] pose sensor, and determine the position of the agent """
    pose = agentPose_stream.get()

    return pose


def frighten_mouse():
    """ Use the mouse pose sensor to locate and "chase" it """

    with Morse() as morse:
        rotorPose = morse.rotor.rotorPose
        waypoint = {    "x": 50, \
                        "y": 0, \
                        "z": 0.1, \
                        "yaw": 0, \
                        "tolerance": 0.1 \
                    }
        motiondata = {"v": 1, "w": 0}
        #motion = morse.rotor.waypoint
        #motion.publish(waypoint)
        #while True:
            # send the command through the socket
        motionvw = morse.rotor.motionvw
        morse.reset()
        motionvw.publish(motiondata)
        time.sleep(120)
        morse.quit()

def main():
    """ Main behaviour """
    frighten_mouse()

if __name__ == "__main__":
    main()
