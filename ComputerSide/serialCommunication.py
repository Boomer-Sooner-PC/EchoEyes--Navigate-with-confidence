import serial
import binascii
from calcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math
import queue


TOLERANCE = 2
POINTS = 2

# function like the map() function in arduino
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

ser = serial.Serial(port='COM8',
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

tmpString = ""
loopFlag = True
flag2c = False
i = 0

points = [(i - TOLERANCE / 2, i + TOLERANCE / 2) for i in range(0, 360, int(360 / POINTS))]
# points = [(i[0] if i[0] >= 0 else 360 + i[0], i[1] if i[1] <= 360 else i[1] - 360) for i in points]

print(points)
m = 100


dist_queue = queue.Queue()

while True:
    b = ser.read()
    tmpInt = int.from_bytes(b, 'big')
    
    if (tmpInt == 0x54):
        tmpString +=  b.hex()+" "
        flag2c = True
        continue
    
    elif(tmpInt == 0x2c and flag2c):
        tmpString += b.hex()

        if(not len(tmpString[0:-5].replace(' ','')) == 90 ):
            tmpString = ""
            loopFlag = False
            flag2c = False
            continue

        lidarData = CalcLidarData(tmpString[0:-5])

        angles = [map(i, 0, 6.283185307179586, 0, 360) for i in lidarData.Angle_i]

        # if max(angles) > m: m = max(angles)
        # print(m)

        for i, angle in enumerate(angles):
            if lidarData.Confidence_i[i] > 0:
                for j, point in enumerate(points):
                    # check if angle is between the points
                    if point[0] <= angle <= point[1]:
                        print(f'Angle: {angle} | Point: {points.index(point)} | Distance: {lidarData.Distance_i[i]}')
                    

        tmpString = ""
        loopFlag = False
    else:
        tmpString += b.hex()+" "
    
    flag2c = False


ser.close()