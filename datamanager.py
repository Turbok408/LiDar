import os
import math
import matplotlib.pyplot as plt
import re

def converCoordinates(detectorCoords,points):
    cartCoords = [[],[]]
    for i in range(16):
        cartCoords[1].append(math.cos(-0.418879 + 0.0523599*i)*float(points[i])+detectorCoords[1])
        cartCoords[0].append(math.sin(-0.418879 + 0.0523599 * i) * float(points[i])+detectorCoords[0])
    return cartCoords

dirname = "C:\\Users\edwar\PycharmProjects\Lidar\.venv\data\lecturehall_08.11"
leddar1pos = (-40,0)
leddar2pos=(140,0)

measurements = {}
for file in os.listdir(dirname):
    if file.endswith(".lvm"):
        print(file)
        name = ["_".join( file.split("_")[:2]),  file.split("_")[2:][0][:-4]]
        f = open("C:\\Users\edwar\PycharmProjects\Lidar\.venv\data\lecturehall_08.11\\"+file,"r")
        if name[1] == "leddar1":
            detecorCoords = leddar1pos
        elif name[1] == "leddar2":
            detecorCoords = leddar2pos
        points = converCoordinates(detecorCoords, f.read().split()[::2])
        if name[0] not in measurements.keys():
            measurements.update( {name[0] : {name[1] : points}} )
        else:
            measurements[name[0]].update( {name[1] : points})
        f.close()
fig, axs = plt.subplots(2, round(len(measurements.keys())/2))
fig.tight_layout()
for i in range(len(measurements.keys())):
    for key in measurements[list(measurements.keys())[i]]:
        axs.flat[i].plot(measurements[list(measurements.keys())[i]][key][0],measurements[list(measurements.keys())[i]][key][1],marker="o",linestyle ="--")
    axs.flat[i].set_title(list(measurements.keys())[i])
    axs.flat[i].set_ylim(bottom=0)

plt.show()
