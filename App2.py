from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
import threading
import time

Builder.load_string('''
<Root>:
    Map:
        pos: self.pos
    Touch_pos:
    
<Touch_pos>
<thread>

<Map>:
    AnchorLayout:
        size: 1920,1080
        ScatterLayout:
            Image:
                source: 'plattegrond.jpg'
            Your_Position:
                pos: self.pos

<Your_Position>:
    canvas:
        Color:
            rgba: 0.5,0.5,1,1
        Ellipse:
            pos: self.pos
            size: 17,17
''')


Window.size = (1920,1080)
Window.clearcolor = (1,1,1,1)

User_Position_x = 0
User_Position_y = 0
def Get_Coordinates():
    global User_Position_x
    global User_Position_y

    while User_Position_x < 640:
        #In deze loop moeten iedere keer de nieuwe coordinaten opgevraagd worden
        User_Position_x += 1
        User_Position_y += 1
        #print('done')
        time.sleep(0.01)

Get_Coordinates_Thread = threading.Thread(name='loop',target=Get_Coordinates) #runt 'Get_Coordinates' in de achtergrond
Get_Coordinates_Thread.start()

class Root(Widget):
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
