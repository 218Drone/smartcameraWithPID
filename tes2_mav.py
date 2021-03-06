#!/usr/bin/python
import math
import time
import cv2
import Queue
import sc_config
from sc_video import sc_video
from sc_dispatcher import sc_dispatcher
from sc_logger import sc_logger
from pl_gui import PrecisionLandGUI as gui
from pl_sim import sim
from pl_util import shift_to_origin, current_milli_time
from CircleDetector import CircleDetector
from vehicle_control import veh_control
from droneapi.lib import VehicleMode, Location, Attitude
from position_vector import PositionVector

#api             = local_connect()
#vehicle         = api.get_vehicles()[0]
#descent_rate = sc_config.config.get_float('general','descent_rate', 0.5)

class takeland(object):

	def __init__(self):
		#when we have lock on target, only descend if within this radius
		self.descent_radius = sc_config.config.get_float('general', 'descent_radius', 1.0)
		#Descent velocity
		self.descent_rate = sc_config.config.get_float('general','descent_rate', 0.5)
	def name(self):
		return "Precision_Land"
	
	def connect(self):
		while(veh_control.is_connected() == False):
			# connect to droneapi
			veh_control.connect(local_connect())
		self.vehicle = veh_control.get_vehicle()

	#straight_descent - send the vehicle straight down
	def straight_descent(self):
		#veh_control.set_velocity(0,0,self.descent_rate)
		veh_control.set_velocity(0,0,self.descent_rate)
	def straight_raise(self):
		veh_control.set_velocity(0,0,1)
		time.sleep(10)
	def arm_and_takeoff(self):
	    """Dangerous: Arm and takeoff vehicle - use only in simulation"""
	    # NEVER DO THIS WITH A REAL VEHICLE - it is turning off all flight safety checks
	    # but fine for experimenting in the simulator.
	    #self.connect(self)
            print "Arming and taking off"
	    self.vehicle.mode    = VehicleMode("GUIDED")
	    self.vehicle.parameters["ARMING_CHECK"] = 0
	    self.vehicle.armed   = True
	    self.vehicle.flush()

	    while not self.vehicle.armed:
		    print "Waiting for arming..."
		    time.sleep(1)

	    print "Taking off!"
	    self.vehicle.commands.takeoff(2) # Take off to 20m height

	    # Pretend we have a RC transmitter connected
	    rc_channels = self.vehicle.channel_override
	    rc_channels[3] = 0 # throttle
	    self.vehicle.channel_override = rc_channels
	    #print veh_control.get_location().alt
	    self.vehicle.flush()
	    time.sleep(3)
	
	'''def land(self):
	    if alt>1:
		self.changemode("LAND")
	'''
	def changemode(self,str):
		self.vehicle.mode    = VehicleMode(str)
		self.vehicle.flush()
		

# if starting from mavproxy
if __name__ == "__builtin__":
	# start precision landing
	start = takeland()
	start.connect()
	# run strategy
	start.arm_and_takeoff()
	print veh_control.get_location().alt
	#while veh_control.get_location().alt<1:
	#    print veh_control.get_locaguition().alt
	     		
	#print veh_control.get_location().alt
	#while veh_control.get_location().alt>2:
	start.changemode("GUIDED")
	#while veh_control.get_location().alt<20:
	#	veh_control.set_velocity(0,0,-2);

	#start.changemode("LOITER")
	#start.straight_raise()
	#start.straight_descent()
	
	#time.sleep(5)
	#start.changemode("LAND")



