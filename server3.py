from datetime import datetime
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
lastActive = {}
lastActiveCheck = datetime.now()

ESTIMATED_NUM_PIS = 1
ACTIVE_CHECK_PERIOD = 1

ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

print("-> waiting for connection")

while True:
    data, address = sock.recvfrom(max_length)

    if address not in lastActive.keys():
        print("[INFO] receiving data from {}...".format(address))

    lastActive[address] = datetime.now()
    
    if len(data) < 100:
        frame_info = pickle.loads(data)

        if frame_info:
            nums_of_packs = frame_info["packs"]
            time = frame_info["date"]

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
            if frame is not None and type(frame) == np.ndarray:
                (h, w) = frame.shape[:2]
                cv2.putText(frame, str(time), (10, h - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                montages = build_montages(frameDict.values(), (w, h), (100, 100))
                # display the montage(s) on the screen
                for (i, montage) in enumerate(montages):
                    cv2.imshow("Home pet location monitor ({})".format(i),
                            montage)
    if (datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
        # loop over all previously active devices
        for (address, ts) in list(lastActive.items()):
            # remove the RPi from the last active and frame
            # dictionaries if the device hasn't been active recently
            if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
                print("[INFO] lost connection to {}".format(address))
                lastActive.pop(address)
                frameDict.pop(address)
            # set the last active check time as current time
        lastActiveCheck = datetime.now()
    if (len(lastActive.items()) == 0):
        cv2.destroyAllWindows()