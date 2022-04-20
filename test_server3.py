from math import *
from operator import imul
import pyautogui
import cv2
import socket
import pickle
import numpy as np
from imutils import build_montages
import imutils
import os
import datetime
import apscheduler as sch
import load

def send_video():
    out.release()
    date = datetime.strftime(datetime.now()-datetime.timedelta(minutes=5), "%d.%m.%Y-%H.%M.%S")
    load.load_file('./videos/output.avi', 'output{}.avi'.format(date))
    out = cv2.VideoWriter(os.path.join('videos', 'output.avi'), fourcc, 30.0, resolution)

host = "192.168.1.3"
port = 5000
max_length = 65540

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

scheduler = sch.BackgroundScheduler()
job = scheduler.add_job(send_video, 'interval', minutes=5)

frame_info = None
buffer = None
frame = None
frameDict = {}

resolution = (1920, 1080)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(os.path.join('videos', 'output.avi'), fourcc, 30.0, resolution)


print("-> waiting for connection")


while True:
    data, address = sock.recvfrom(max_length)

    addr_str = str(address[0])

    try:
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
                

                
                if frame is not None and type(frame) == np.ndarray:
                    (h, w) = frame.shape[:2]
                    frameDict[addr_str] = frame
                    # print(frameDict)
                    mWH = floor(log2(len(frameDict.keys()))+1.0)
                    newW = w // mWH
                    newH = h // mWH
                    montages = build_montages(
                        frameDict.values(), (newW, newH), (mWH, mWH))
                    output = np.array(montages[0])
                    
                    # output = imutils.resize(output, width=resolution[0], height=resolution[1])
                    output = cv2.resize(output, resolution)

                    # for (i, montage) in enumerate(montages):
                    #     cv2.imshow("Stream ({})".format(i), montage)
                    
                    cv2.imshow("Stream", output)
                    
                    out.write(output)

                    key = cv2.waitKey(1) & 0xFF
            
            #out.release()
    except Exception as e:
        print(e)