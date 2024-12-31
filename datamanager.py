import itertools
import os
import math
import re

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def converCoordinates(detectorCoords,points,deg_offset):
    cartCoords = [[[],[]]]
    line_num = 0
    for i in range(len(points)):
        #to make mutiple line segments return list where data is split at 0 values and 0s are deleted
        #if r = 0 and previus line segment not empty skip to next segment
        if float(points[i]) == 0.0:
            if cartCoords[line_num] != [[], []]:
                cartCoords.append([[], []])
                line_num += 1
        else:
            cartCoords[line_num][1].append(math.cos(-0.418879 + 0.0523599*i+deg_offset)*float(points[i])+detectorCoords[1])
            cartCoords[line_num][0].append(math.sin(-0.418879 + 0.0523599 * i+deg_offset) * float(points[i])+detectorCoords[0])
    return cartCoords

def makeGraphs(dirname,set_name):
    colours = {"leddar1":"red","leddar2":"blue"}
    measurements = {} # this should really be list
    #get deg offsets and detector detectors from directory name
    if re.findall(r'(\d+)deg',dirname) == []:
        offset = [0,0]
    else:
        #assumes titlted into each other
        offset = [int(re.findall(r'(\d+)deg',dirname)[0])*math.pi/180,-int(re.findall(r'(\d+)deg',dirname)[0])*math.pi/180]
    if "90sep" in dirname:
        leddar1pos = (700, 0)
        leddar2pos = (790, 0)
    else:
        leddar1pos = (700, 0)
        leddar2pos = (880, 0)
    #for each file in directory get a data dir {graph_title :{detecor_name:data points[line_segment][0 for x,1 for y]}}
    personpointsdir ={}
    for file in os.listdir(dirname):
        if file.endswith(".lvm"):
            name = ["_".join(file.split("_")[:2]), file.split("_")[2:][0][:-4]]
            expected = (re.findall(r'X(\d+)',name[0])[0:][0],re.findall(r'Y(\d+)',name[0])[0:][0])
            f = open(dirname + "\\" + file, "r")
            if name[1] == "leddar1":
                detecor_coords = leddar1pos
                detecor_offset = offset[0]
            elif name[1] == "leddar2":
                detecor_coords = leddar2pos
                detecor_offset = offset[1]
            points = converCoordinates(detecor_coords, f.read().split()[::2],detecor_offset)
            f.seek(0)
            amplitudes = f.read().split()[1::2]
            person_points =[]
            for i in range(len(amplitudes)):
                f.seek(0)
                if float(amplitudes[i]) > 0.8*max([float(i) for i in amplitudes]) and float(amplitudes[i]) >500:
                    person_points.append(converCoordinates(detecor_coords,[f.read().split()[::2][i]],detecor_offset+i*0.0523599))
                    if float(expected[0]) - 200 < float(person_points[0][0][0][0]) < float(expected[0]) + 200 and float(expected[1]) - 200 < float(person_points[0][0][1][0]) < float(expected[1]) + 200:
                        if expected in personpointsdir:
                                personpointsdir[expected][0] = personpointsdir[expected][0]+person_points[0][0][0]
                                personpointsdir[expected][1] = personpointsdir[expected][1] + person_points[0][0][1]
                        else:
                            personpointsdir.update({expected:[person_points[0][0][0],person_points[0][0][1]]})
            if name[0] not in measurements.keys():
                measurements.update({name[0]: {name[1]: points}})
            else:
                measurements[name[0]].update({name[1]: points})
            f.close()
    errors = {}
    person_size = (44, 22)
    for key in personpointsdir.keys():
        errors.update({key:{"std":[np.std(personpointsdir[key][0]),np.std(personpointsdir[key][1])],"aerr":[np.abs(np.mean(personpointsdir[key][0])-float(key[0])),np.abs(np.mean(personpointsdir[key][1])-float(key[1]))]}})
    error_std=[[],[]]
    for key in errors:
        error_std[0].append(errors[key]["aerr"][0])
        error_std[1].append(errors[key]["aerr"][1])
    error_std=np.array(error_std)

    print("x std",np.std(error_std[0]),"y std",np.std( error_std[1]),"x err",np.mean(error_std[0]),"y err",np.mean(error_std[1]))
    print(dirname)
    """
    # PLOT ERRORS GRAPHS
    x=[]
    y=[]
    n=[]
    measurements=[]
    for key in errors:
        measurements.append([key[0],key[1],np.array([float(np.format_float_positional(errors[key]["aerr"][0],precision=2)),float(np.format_float_positional(errors[key]["aerr"][1], precision=2))])])
    measurements = sorted(measurements,key=lambda x: [int(x[0]), int(x[1])])
    for i in measurements:
        x.append(float(i[0]))
        y.append(float(i[1]))
        n.append(i[2])
    n = np.array(n)
    fig, ax = plt.subplots()
    colours = []
    maxn = 0
    for i in n:
        if i[0]+i[1]>maxn:
            maxn=i[0]+i[1]
    for i in range(len(n)):
        colours.append(((n[i][0]+n[i][1])/maxn,1-(n[i][0]+n[i][1])/maxn,0))
    ax.scatter(x, y,s=400,color=colours)
    fig.suptitle(set_name)
    for i, txt in enumerate(n):
        ax.annotate(str(txt[0]), (x[i], y[i]),ha='center',va='top')
        ax.annotate(str(txt[1]), (x[i], y[i]), ha='center', va='bottom')
    plt.show()
    plt.close(fig)
    """
        #PLOT NORMAL GRAPHS
    measurements = list(measurements.items())
    fig, axs = plt.subplots(8, 8, figsize=(60, 80), tight_layout=True)
    measurements = sorted(measurements, key = lambda x: (-int(re.findall(r'Y(\d+)',x[0])[0]), int(re.findall(r'X(\d+)',x[0])[0])))
    fig.suptitle(set_name)
    for i in range(len(measurements)):
        for key in measurements[i][1]:
            for j in measurements[i][1][key]:
                axs.flat[i].plot(j[0],j[1], marker="o", linestyle="--", color=colours[key])
        axs.flat[i].set_title(measurements[i][0])
        axs.flat[i].set_xlabel("x")
        axs.flat[i].set_ylabel("y")
        axs.flat[i].set_ylim(bottom=0)
        axs.flat[i].set_xlim(left=-10)
        axs.flat[i].legend(handles=[mpatches.Patch(color='red', label='Leddar1'),mpatches.Patch(color='blue', label='Leddar2')])
    plt.savefig(set_name+".png")
    plt.show()
    plt.close(fig)


dataSets = os.listdir(os.path.dirname(os.path.realpath(__file__))+"\\data")
for i in dataSets:
    makeGraphs(os.path.dirname(os.path.realpath(__file__))+"\\data\\"+i,i)


