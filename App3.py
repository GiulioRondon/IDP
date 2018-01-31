from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.utils import escape_markup
import threading
import time
from kivy.uix.textinput import TextInput
from Locatie_berekenen_functie import geef_positie
from Route_Bepalen import TotaalDijkstra
from Database import search_database, give_places

Builder.load_string('''
<Root>:
    canvas:
    
    Map:
        pos: self.pos
    Touch_pos:
    Your_Position:
        pos: self.pos
    GoTo:
    wall:
    Button1:
        pos: 430,750
    drawing:
    
        
<drawing>:        
    
<Button1>:
    Button:
        text: 'WC'
        on_press: root.on_press()
        size: 50,50
        
 

<Touch_pos>
<thread>


<line>

<Your_Position>:
    canvas:
        Color:
            rgba: 0.5,0.5,1,1
        Ellipse:
            pos: self.pos
            size: 20,20
            
<wall>
    canvas:
        Color:
            rgba: 0,0,0,1
        Rectangle:
            size: 10, 400
            pos: 500, 0

''')


Window.size = (800,480)
Window.clearcolor = (1,1,1,1)

User_Position_x = 0
User_Position_y = 0

start_new = True

def Get_Route():
    global User_Position_x
    global User_Position_y

    global GoToHere

    X = ((User_Position_x -10)/20) +1
    Y = ((User_Position_y -10)/20) +1

    RouteCoord_x =0
    RouteCoord_y =0

    Route_Coord_list = []
    X_Coordinate1 = X
    Y_Coordinate1 = Y
    X_Coordinate2 = int(GoToHere[1])
    Y_Coordinate2 = int(GoToHere[2])



    Dijkstra = TotaalDijkstra(X_Coordinate1, Y_Coordinate1, X_Coordinate2, Y_Coordinate2)


    route_coords = Dijkstra
    print(('DIJKSTRA: ' + str(route_coords)))

    GoX = ((int(GoToHere[1]) - 1) * 20) + 10
    GoY = ((int(GoToHere[2]) - 1) * 20) + 10
    print('WENT HERE: ' + str(GoX) + ', ' + str(GoY) + ' in grid: ' + str(GoToHere[0]) + ' ' + str(GoToHere[1]))

    for list in route_coords:
        RouteCoord_x = ((list[0]) * 20) + 10
        RouteCoord_y = ((list[1]) * 20) + 10
        Route_Coord_list.append([RouteCoord_x, RouteCoord_y])
    print(Route_Coord_list)
    return Route_Coord_list

def Get_Coordinates():
    global User_Position_x
    global User_Position_y

    while User_Position_x < 640:
        #In deze loop moeten iedere keer de nieuwe coordinaten opgevraagd worden
        #User_Position_x += 1
        #User_Position_y += 1
        coords = geef_positie()
        #print(coords)
        if coords[0] == 1:
            User_Position_x = 10
        if coords[1] == 1:
            User_Position_y = 10

        if coords[0] == 2:
            User_Position_x = 550
        if coords[1] == 2:
            User_Position_y = 110

        if coords[0] == 3:
            User_Position_x = 210
        if coords[1] == 3:
            User_Position_y = 210

        #print('done')
        time.sleep(1)

Get_Coordinates_Thread = threading.Thread(name='loop',target=Get_Coordinates) #runt 'Get_Coordinates' in de achtergrond
Get_Coordinates_Thread.start()

clicked = False

GoToCoords = []

line_position_x = 200
line_position_y = 0

line_length = 10
line_height = 10

class textinput(Widget):
    pass

times_pressed = 0
class Button1(Widget):

    def on_press(self):
        global start_new
        global GoToHere

        global User_Position_x
        global User_Position_y

        global times_pressed

        # if times_pressed >= 1:
        #     Root.canvas.remove(Root.ellipse)
        #     self.canvas.ask_update()
        #     print('should be removed')

        times_pressed +=1
        GoToHere = search_database('wc', [User_Position_x, User_Position_y])

        start_new = True


class Root(Widget):
    def __init__(self, **kwargs):
        super(Root,self).__init__(**kwargs)
        GoToCoords_Thread = threading.Thread(name='loop',target=self.Go_To_Coords_Function)
        GoToCoords_Thread.start()
        Draw_Places_Thread = threading.Thread(name='loop',target=self.get_places())
        Draw_Places_Thread.start()

    def startfunc(self):
        print('ewofjewoifjewo')

    def get_places(self):
        places_list = give_places()
        for list in places_list:
            X = ((int(list[1]) - 1) * 20) -10
            Y = ((int(list[2]) - 1) * 20) -10
            draw_places.draw_line(self,X,Y, list[0])

    # def on_touch_down(self, touch):
    #     global GoToCoords
    #     global touch_coords
    #
    #     global clicked
    #
    #     global schedule_line
    #
    #     touch_coords = touch.pos
    #     schedule_line = Clock.schedule_interval(self.draw_line, 0.1)
    #     schedule_line()
    #     clicked = True
    #     #update_line_coords()
    #
    #     print('done1')

    def Go_To_Coords_Function(self):
        global start_new
        start_new = False
        while True:
            while start_new == False:
                pass

            Route_Coord_list = Get_Route()

            for list in Route_Coord_list:
                Coords_For_Route = [list[0], list[1]]
                print(Coords_For_Route)
                drawing.draw_line(self, list[0], list[1])

class drawing(Widget):
    def draw_line(self,X_Coord, Y_Coord):
        global start_new
        #print(line_height, line_length, line_position_x, line_position_y)
        with self.canvas:
            Color(0,1,0)
            self.ellipse = Ellipse(pos=(X_Coord, Y_Coord), size=(line_length, line_height), rgba=(0,1,0,1))

        start_new = False

    def clear_canvas(self):
        self.canvas.children.remove(drawing.ellipse)
        self.canvas.ask_update()
        print('should be removed')

class draw_places(Widget):
    def draw_line(self,X_Coord, Y_Coord, text):
        global start_new
        #print(line_height, line_length, line_position_x, line_position_y)
        with self.canvas:
            Color(1,0,0)
            #self.ellipse = Ellipse(pos=(X_Coord, Y_Coord), size=(line_length, line_height), rgba=(0,1,0,1))
            #self.label = Label(text='[color=000000]WC[/color]', markup = True, pos=(X_Coord, Y_Coord))
            self.label = Label(text='[color=000000]' + escape_markup(text) + '[/color]', markup=True, pos=(X_Coord, Y_Coord), font_size=25)

        start_new = False

class Line(Widget):
    pass

class GoTo(Widget):
    pass

class wall(Widget):
    pass

class knop(Widget):
    pass

class Touch_pos(Widget): #zorgt ervoor dat de coordinaten waar je klikt in de console worden weergegeven
    def on_touch_down(self, touch):
        print(touch)

class Your_Position(Widget):
    def __init__(self, **kwargs):
        super(Your_Position,self).__init__(**kwargs)
        Clock.schedule_interval(self.move, 0.1)

    def move(self, *args):
        #Animation.cancel_all(self)
        global User_Position_x
        global User_Position_y

        #print(str(User_Position_x) + ', ' + str(User_Position_y))

        anim = Animation(x=User_Position_x,
                         y=User_Position_y,
                         duration=3/10)
        anim.start(self)

class Map(Widget):
    pass

runTouchApp(Root())
