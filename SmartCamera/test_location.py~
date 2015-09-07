"""
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

The example demonstrates how to arm and takeoff in Copter and how to navigate to 
points using Vehicle.commands.goto.

Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

import time
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil

api = local_connect()
vehicle = api.get_vehicles()[0]

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't let the user try to fly autopilot is booting
    if vehicle.mode.name == "INITIALISING":
        print "Waiting for vehicle to initialise"
        time.sleep(1)
    while vehicle.gps_0.fix_type < 2:
        print "Waiting for GPS...:", vehicle.gps_0.fix_type
        time.sleep(1)
		
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True
    vehicle.flush()

    while not vehicle.armed and not api.exit:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.commands.takeoff(aTargetAltitude) # Take off to target altitude
    vehicle.flush()

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.commands.takeoff will execute immediately).
    while not api.exit:
        print " Altitude: ", vehicle.location.alt
        if vehicle.location.alt>=aTargetAltitude*0.95: #Just below target, in case of undershoot.
            print "Reached target altitude"
            break;
        time.sleep(1)

arm_and_takeoff(3)

'''
location:
1.-35.363554 149.165139
2.-35.362664 149.165693
3. -35.363562 149.166230 
4.-35.362664 149.166803
5.-35.363562 149.167339
6. -35.362618 149.167875
7-35.363531 149.168440 

'''

print "Going to first point..."
#point1 = Location(-35.363554, 149.165139, 3, is_relative=True)
point1 = Location(30.264233, 120.118813, 3, is_relative=True)
vehicle.commands.goto(point1)
vehicle.flush()

# sleep so we can see the change in map
time.sleep(20)
'''
print "Going to second point..."
point2 = Location(-35.362664, 149.165693, 20, is_relative=True)
vehicle.commands.goto(point2)
vehicle.flush()

# sleep so we can see the change in map
time.sleep(20)


print "Going to second point..."
point2 = Location(-35.363562, 149.166230, 20, is_relative=True)
vehicle.commands.goto(point2)
vehicle.flush()

# sleep so we can see the change in map
time.sleep(20)


print "Going to second point..."
point2 = Location(-35.362664, 149.166803, 20, is_relative=True)
vehicle.commands.goto(point2)
vehicle.flush()

# sleep so we can see the change in map
time.sleep(20)


print "Going to second point..."
point2 = Location(-35.363562, 149.167339, 20, is_relative=True)
vehicle.commands.goto(point2)
vehicle.flush()

# sleep so we can see the change in map
time.sleep(20)

print "Going to second point..."
point2 = Location(-35.362618, 149.167875, 20, is_relative=True)
vehicle.commands.goto(point2)
vehicle.flush()

# sleep so we can see the change in map
time.sleep(20)

print "Going to second point..."
point2 = Location(-35.363531,149.168440, 20, is_relative=True)
vehicle.commands.goto(point2)
vehicle.flush()

# sleep so we can see the change in map
time.sleep(20)
'''
print "Returning to Launch"
vehicle.mode    = VehicleMode("RTL")
vehicle.flush()


