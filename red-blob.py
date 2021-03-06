#!/usr/bin/python
import math
import time
import cv2
import Queue
import sc_config
import pid
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
import balloon_config
from find_balloon import balloon_finder
from balloon_video import balloon_video


class GetPara(object):
	
	def __init__(self):
		self.simulator = sc_config.config.get_boolean('simulator','use_simulator',False)
		#get camera specs
		self.camera_index = sc_config.config.get_integer('camera','camera_index',0)
		#load config file
		sc_config.config.get_file('Smart_Camera')

		#get camera specs
		self.camera_width = sc_config.config.get_integer('camera', 'camera_width', 640)
		self.camera_height = sc_config.config.get_integer('camera', 'camera_height', 480)
		self.camera_hfov = sc_config.config.get_float('camera', 'horizontal-fov', 72.42)
		self.camera_vfov = sc_config.config.get_float('camera', 'vertical-fov', 43.3)
		#how many frames have been captured
		self.frame_count = 0

	def name(self):
		return "Precision_Land"

	def connect(self):
		while(veh_control.is_connected() == False):
			# connect to droneapi
			veh_control.connect(local_connect())
		self.vehicle = veh_control.get_vehicle()

	def run(self):
		sc_logger.text(sc_logger.GENERAL, 'running {0}'.format(self.name()))

		#start a video capture
		'''
		if(self.simulator):
			sc_logger.text(sc_logger.GENERAL, 'Using simulator')
			sim.set_target_location(veh_control.get_home())
			#sim.set_target_location(Location(0,0,0))

		else:'''

		sc_video.start_capture(self.camera_index)

		#camera = balloon_video.get_camera()
        	video_writer = balloon_video.open_video_writer()

		#create an image processor
		detector = CircleDetector()

		#create a queue for images
		imageQueue = Queue.Queue()

		#create a queue for vehicle info
		vehicleQueue = Queue.Queue()

	 	while veh_control.is_connected():

			#get info from autopilot
			location = veh_control.get_location()
			attitude = veh_control.get_attitude()

			print location
			print attitude


			# Take each frame
            		#_, frame = camera.read()
			#update how often we dispatch a command
		 	sc_dispatcher.calculate_dispatch_schedule()
			# grab an image
			capStart = current_milli_time()
			frame = sc_video.get_image()
			capStop = current_milli_time()
			#frame = sc_video.undisort_image(frame)
			#cv2.imshow('frame',frame)
			# write the frame
            		video_writer.write(frame)
			#update capture time
			sc_dispatcher.update_capture_time(capStop-capStart)

			#Process image
			#We schedule the process as opposed to waiting for an available core
			#This brings consistancy and prevents overwriting a dead process before
			#information has been grabbed from the Pipe
			if sc_dispatcher.is_ready():
				#queue the image for later use: displaying image, overlays, recording
				imageQueue.put(frame)
				#queue vehicle info for later use: position processing
				vehicleQueue.put((location,attitude))

				#the function must be run directly from the class

				#######
				sc_dispatcher.dispatch(target=balloon_finder.analyse_frame, args=(frame,))
	 			


			 #retreive results
			if sc_dispatcher.is_available():
			 	sc_logger.text(sc_logger.GENERAL, 'Frame {0}'.format(self.frame_count))
			 	self.frame_count += 1


			 	#results of image processor
			 	results = sc_dispatcher.retreive()
			 	# get image that was passed with the image processor
			 	img = imageQueue.get()
			 			#get vehicle position that was passed with the image processor
			 	location, attitude = vehicleQueue.get()
			
					
			 	#overlay gui
			 	#rend_Image = gui.add_target_highlights(img, results[3])


			 	#show/record images
			 	sc_logger.image(sc_logger.RAW, img)
			 	#sc_logger.image(sc_logger.GUI, rend_Image)
			
			 	#display/log data
			 	sc_logger.text(sc_logger.ALGORITHM,'found: {0} x: {1} y: {2} radius: {3}'.format(results[0],results[1],results[2],results[3]))
				#print Location(-35.363554, 149.165139,0)

				

# if starting from mavproxy
if __name__ == "__builtin__":
	# start precision landing
	strat = GetPara()

	# connect to droneapi
	sc_logger.text(sc_logger.GENERAL, 'Connecting to vehicle...')
	strat.connect()
	sc_logger.text(sc_logger.GENERAL, 'Vehicle connected!')

	# run strategy
	strat.run()
