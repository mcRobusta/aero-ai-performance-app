import os
import json

def clean_array(inputArray, delete=True):
    cleanArray = []
    for counter in range(len(inputArray)):
        if len(inputArray[counter]) > 0:
            cleanArray.append(inputArray[counter])
    del cleanArray[-1]
    return cleanArray

def seperate_v_values(v_array):
    v_1 = []
    v_r = []
    v_2 = []
    for item in v_array:
        v_values = item.split('/')
        v_1.append(v_values[0])
        v_r.append(v_values[1])
        v_2.append(v_values[2])
    return v_1, v_r, v_2

def extract_takeoff_weights(array):
    takeOffWeightArray = []
    for counter in range(1, len(array)):
        if "/" not in array[counter]:
            splitArray = array[counter].split(' ')
            if len(splitArray) > 1:
                takeOffWeightArray.append(splitArray[0])
            else:
                takeOffWeightArray.append(array[counter])
    return takeOffWeightArray

def strip_extra_v_values(array):
    for counter in range(len(array)):
        splitArray = array[counter].split(' ')
        if len(splitArray) > 1:
            if splitArray[1] == '':
                array[counter] = splitArray[0]
            else:
                array[counter] = splitArray[1]
    return array
        
datafile = open(os.getcwd() + "/data-extraction/datafile.json", "w")

pressureAltitudeArray = [0, 1000, 2000]
fileString = os.getcwd() + "/data-extraction/data-"

for fileCounter in range(9):
    file = open(fileString + str(fileCounter + 1) + ".txt", "r")
    fileArray = file.readlines()

    runwayLengths = clean_array(fileArray[1].split('\t'), delete=False)

    for iterator in range(1, (len(fileArray)-1) // 2):
        input_values = fileArray[2*iterator].replace('*', '')
        input_values = input_values.replace('\t', ' ')
        input_values = clean_array(input_values.split(' '))
        # Each line of input_values is structured like so:
        # [ Temperature,  TakeoffWeight, Codes, TakeoffWeight, Codes, etc. ]
        #print(input_values)
        v_values = fileArray[2*iterator+1].replace('*', '')
        v_values = clean_array(v_values.split('\t'))
        temp = input_values[0]
        v_1, v_r, v_2 = seperate_v_values(v_values)
        # Some values in the table with v values
        # have a '1 ' placed in front of them.
        # The following loop removes the '1 '
        # fron the v_1 array if present.
        v_1 = strip_extra_v_values(v_1)
        v_r = strip_extra_v_values(v_r)
        v_2 = strip_extra_v_values(v_2)
        takeoff_weights = extract_takeoff_weights(input_values)
        # Aero AI's file output is structured like so:
        # [ Pressure Altitude, Temperature, Max Takeoff Weight, Runway Length, V1, Vr, V2 ]
        for x in range(5):
            outputLine = {
                'pressureAltitude': float(pressureAltitudeArray[fileCounter % 3]), 
                'temperature': float(temp),
                'maxToW': float(takeoff_weights[x]),
                'runwayLengths': float(runwayLengths[x]),
                'v_1': float(v_1[x]),
                'v_r': float(v_r[x]),
                'v_2': float(v_2[x])
            }
            datafile.write(str(outputLine))

datafile.close()