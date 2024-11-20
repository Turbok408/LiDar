import os
import math
import matplotlib.pyplot as plt

def converCoordinates(detectorCoords,points):
    cartCoords = [[],[]]
    for i in range(16):
        cartCoords[1].append(math.cos(-0.418879 + 0.0523599*i)*float(points[i])+detectorCoords[1])
        cartCoords[0].append(math.sin(-0.418879 + 0.0523599 * i) * float(points[i])+detectorCoords[0])
    return cartCoords

def makeGraphs(dirname,setName):
    measurements = {}
    ##asssume seperation is always 180
    leddar1pos = (-40 + 420, 0)
    leddar2pos = (140 + 420, 0)
    for file in os.listdir(dirname):
        if file.endswith(".lvm"):
            name = ["_".join(file.split("_")[:2]), file.split("_")[2:][0][:-4]]
            f = open(dirname + "\\" + file, "r")
            if name[1] == "leddar1":
                detecorCoords = leddar1pos
            elif name[1] == "leddar2":
                detecorCoords = leddar2pos
            points = converCoordinates(detecorCoords, f.read().split()[::2])
            if name[0] not in measurements.keys():
                measurements.update({name[0]: {name[1]: points}})
            else:
                measurements[name[0]].update({name[1]: points})
            f.close()
    fig, axs = plt.subplots(2, round(len(measurements.keys()) / 2), figsize=(10, 10), tight_layout=True)
    for i in range(len(measurements.keys())):
        for key in measurements[list(measurements.keys())[i]]:
            axs.flat[i].plot(measurements[list(measurements.keys())[i]][key][0],
                             measurements[list(measurements.keys())[i]][key][1], marker="o", linestyle="--", label=key)
        axs.flat[i].set_title(list(measurements.keys())[i])
        axs.flat[i].set_xlabel("x")
        axs.flat[i].set_ylabel("y")
        axs.flat[i].set_ylim(bottom=0)
        axs.flat[i].set_xlim(left=-10)
        axs.flat[i].legend(loc="lower right")
    plt.savefig(setName+".png")
    plt.show()

dataSets = os.listdir(os.path.dirname(os.path.realpath(__file__))+"\\data")
for i in dataSets:
    makeGraphs(os.path.dirname(os.path.realpath(__file__))+"\\data\\"+i,i)


