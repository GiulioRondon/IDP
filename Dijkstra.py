#####################
# In deze file is het Dijkstra algoritme uitgewerkt, alle functies in deze file zijn:
#
# GenCor(minX, maxX, minY, maxY), deze wordt gebruikt om alle coordinaten te genereren.
# neighboursCal(vertex, xMax, yMax), deze functie berekend alle buren van een coordinaat.
# FindVertexFromCor(ListWithVertex, coordinate), Omdat er twee "soorten" coordinaten worden gebruikt in deze code,
#   namelijk coordinaten in de form [xCor, yCor] en vertexen; coordinaten met extra informatie die belangrijk zijn voor
#   het dijkstra algoritme, moest er een functie komen om de vertex te vinden bij een coordinaat.
# Dijkstra(grid, source, destination), het algoritme! Deze berekend de snelste route van "source" naar "destination".
#   De functie genereerd ook de benodigde vertexen.
#####################

import copy

# Eerst het maken van alle coordinaten, dit zijn er 960 in totaal, een resolutie van 40x24
gridCor = []                # De lijst waar alle coordinaten in worden gezet, in de form [[xCor, yCor], [xCor, yCor]]
startCoordinate = []        # De lijst waar de start coordinaten in worden gezet, in de form [xCor, yCor]
DestinationCoordinate = []  # De lijst waar de coordinaten van het doel in worden gezet, in de form [xCor, yCor]

def GenCor(minX, maxX, minY, maxY):
    maxX += 1
    maxY += 1
    lstCor = []
    for x in range(minX, maxX):              # Hier begint het genereren van alle coordinaten
        for y in range(minY, maxY):
            coordinate = [x, y]         # Een lijst met een coordinaat
            lstCor.append(coordinate)  # De coordinaat wordt toegevoegd aan gridCor
    return lstCor

gridCor = GenCor(1, 40, 1, 24)

print(gridCor[-1])

#Nu het generen van test obstakels
# obstaclesCor = []
# for x in range(10, 12):
#     for y in range(1, 14):
#         coordinateOb = [x, y]
#         obstaclesCor.append(coordinateOb)
# print("Obstacles = {} to {}".format(obstaclesCor[0], obstaclesCor[-1]))

# Daarna, omdat dit een test is, voert de gebruiker de start coordinaten in.
startCoordinateX = int(input("Give x coordinate: "))
startCoordinate.append(startCoordinateX)
startCoordinateY = int(input("Give y coordinate: "))
startCoordinate.append(startCoordinateY)

# Daarna, omdat dit een test is, voert de gebruiker de doel/eindbestemming coordinaten in.
DestinationCoordinateX = int(input("Give x coordinate: "))
DestinationCoordinate.append(DestinationCoordinateX)
DestinationCoordinateY = int(input("Give y coordinate: "))
DestinationCoordinate.append(DestinationCoordinateY)

# Hier wordt een functie aangemaakt om de coordinaten van alle "buren" te berekenen
# en alle negatieve coordinaten weghaalt
def neighboursCal(vertex, xMax, yMax):
    """Function to calculate all neighbours, this function needs optimization"""
    deleteList = []                                     # De lijst die gevult gaat worden met alle negatieve coordinaten
    neighboursList = []                             # De lijst die gevuld gaat worden met alle coordinaten van de buren
    neighboursList.append([vertex[0], vertex[1] - 1, 1])# In dit blok code worden alle coordinaten een voor een berekend
    neighboursList.append([vertex[0], vertex[1] + 1, 1])# dit heeft wat optimization nodig heeft.
    neighboursList.append([vertex[0] - 1, vertex[1], 1])
    neighboursList.append([vertex[0] + 1, vertex[1], 1])
    neighboursList.append([vertex[0] - 1, vertex[1] - 1, 1.4])
    neighboursList.append([vertex[0] - 1, vertex[1] + 1, 1.4])
    neighboursList.append([vertex[0] + 1, vertex[1] - 1, 1.4])
    neighboursList.append([vertex[0] + 1, vertex[1] + 1, 1.4])
    for neighbour in neighboursList:                # Hier worden alle negatieve coordinaten in de deleteList gedaan.
        if neighbour[0] <= 0 or neighbour[1] <= 0:
            deleteList.append(neighbour)
        if neighbour[0] > xMax or neighbour[1] > yMax:
            deleteList.append(neighbour)
    for deleteCor in deleteList: # Hier worden alle coordinaten die in de deleteList staan uit de neighboursList gehaald
        if deleteCor in neighboursList:
            neighboursList.remove(deleteCor)
        # else:
        #     print("{} wasn't deleted".format(deleteCor))
    return neighboursList

def FindVertexFromCor(ListWithVertex, coordinate):
    """Function to convert a coordinate to a vertex found in a grid"""
    for vertex in ListWithVertex:
        vertexCor = []
        vertexCor.append(vertex[0])
        vertexCor.append(vertex[1])
        if coordinate == vertexCor:
            return vertex
    print("{} not found in list".format(coordinate))

# Dit wordt de functie om de kortste route te berekenen.
def Dijkstra(grid, source, destination):
    """The function to calculate the shortest route with dijkstra's
    The parameter grid should be in the form [[xCor, yCor], [xCor yCor]]
    The parameter source should be in the form [xCor, yCor]"""

    unvisited = copy.deepcopy(grid) # unvisited wordt een copy van het grid, wanneer een coordinaat is bezocht door het
                                    # algoritme wordt dit coordinaat uit unvisited gehaald.
    grid_Ext = copy.deepcopy(grid)  # Dit wordt het grid, maar met extra informatie belangrijk voor het algoritme,
                        # een coordinaat/vertex staat hier in de form:
                        # [xCor, Ycor, DistFromSource, OptimalPrevVertex, [neighbourVertex[xCor, yCor, dist]], visited]
                        # Wanneer een coordinaat de extra informatie bevat, wordt het een vertex genoemd in de code
    sourceIndex = grid_Ext.index(source) # De index van het doel in grid_Ext.
    # Hieronder wordt de extra informatie toegevoegd aan elk coordinaat/vertex, waarbij:
    # DistFromSource=-1, OptimalPrevVertex=[-1,-1], De lijst van buren is leeg, visited=0
    for vertex in grid_Ext:
        vertex.append(10000000000)
        vertex.append([-1,-1])
        vertex.append([])
        vertex.append(0)
        vertex[4] = neighboursCal(vertex, 40, 24)
    # print(len(grid_Ext))
    # print(grid_Ext[3])
    # print(grid_Ext[sourceIndex])
    # print("<><><><>")
    # print(unvisited[25])

    grid_Ext[sourceIndex][2] = 0 # zet de afstand tot de bron van de bron op 0

    currentNeighbourIndex = 0   # De index van de buur waar de afstand tot de bron wordt berekend
    currenVertexCor = copy.deepcopy(source)    # CurrenVertexCor is het coordinaat van de huidige vertex
    listUnVisitedNeighbours = []# Een lijst met coordinaten van buren met visited=0
                                # dit wordt gebruikt tijdens het bepalen welke volgende vertex bezocht moet worden
    step = 0

    # Dit is het Algoritme
    while len(unvisited) != 0:  # Het algorimte moet stoppen wanneer er geen onbezochte vertexen meer zijn.
        currenVertex = FindVertexFromCor(grid_Ext, currenVertexCor) # currenVertex: de vertex van het huidige coordinaat
        for neighbour in grid_Ext[grid_Ext.index(currenVertex)][4]: # For buren in de lijst met buren in currenVertex:
            currentNeighbourCor = []                # Wat is het coordinaat van de buur?
            currentNeighbourCor.append(neighbour[0])
            currentNeighbourCor.append(neighbour[1])

            currentNeighbour = FindVertexFromCor(grid_Ext, currentNeighbourCor)   # Dit is de vertex van de buur

            currentNeighbourIndex = grid_Ext.index(currentNeighbour) # Wat is de index van de buur in grid_ext

            if grid_Ext[currentNeighbourIndex][5] == 1: # als de buur visited=1 heeft,
                continue                                # hoeft hij niet opnieuw berekend te worden

            newDistance = grid_Ext[grid_Ext.index(currenVertex)][2] + neighbour[2] # Het berekenen van de afstand van de buur
                                                                            # tot de bron via het huidige coordinaat
            if newDistance < grid_Ext[currentNeighbourIndex][2]:    # Als deze afstand korter is dan de afstand bij de
                grid_Ext[currentNeighbourIndex][2] = newDistance    # huidige kortste route, dan is deze route dus
                grid_Ext[currentNeighbourIndex][3] = currenVertexCor# sneller en moet dit de nieuwe korste route worden
            listUnVisitedNeighbours.append(currentNeighbourCor) # De huidige buur moet wel bij listUnVisitedNeighbours
        try:
            #print("Current vertex for remove = {}".format(currenVertexCor))
            unvisited.remove(currenVertexCor) # Wanneer de afstand tot alle buren berekend is, is deze coordinaat bezocht
        except ValueError:
            print("Value Error!\n{}\nStep = {}".format(currenVertexCor, step))
            # print("Value? = {}".format(unvisited[25]))
            # print(currenVertexCor)
            # print("step = " + str(step))
            break
        grid_Ext[grid_Ext.index(currenVertex)][5] = 1 # Zet visited=1

        if (step % 20) == 0:
            print("Current step = " + str(step))
        if currenVertexCor == destination:
            print("Destination reached")
            #print(currenVertexCor)
            #print(destination)
            print("End step = " + str(step))
            break
        #print("Wich cor is next??")

        # Welke coordinaat moet nu worden bezocht? Dit wordt de coordinaat die het dichts bij de bron ligt en visited=0.
        shortestDistanceToSource = 10000             # Om er voor te zorgen dat niet alle afstanden
        for vertexxCor in listUnVisitedNeighbours:   # van alle coordinaten worden berekend, wordt het alleen berekend
            vertexx = FindVertexFromCor(grid_Ext, vertexxCor) # uit de lijst listUnVisitedNeighbours
            #print("Vertexx: {}\nVisited? {}".format(vertexx, vertexx[5]))
            if vertexx[5]== 1:
                listUnVisitedNeighbours.remove(vertexxCor)
                continue
            if grid_Ext[grid_Ext.index(vertexx)][2] < shortestDistanceToSource:
                shortestDistanceToSource = grid_Ext[grid_Ext.index(vertexx)][2]
                currenVertexCor = vertexxCor
                #print("New vertex for visiting is {}".format(currenVertexCor))
        step += 1

    # Nu moet de route berekend worden
    #print("route calculation")
    route_step = 0
    route_currentVertexCor = copy.deepcopy(destination)
    route_routeCors = []
    while(True):
        #print("Route calculationStep = {}, on vertex{}".format(route_step, route_currentVertexCor))
        route_routeCors.append(route_currentVertexCor)
        route_currentVertex = FindVertexFromCor(grid_Ext, route_currentVertexCor)
        route_currentVertexCor = route_currentVertex[3]
        if route_currentVertexCor == source:
            route_routeCors.append(route_currentVertexCor)
            break
        #print("Next vertex in route = {}".format(route_currentVertexCor))
        route_step += 1
        if route_step > 1000:
            print("Infinate loop? Something went wrong!")
            break
    return route_routeCors


theRoute = Dijkstra(gridCor, startCoordinate, DestinationCoordinate)

print("+++++++++++++++++++++++++\n{}\n+++++++++++++++++++++++++".format(theRoute))

#vertexx = [0, 0, -1, [-1,-1], [], 0]

#neighboursCal(vertexx, 4)
