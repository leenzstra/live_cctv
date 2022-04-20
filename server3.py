import cv2
import socket
import pickle
import numpy as np
from imutils import build_montages


host = "localhost"
port = 5000
max_length = 65540

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

frame_info = None
buffer = None
frame = None
frameDict = {}

print("-> waiting for connection")

while True:
    data, address = sock.recvfrom(max_length)
    
    if len(data) < 100:
        frame_info = pickle.loads(data)

        if frame_info:
            nums_of_packs = frame_info["packs"]

            for i in range(nums_of_packs):
                data, address = sock.recvfrom(max_length)
                if i == 0:
                    buffer = data
                else:
                    buffer += data

            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape(frame.shape[0], 1)

            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.flip(frame, 1)
            frameDict[address] = frame
            (h, w) = frame.shape[:2]
            if frame is not None and type(frame) == np.ndarray:
                montages = build_montages(frameDict.values(), (w, h), (100, 100))
                # display the montage(s) on the screen
                for (i, montage) in enumerate(montages):
                    cv2.imshow("Home pet location monitor ({})".format(i),
                            montage)
            
            #if frame is not None and type(frame) == np.ndarray:
                #cv2.imshow("Stream", frame)
                #if cv2.waitKey(1) == 27:
                    #break
                
print("goodbye")