import cv2
import socket
from datetime import datetime
import math
import pickle
import signal
import sys
import argparse

max_length = 65000


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", default='127.0.0.1',
                help="ip address of the server to which the client will connect")
ap.add_argument("-p", "--server-port", default=5000)
args = vars(ap.parse_args())

host = args['server_ip']
port = int(args['server_port'])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
rpiName = socket.gethostname()

while ret:
    # compress frame
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)
        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)
        
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        frame_info = {"packs":num_of_packs, "date":time}
        
        sock.sendto(pickle.dumps(frame_info), (host, port))

        left = 0
        right = max_length

        for i in range(num_of_packs):
            data = buffer[left:right]
            left = right
            right += max_length
            sock.sendto(data, (host, port))

    ret, frame = cap.read()

print("done")
