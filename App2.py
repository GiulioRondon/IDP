from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Color, Ellipse, Rectangle
import threading
import time
from Locatie_berekenen_functie import geef_positie

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
    
<Touch_pos>
<thread>

#<Map>:
    AnchorLayout:
        size: 1920,1080
        ScatterLayout:
            Image:
                source: 'plattegrond.jpg'
            Your_Position:
                pos: self.pos
<line>

<Your_Position>:
    canvas:
        Color:
            rgba: 0.5,0.5,1,1
        Ellipse:
            pos: self.pos
            size: 20,20



<GoTo>
    canvas:
        Color:
            rgba: 1,0,0,1
        Ellipse:
            size: 15,15
            pos: 700,10
            
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
            User_Position_x = 110
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



line_position_x = 200
line_position_y = 0

line_length = 10
line_height = 10

def update_line_coords():
    global line_position_x
    global line_position_y
    global line_length
    global line_height

    global User_Position_x
    global User_Position_y

    User_Position = [User_Position_x, User_Position_y]
    GoToCoords = [700,10]

    if GoToCoords[0] > GoToCoords[1]:
        print('X is biggest')
        line_position_x = User_Position_x + 10 #zorgt dat de lijn start bij de gebruiker
        line_position_y = User_Position_y

        while line_position_x < GoToCoords[0] - 10:
            if GoToCoords[0] > 510 and line_position_x < 490 or GoToCoords[0] < 490 and line_position_x > 510:
                if line_position_y < 410: #geeft de muur bij 400 aan
                    line_position_y += 10
                else:
                    line_position_x += 10
            else:
                line_position_x += 10
            time.sleep(0.1)
        while line_position_y < GoToCoords[1] - 10:
            line_position_y += 10
            time.sleep(0.1)

        if line_position_x > GoToCoords[0]: #herstelt de ontwijking van de muur bij hogere waarden
            while line_position_x > GoToCoords[0] +10:
                line_position_x -= 10
                time.sleep(0.1)
        if line_position_y > GoToCoords[1]:
            while line_position_y > GoToCoords[1] +10:
                line_position_y -= 10
                time.sleep(0.1)

        if line_position_x < GoToCoords[0]: #herstelt de ontwijking van de muur bij lagere waarden
            while line_position_x < GoToCoords[0] -10:
                line_position_x += 10
                time.sleep(0.1)
        if line_position_y < GoToCoords[1]:
            while line_position_y < GoToCoords[1] -10:
                line_position_y += 10
                time.sleep(0.1)



    if GoToCoords[1] > GoToCoords[0]:
        print('Y is biggest')
        line_position_x = User_Position_x
        line_position_y = User_Position_y + 10
        while line_position_y < GoToCoords[1] - 10:
            line_position_y += 10
            time.sleep(0.1)
        while line_position_x < GoToCoords[0] - 10:
            line_position_x += 10
            time.sleep(0.1)

    if GoToCoords[0] == GoToCoords[1]:
        print('Same')
        line_position_x = User_Position_x
        line_position_y = User_Position_y + 10
        while line_position_y < GoToCoords[1]:
            line_position_y += 10
            time.sleep(0.1)
        while line_position_x < GoToCoords[0]:
            line_position_x += 10
            time.sleep(0.1)

update_line_coords_Thread = threading.Thread(name='loop',target=update_line_coords)





class Root(Widget):
    def __init__(self, **kwargs):
        super(Root,self).__init__(**kwargs)
        Clock.schedule_interval(self.draw_line, 0.1)
        update_line_coords_Thread.start()

    def draw_line(self, touch):
        global line_position_x
        global line_position_y
        global line_length
        global line_height

        #print(line_height, line_length, line_position_x, line_position_y)
        with self.canvas:
            Color(0,1,0)
            Rectangle(pos=(line_position_x, line_position_y), size=(line_length, line_height), rgba=(0,1,0,1))

class Line(Widget):
    pass

class GoTo(Widget):
    pass

class wall(Widget):
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
