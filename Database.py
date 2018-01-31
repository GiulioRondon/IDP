import math
import csv
import random

def search_database(plek_input, user_coords):
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

                #print(locations)
                #Get the index of the shortest distance, that index is the same as the location name
                #print(locations[lst.index(min(lst))])
                #print('Nearest location: ', locations[lst.index(min(lst))][0], 'with distance: ', min(lst))

                opgeteld_list = []
                for list in locations:
                    if list[0] == plek_input:
                        opgeteld_list.append(int(list[1]) + int(list[2]))
                print(opgeteld_list)

                user_coords_opgeteld = int(user_coords[0]) + int(user_coords[1])
                print(user_coords_opgeteld)

                #print(opgeteld_list)
                #print(user_coords_opgeteld)

                takeClosest = lambda num,collection:min(collection,key=lambda x:abs(x-num))
                closest_index = opgeteld_list.index(takeClosest(user_coords_opgeteld,opgeteld_list))

                closest_list = []
                for place in locations:
                    if place[0] == plek_input:
                        closest_list = place
                #print(closest_list[1], closest_list[2])

                #print('the closest ' + str(plek_input) + ' is op ' + str(closest_list[1]) + str(closest_index[2]))
                #print(closest_list)
                return closest_list
    res = get_distance()
    #print(res)
    return res

def give_places():
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

        return locations

    res = get_distance()
    #print(res)
    return res

