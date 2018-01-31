import math
import csv
import random


class Gebruiker:
    def __init__(self, x, y):
        self.xcord = x
        self.ycord = y

class Location:
    def __init__(self, name, x, y):
        self.name = name
        self.xcord = x
        self.ycord = y

def get_distance():
    '''Get shortest distance from user to location, and show location'''
    with open('gebruiker.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for i in reader: #Read csv to user object
            gebruiker = Gebruiker(int(i[0]), int(i[1]))#Make user object

        with open('locations.csv', 'r') as f: #Read locations.csv
            reader = csv.reader(f, delimiter=';')
            lst = [] #Make list of all distances
            locations = [] #Make two dimensional list of locations
            for j in reader:
                location = Location(j[0], int(j[1]), int(j[2])) #Make location objects
                x = math.sqrt((location.xcord - gebruiker.xcord) ** 2 + (location.ycord - gebruiker.ycord) ** 2)#Stelling van pythagoras
                lst.append(x) #Add distances to list
                locations.append(j)#Add location to list

            #Get the index of the shortest distance, that index is the same as the location name
            print('Nearest location: ', locations[lst.index(min(lst))][0], 'with distance: ', min(lst))


if __name__ == '__main__':
    get_distance()

