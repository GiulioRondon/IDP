# De signaalsterkte die de bakens uitzenden is 312,5 units
# De formule voor het berekenen van de afstand is: math.sqrt((Sb/S)) waarbij Sb= signaalsterkte bron en S= signaalsterkte

import math

def calDistGrid(xCor, yCor, xCorS, yCorS):
    """Function to calculate the distance between two grid coordinates where; xCor and yCor are the coordinates
    for the first point and xCorS and yCorS are the coordinates for the second grid point"""
    if xCor > xCorS:
        distX = xCor - xCorS
    else: distX = xCorS - xCor
    if yCor > yCorS:
        distY = yCor - yCorS
    else: distY = yCorS - yCor
    distGrid = math.sqrt(distX**2 + distY**2)
    return distGrid*2

def calDistSignal(Sb, S):
    """Function to calculate the distance between a signal receiver and the signal broadcaster where;
    S is the signalstrength as received and Sb is the original singalstrength"""
    distance = math.sqrt((Sb/S))
    print("Distance is "+ str(distance))
    return distance

def calposition(Sa, Sb, Sc, corDis):
    """function to calculate the position using the signalstrength from all three beacons where;
    Sletter is the signalstrength and corDis is a list with coordinates
    in the format [xCor, yCor, distA, distB, distC]"""
    distanceToA = calDistSignal(312.5, Sa)
    distanceToB = calDistSignal(312.5, Sb)
    distanceToC = calDistSignal(312.5, Sc)
    stepp = 0
    highestDifference = 10000000000
    location = []
    for cor in corDis:
        differenceA = cor[2] - distanceToA
        differenceB = cor[3] - distanceToB
        differenceC = cor[4] - distanceToC
        totalDiffernce = max((differenceA + differenceB + differenceC), -(differenceA + differenceB + differenceC))
        if highestDifference > totalDiffernce:
            print("update")
            print(highestDifference)
            print(totalDiffernce)
            highestDifference = totalDiffernce
            location = cor
            print(cor)
            print("<<<<<>>>>>")
        stepp += 1
    return location

beaconCor = [[1, 1], [5, 1], [3, 5]] # list with beacon coordinates in format A(x, y), B(x,y), C(x,y)
gridCor = [] # list to be filled with grid coordinates and distances in the format [xCor, yCor, distA, distB, distC]
for x in range(1, 6):
    for y in range(1, 6):
        coordinate = [x, y]
        step = 0
        for beacon in beaconCor:
            dist = calDistGrid(x, y, beaconCor[step][0], beaconCor[step][1])
            coordinate.append(dist)
            step += 1
        gridCor.append(coordinate)

print(gridCor)

strengthA = input("What is the signalstrength for beacon Alpha? ")
#while not strengthA.isdigit():
#    strengthA = input("Give a number: What is the signalstrength for beacon Alpha? ")

strengthAFloat = eval(strengthA)
strengthB = input("What is the signalstrength for beacon Bravo? ")
#while not strengthB.isdigit():
#    strengthB = input("Give a number: What is the signalstrength for beacon Bravo? ")

strengthBFloat = eval(strengthB)
strengthC = input("What is the signalstrength for beacon Charlie? ")
#while not strengthC.isdigit():
#    strengthC = input("Give a number: What is the signalstrength for beacon Charlie? ")

strengthCFloat = eval(strengthC)

position = calposition(strengthAFloat, strengthBFloat, strengthCFloat, gridCor)
print(position)

print("Your position on the grid is {},{}.".format(position[0], position[1]))
