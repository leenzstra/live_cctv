# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import imagezmq
import argparse
import socket
import time
import logging
import cv2

import signal
import sys

def signal_handler(sig, frame):
    logging.info('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", default='127.0.0.1',
	help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())


sender = imagezmq.ImageSender(connect_to="udp://{}:5555".format(
	args["server_ip"]))

rpiName = socket.gethostname()
vs = VideoStream(src=0).start()
time.sleep(2.0)


while True:
	fps = FPS().start()
	frame = vs.read()
	
	sender.send_image(rpiName, frame)
	fps.update()
	fps.stop()
	print(fps.fps())
	

# while True:
	# frame = vs.read()
	# 
	# sender.send_image(rpiName, frame)

