import os
import math
import re
import matplotlib.pyplot as plt

def converCoordinates(detectorCoords,points,deg_offset):
    cartCoords = [[],[]]
    for i in range(16):
        cartCoords[1].append(math.cos(-0.418879 + 0.0523599*i+deg_offset)*float(points[i])+detectorCoords[1])
        cartCoords[0].append(math.sin(-0.418879 + 0.0523599 * i+deg_offset) * float(points[i])+detectorCoords[0])
    return cartCoords

def makeGraphs(dirname,set_name):
    measurements = {}
    if re.findall(r'(\d+)deg',dirname) == []:
        offset = [0,0]
    else:
        #assumes titlted into each other
        offset = [int(re.findall(r'(\d+)deg',dirname)[0])*math.pi/180,-int(re.findall(r'(\d+)deg',dirname)[0])*math.pi/180]
    if "90sep" in dirname:
        leddar1pos = (0, 0)
        leddar2pos = (90, 0)
    else:
        leddar1pos = (-40 + 420, 0)
        leddar2pos = (140 + 420, 0)
    for file in os.listdir(dirname):
        if file.endswith(".lvm"):
            name = ["_".join(file.split("_")[:2]), file.split("_")[2:][0][:-4]]
            f = open(dirname + "\\" + file, "r")
            if name[1] == "leddar1":
                detecor_coords = leddar1pos
                detecor_offset = offset[0]
            elif name[1] == "leddar2":
                detecor_coords = leddar2pos
                detecor_offset = offset[1 ]
            points = converCoordinates(detecor_coords, f.read().split()[::2],detecor_offset)
            if name[0] not in measurements.keys():
                measurements.update({name[0]: {name[1]: points}})
            else:
                measurements[name[0]].update({name[1]: points})
            f.close()
    print(dirname)
    measurements = list(measurements.items())
    fig, axs = plt.subplots(8, 8, figsize=(60, 80), tight_layout=True)
    measurements = sorted(measurements, key = lambda x: (-int(re.findall(r'Y(\d+)',x[0])[0]), int(re.findall(r'X(\d+)',x[0])[0])))
    fig.suptitle(set_name)
    for i in range(len(measurements)):
        for key in measurements[i][1]:
            axs.flat[i].plot(measurements[i][1][key][0],
                             measurements[i][1][key][1], marker="o", linestyle="--", label=key)
        axs.flat[i].set_title(measurements[i][0])
        axs.flat[i].set_xlabel("x")
        axs.flat[i].set_ylabel("y")
        axs.flat[i].set_ylim(bottom=0)
        axs.flat[i].set_xlim(left=-10)
        axs.flat[i].legend(loc="lower right")
    plt.savefig(set_name+".png")
    plt.show()
    plt.close(fig)


dataSets = os.listdir(os.path.dirname(os.path.realpath(__file__))+"\\data")
for i in dataSets:
    makeGraphs(os.path.dirname(os.path.realpath(__file__))+"\\data\\"+i,i)


