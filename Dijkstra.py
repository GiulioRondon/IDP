#####################
# In deze file is het Dijkstra algoritme uitgewerkt, alle functies in deze file zijn:
#
# GenCor(minX, maxX, minY, maxY), deze wordt gebruikt om alle coordinaten te genereren.
# neighboursCal(vertex, xMax, yMax), deze functie berekend alle buren van een coordinaat.
# FindVertexFromCor(ListWithVertex, coordinate), Omdat er twee "soorten" coordinaten worden gebruikt in deze code,
#   namelijk coordinaten in de form [xCor, yCor] en vertexen; coordinaten met extra informatie die belangrijk zijn voor
#   het dijkstra algoritme, moest er een functie komen om de vertex te vinden bij een coordinaat.
# Dijkstra(grid, source, destination), het algoritme! Deze berekend de snelste route van "source" naar "destination":
#   De functie genereerd de benodigde vertexen.
#   De functie ontwijkt obstakels
# De functie berekend de snelste weg en geeft deze in een multidimensional list in de form: [[xCor, yCor], [xCor, yCor]]
#
# Omdat bepaalde functies uit deze file worden gebruikt door de functie Dijkstra, moet deze file geimporteerd worden
# met de regel: "from Dijkstra import *"
#####################
import copy

def genCor(minX, maxX, minY, maxY):
    """The function that generates the coordinates for the grid, the output is a multidimensional list
    The parameters minX and minY are the lowest x and y values in the grid
    The parameters maxX and maxY are the highest x and y values in the grid"""
    maxX += 1
    maxY += 1
    lstCor = []
    for x in range(minX, maxX):              # Hier begint het genereren van alle coordinaten
        for y in range(minY, maxY):
            coordinate = [x, y]         # Een lijst met een coordinaat
            lstCor.append(coordinate)  # De coordinaat wordt toegevoegd aan lstCor
    return lstCor


# Hier wordt een functie aangemaakt om de coordinaten van alle "buren" te berekenen
# en alle negatieve coordinaten weghaalt
def neighboursCal(vertex, xMax, yMax):
    """Function to calculate all neighbours, this function could use optimization though
    The parameter vertex is the vertex """
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
    """Function to convert a coordinate to a vertex found in a grid
    The parameter ListWithVertex is the list that contains the vertex
    The parameter coordinate is the coordinate in the form [xCor, yCor]"""
    for vertex in ListWithVertex:
        vertexCor = []
        vertexCor.append(vertex[0])
        vertexCor.append(vertex[1])
        if coordinate == vertexCor:
            return vertex
    print("{} not found in list".format(coordinate))

# Dit wordt de functie om de kortste route te berekenen.
def Dijkstra(grid, source, destination, obstacles):
    """The function to calculate the shortest route with dijkstra's
    The parameter grid should be in the form [[xCor, yCor], [xCor yCor]]
    The parameter source should be in the form [xCor, yCor]
    The parameter destination should be in the form [xCor, yCor]
    The parameter obstacles should be in the form [[xCor, yCor], [xCor yCor]]"""

    unvisited = copy.deepcopy(grid) # unvisited wordt een copy van het grid, wanneer een coordinaat is bezocht door het
                                    # algoritme wordt dit coordinaat uit unvisited gehaald.
    grid_Ext = copy.deepcopy(grid)  # Dit wordt het grid, maar met extra informatie belangrijk voor het algoritme,
            # een coordinaat/vertex staat hier in de form:
            # [xCor, Ycor, DistFromSource, OptimalPrevVertex, [neighbourVertex[xCor, yCor, dist]], visited, obstacle]
                        # Wanneer een coordinaat de extra informatie bevat, wordt het een vertex genoemd in de code
    sourceIndex = grid_Ext.index(source) # De index van het doel in grid_Ext.
    # Hieronder wordt de extra informatie toegevoegd aan elk coordinaat/vertex, waarbij:
    # DistFromSource=-1, OptimalPrevVertex=[-1,-1], De lijst van buren is leeg, visited=0, obstacle=0
    for vertex in grid_Ext:
        vertex.append(10000000000)
        vertex.append([-1,-1])
        vertex.append([])
        vertex.append(0)
        vertex.append(0)
        vertex[4] = neighboursCal(vertex, grid[-1][0], grid[-1][1])
    # print(grid[-1])
    # print(grid[-1][0])
    # print(grid[-1][1])

    # Zet waarde obstacle in alle obstacle vertexen op 1
    for obstacle in obstacles:
        obstacleVertex = FindVertexFromCor(grid_Ext, obstacle)
        grid_Ext[grid_Ext.index(obstacleVertex)][6] = 1

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
            unvisited.remove(currenVertexCor) # Wanneer de afstand tot alle buren berekend is, is deze coordinaat bezocht
        except ValueError:
            print("Value Error!\n{}\nStep = {}".format(currenVertexCor, step))
            print("Value? = {}".format(unvisited[25]))
            print(currenVertexCor)
            print("step = " + str(step))
            break
        grid_Ext[grid_Ext.index(currenVertex)][5] = 1 # Zet visited=1

        if (step % 20) == 0:
            print("Current step = " + str(step))
        if currenVertexCor == destination:
            print("Destination reached")
            print("End step = " + str(step))
            break

        # Welke coordinaat moet nu worden bezocht? Dit wordt de coordinaat die het dichts bij de bron ligt, visited=0,
        shortestDistanceToSource = 10000             # En obstacle=0 heeft.Om er voor te zorgen dat niet alle afstanden
        for vertexxCor in listUnVisitedNeighbours:   # van alle coordinaten worden berekend, wordt het alleen berekend
            vertexx = FindVertexFromCor(grid_Ext, vertexxCor) # uit de lijst listUnVisitedNeighbours
            if vertexx[5]== 1 or vertexx[6] == 1: # Als die al bezocht is of een obstacle is...
                listUnVisitedNeighbours.remove(vertexxCor)
                continue
            if grid_Ext[grid_Ext.index(vertexx)][2] < shortestDistanceToSource:
                shortestDistanceToSource = grid_Ext[grid_Ext.index(vertexx)][2]
                currenVertexCor = vertexxCor
        step += 1

    # Nu moet de route berekend worden
    route_step = 0
    route_currentVertexCor = copy.deepcopy(destination)
    route_routeCors = []
    while(True):
        route_routeCors.append(route_currentVertexCor)
        route_currentVertex = FindVertexFromCor(grid_Ext, route_currentVertexCor)
        route_currentVertexCor = route_currentVertex[3]
        if route_currentVertexCor == source:
            route_routeCors.append(route_currentVertexCor)
            break
        route_step += 1
        if route_step > 1000:
            print("Infinate loop? Something went wrong!")
            break
    return route_routeCors
