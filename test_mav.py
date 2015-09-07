import time
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil
from vehicle_control import veh_control

import sc_config
api             = local_connect()
vehicle         = api.get_vehicles()[0]
#descent_rate = sc_config.config.get_float('general','descent_rate', 0.5)
def arm_and_takeoff():
    """Dangerous: Arm and takeoff vehicle - use only in simulation"""
    # NEVER DO THIS WITH A REAL VEHICLE - it is turning off all flight safety checks
    # but fine for experimenting in the simulator.
    print "Arming and taking off"
    vehicle.mode    = VehicleMode("STABILIZE")
    vehicle.parameters["ARMING_CHECK"] = 0
    vehicle.armed   = True
    vehicle.flush()

    while not vehicle.armed and not api.exit:
        print "Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.commands.takeoff(20) # Take off to 20m height

    # Pretend we have a RC transmitter connected
    rc_channels = vehicle.channel_override
    rc_channels[3] = 1500 # throttle
    vehicle.channel_override = rc_channels

    vehicle.flush()
    time.sleep(10)

arm_and_takeoff()
vehicle.mode    = VehicleMode("LOITER")

#def autopilot_land():
		#descend velocity
#		veh_control.set_velocity(0,0,descent_rate)


msg = vehicle.message_factory.set_position_target_local_ned_encode(
                                                         0,       # time_boot_ms (not used)
                                                         0, 0,    # target system, target component
                                                         mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
                                                         0x01C7,  # type_mask (ignore pos | ignore acc)
                                                         0, 0, 0, # x, y, z positions (not used)
                                                         0, 0, 1, # x, y, z velocity in m/s
                                                         0, 0, 0, # x, y, z acceleration (not used)
                                                         0, 0)    # yaw, yaw_rate (not used)
            # send command to vehicle
vehicle.send_mavlink(msg)
vehicle.flush()




#autopilot_land()





