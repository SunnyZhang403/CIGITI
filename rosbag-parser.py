import pandas as pd
import numpy as np
import tkinter as tk
import math
from matplotlib import pyplot as plt

def parseData(path): #This function is far from optimized and will be polished later, is functional at the moment

    #Read in data file (.txt format, see Sample Data.txt for reference)
    file = open(path, "r")
    data = file.read().split('\n')

    #Collect lines from txt file, remove unnecessary whitespaces
    lines = []
    for line in data:
        lines.append(line.strip(''))
    
    #Intialize Python array for data (temporary storage)
    dataarray = []
    for i in range(0,6):
        dataarray.append([])

    #Parse through blocks of 52 lines
    for i in range(len(lines)//52):
        #Time data, add cumulative seconds to current nanoseconds
        t = float(''.join(filter(str.isdigit,lines[52*i+3]))) + int(''.join(filter(str.isdigit, lines[52*i+4])))/(10**9)
        dataarray[0].append(t)

        #Set up arrays in other data values for current timestamp
        for l in range(1,6):
            dataarray[l].append([])

        #Append values in each data category (this is not optimized)
        for k in range(0,3):
            dataarray[1][i].append(float(lines[52*i+15+k].split(': ')[1]))
            dataarray[2][i].append(float(lines[52*i+20+k].split(': ')[1]))
            dataarray[4][i].append(float(lines[52*i+30+k].split(': ')[1]))
            dataarray[5][i].append(float(lines[52*i+34+k].split(': ')[1]))
        #Orientation requires 4 values in quaternerion format
        for j in range(0,4):
            dataarray[3][i].append(float(lines[52*i+24+j].split(': ')[1]))

    #Set up Pandas DataFrames (will initialize with columns as rows initially, so need to take the transpose)
    df = pd.DataFrame(dataarray)
    finaldf = df.transpose()

    #Label columns and return DataFrame
    finaldf.columns = ['Time (s)', 'pInertia','Position (x, y, z)', 'Orientation (x, y, z, w)', 'Linear Twist', 'Angular Twist']
    return finaldf


def processData(dataset):
    timestamp = []
    xpos = []
    ypos = []
    zpos = []
    pitch = []
    roll = []
    yaw = []
    npd = pd.DataFrame.to_numpy(dataset)
    for row in npd:
        timestamp.append(row[0] - npd[0][0])
        xpos.append(row[2][0])
        ypos.append(row[2][1])
        zpos.append(row[2][2])
        # print(row[1])
        yaw.append(math.atan2(2*(row[3][3]*row[3][0]+row[3][1]*row[3][2]),1-2*(row[3][0]**2+row[3][1]**2)))
        pitch.append(-math.pi/2 + math.atan2(math.sqrt(1+2*(row[3][3]*row[3][1]-row[3][0]*row[3][2])),math.sqrt(1-2*(row[3][3]*row[3][1]-row[3][0]*row[3][2]))))
        roll.append(math.atan2(2*(row[3][3]*row[3][2]+row[3][1]*row[3][0]),1-2*(row[3][2]**2+row[3][1]**2)))
    fdata = [timestamp, xpos, ypos, zpos, pitch, yaw, roll]
    df1 = pd.DataFrame(fdata)
    df2 = pd.DataFrame.transpose(df1)
    df2.columns = ["Time (s)", "X position", "Y position", "Z position", "Pitch", "Yaw", "Roll"]
    return df2
        
def plotData(dataset):
    plt.plot(processeddata["Time (s)"], processeddata["X position"], label = "X position")
    plt.plot(processeddata["Time (s)"], processeddata["Y position"], label = "Y position")
    plt.plot(processeddata["Time (s)"], processeddata["Z position"], label = "Z position")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title("X, Y, and Z Position")
    plt.show()

    
    plt.plot(processeddata["Time (s)"], processeddata["Pitch"], label = "Pitch")
    plt.plot(processeddata["Time (s)"], processeddata["Yaw"], label = "Yaw")
    plt.plot(processeddata["Time (s)"], processeddata["Roll"], label = "Roll")
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Angle")
    plt.title("Pitch Yaw and Roll Over Time")
    plt.show()

if __name__ == "__main__":
    data = parseData("Sample Data.txt")
    processeddata = processData(data)
    plotData(processeddata)
