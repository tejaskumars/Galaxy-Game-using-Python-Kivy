from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.graphics.context_instructions import Color
from kivy.properties import Clock, ObjectProperty, StringProperty
from kivy.core.window import Window
from platform import platform
import random
from kivy.lang.builder import Builder
from kivy.core.audio import SoundLoader

Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from keywords import _keyboard_closed, on_touch_down,on_touch_up,_on_keyboard_down, _on_keyboard_up
    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    
    NO_OF_VERTICAL_LINES = 8
    v_LINES_SPACING = .4
    vertical_lines = []
    NO_OF_HORIZONTAL_LINES = 15
    h_LINES_SPACING = .2 
    horizontal_lines = []

    SPEED = 1.2
    current_offset_y = 0
    current_Y_loop = 0

    SPEED_x = 3.0
    current_SPEED_X = 0
    current_offset_x = 0


    No_OF_TILES = 10 
    tiles = []
    tiles_coordinates= []

    ship = None
    SHIP_WIDTH = .1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04
    ship_coordinates = [(0,0),(0,0),(0,0)]

    
    game_over = False
    game_is_on = False

    score_txt = StringProperty()
    highscore_txt = StringProperty()
    newhighscore_txt = StringProperty()
    menu_title = StringProperty(" G   A   L   A   X   Y")
    menu_button_title = StringProperty("START")


    sound_begin = None
    galaxy = None
    gameover_impact = None
    gameover_voice = None
    music1 = None
    restart = None

    file = open("highscore.txt",'r')
    highscore = file.read()
    file.close()

    def __init__(self, **kwargs):
        super(MainWidget,self).__init__(**kwargs)
        self.init_audio()
        self.sound_galaxy.play()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def is_desktop(self):
        if platform in ('linux','windows','macosx'):
            return True
        else:
            return False

    def init_audio(self):
        self.sound_begin = SoundLoader.load("audio/begin.wav")
        self.sound_galaxy = SoundLoader.load("audio/galaxy.wav")
        self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
        self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")
        self.sound_music1 = SoundLoader.load("audio/music1.wav")
        self.sound_restart = SoundLoader.load("audio/restart.wav")

        self.sound_music1.volume = 1
        self.sound_begin.volume = .25
        self.sound_galaxy.volume = .25
        self.sound_gameover_impact.volume = .6
        self.sound_restart.volume = .25
        self.sound_gameover_voice.volume =.25

    def reset_game(self):
        self.sound_music1.play()
        self.current_offset_y = 0
        self.current_Y_loop = 0
        self.current_SPEED_X = 0
        self.current_offset_x = 0
        self.SPEED = 1.2
        self.score_txt = "SCORE :" +  str(self.current_Y_loop)
        self.highscore_txt = "HIGHSCORE :" + str(self.highscore)
        self.tiles_coordinates = []
        self.pre_fill_tiles()
        self.generate_tiles_coordinates()
        self.game_over = False


    def init_ship(self):
        with self.canvas:
            Color(0,0,0)
            self.ship = Triangle()
    def update_ship(self):
        centre_x = self.width /2
        base_y = self.SHIP_BASE_Y * self.height
        ship_half_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height
        
        self.ship_coordinates[0] = (centre_x - ship_half_width ,base_y)
        self.ship_coordinates[1] = (centre_x , base_y + ship_height)
        self.ship_coordinates[2] = (centre_x + ship_half_width ,base_y)

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2,y2 = self.transform(*self.ship_coordinates[1])
        x3,y3 = self.transform(*self.ship_coordinates[2])
        self.ship.points=[x1,y1,x2,y2,x3,y3]

    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x,ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_Y_loop + 1:
                return False
            if (self.check_ship_collision_with_tile(ti_x,ti_y)):
                return True
        return False

    def check_ship_collision_with_tile(self,ti_x, ti_y):
        xmin,ymin = self.get_tile_coordinate(ti_x,ti_y)
        xmax,ymax = self.get_tile_coordinate(ti_x +1 ,ti_y+1)
        for i in range(0,3):
            px,py = self.ship_coordinates[i]
            if(xmin <= px <= xmax and ymin <= py <= ymax ):
                return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0,self.No_OF_TILES):
                self.tiles.append(Quad())

    def pre_fill_tiles(self):
        for i in range(0,9):
            self.tiles_coordinates.append((0,i))


    def generate_tiles_coordinates(self):
        last_y = 0
        last_x = 0
        start_hindex = -int(self.NO_OF_VERTICAL_LINES/2) +1
        end_hindex = start_hindex +  self.NO_OF_VERTICAL_LINES-1

        for i in range(len(self.tiles_coordinates) -1 , -1 , -1):
            if self.tiles_coordinates[i][1]< self.current_Y_loop:
                del self.tiles_coordinates[i]

        if( len(self.tiles_coordinates) > 0):
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1 

        for i in range(len(self.tiles_coordinates),self.No_OF_TILES):
            r = random.randint(0,2)
            if (last_x <= start_hindex):
                r = 1
            if (last_x >= end_hindex - 1):
                r = 2
            self.tiles_coordinates.append((last_x,last_y))
            if (r==1):
                last_x +=1
                self.tiles_coordinates.append((last_x,last_y))
                last_y +=1
                self.tiles_coordinates.append((last_x,last_y))
            if (r==2):
                last_x -=1
                self.tiles_coordinates.append((last_x,last_y))
                last_y +=1
                self.tiles_coordinates.append((last_x,last_y))

            last_y +=1
           

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0,self.NO_OF_VERTICAL_LINES):
                self.vertical_lines.append(Line())


    def get_line_x_from_index(self, index):
        centrol_line_x = self.perspective_point_x
        spacing = self.v_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = centrol_line_x +offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        # start_line = self.perspective_point_x
        spacing = self.h_LINES_SPACING * self.height
        line_y = index * spacing - self.current_offset_y
        return line_y

    def get_tile_coordinate(self, ti_x , ti_y):
        ti_y =  ti_y - self.current_Y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self. get_line_y_from_index(ti_y)
        return x,y 


    def update_tiles(self):
        for i in range(0,self.No_OF_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
                
            xmin, ymin = self.get_tile_coordinate(tile_coordinates[0],tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinate(tile_coordinates[0]+1,tile_coordinates[1]+1)
            x1,y1 = self.transform(xmin,ymin)
            x2,y2 = self.transform(xmin,ymax)
            x3,y3 = self.transform(xmax,ymax)
            x4,y4 = self.transform(xmax,ymin)
            tile.points = [x1,y1,x2,y2,x3,y3,x4,y4]

    def update_vertical_lines(self):
        start_vindex = -int(self.NO_OF_VERTICAL_LINES/2) +1
        for i in range(start_vindex,start_vindex + self.NO_OF_VERTICAL_LINES):
            line_x = self.get_line_x_from_index(i)
            x1 , y1 = self.transform(line_x, 0)
            x2 , y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1,y1,x2,y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0,self.NO_OF_HORIZONTAL_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        start_hindex = -int(self.NO_OF_VERTICAL_LINES/2) +1
        end_hindex = start_hindex +  self.NO_OF_VERTICAL_LINES-1
        x_min = self.get_line_x_from_index(start_hindex)
        x_max = self.get_line_x_from_index(end_hindex)
        
        
        spacing_y = self.h_LINES_SPACING * self.height
        for i in range(0,self.NO_OF_HORIZONTAL_LINES):
            line_y = self.get_line_y_from_index(i)


            x1 , y1 = self.transform(x_min, line_y)
            x2 , y2 = self.transform(x_max, line_y)
            self.horizontal_lines[i].points = [x1,y1,x2,y2]

    def update(self , dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()
        if not self.game_over and self.game_is_on:
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor
            
            spacing_y = self.h_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_Y_loop +=1
                self.score_txt = ("SCORE :" +  str(self.current_Y_loop))
                self.highscore_txt = ("HIGHSCORE :" + str(self.highscore))
                if(self.current_Y_loop in [50,100,150,200,250,300]):
                    self.SPEED += 0.1
                self.generate_tiles_coordinates()
                
            
            speed_x = self.current_SPEED_X * self.width / 100
            self.current_offset_x += speed_x * time_factor

        if not self.check_ship_collision() and not self.game_over:
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            Clock.schedule_once(self.play_game_over_voice , 1)
            self.game_over = True
            self.menu_title = "G  A  M  E   O  V  E  R"
            self.menu_button_title = "RESTART"
            self.menu_widget.opacity = 1
            if (self.current_Y_loop > int(self.highscore)):
                self.newhighscore_txt = 'N E W  H I G H  S C O R E'
                file = open("highscore.txt", 'w')
                file.write(str(self.current_Y_loop))
                file.close()
                file = open("highscore.txt",'r')
                self.highscore = file.read()
                file.close()
            self.highscore_txt = ("HIGHSCORE :" + str(self.highscore))



            # print("game over")
    
    def play_game_over_voice(self, dt):
        self.sound_gameover_voice.play()

    def on_menu_button_pressed(self):
        if self.game_over:
            self.sound_restart.play()
            self.newhighscore_txt = ''
        else:
            self.sound_begin.play()
        self.sound_music1.play()
        self.reset_game()
        self.game_is_on = True
        self.menu_widget.opacity = 0
        
class GalaxyApp(App):
    pass


GalaxyApp().run()