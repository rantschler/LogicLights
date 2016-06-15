import pygame as pg
from LogicGates import *

SCALE = 13
WIDTH = 9
HEIGHT = 4

DARK_GRAY = (169,169,169)
DIM_GRAY = (105,105,105)
GRAY = (128,128,128)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
GREEN = (0,128,0)
RED = (255,0,0)
BLUE = (0,0,255)
DARK_RED = (191,0,0)
BLACK_RED = (64,0,0)
BLACK_GREEN = (0,32,0)
BLACK_BLUE = (0,0,64)

class Screen:
    
    def __init__(self,name,game,colors = None):
        
        self.name = name
        
        self.game = game 
        
        self.area = None
        
        self.buttons = []
        self.labels = []
        
        if colors == None:
            self.colors = ColorScheme()
        else:
            self.colors = colors
            
        self.size = (900,600)
        
        self.bg_animations = []
        self.animations = []
        self.fg_animations = []
        
        self.clear_background()
        self.clear_foreground()
    
    def initialize_background(self):
        
        self.clear_background()
        self.initialize(self.background)
        
    def get_background(self):
        
        return self.background
    
    def get_foreground(self):
        
        return self.foreground
    
    def get_animations(self):
        
        return self.bg_animations,self.animations,self.fg_animations
    
    def clear_background(self):
        
        self.background = blank_background(self.size,self.colors.get_background())
    
    def clear_foreground(self):
        
        self.foreground = blank_background(self.size,None)
    
    def set_background(self,new_background):
        
        self.background.blit(new_background,(0,0))
    
    def set_init(self,function):
        
        self.initialize = function
    
    def get_colors(self):
        
        return self.game.get_colors()
    
    def get_play_area(self):
        
        return self.play_area
    
    def get_buttons(self):
        
        return self.buttons
    
    def get_label(self,label):
        
        return self.labels[label]
    
    def add_label(self,label):
        
        self.labels.append(label)
    
    def set_play_area(self,corner,area):
        
        self.area = PlayArea(corner,area,self)
   
    def add_buttons(self,button):
        
        self.buttons.append(button)
   
    def draw_foreground(self,screen):
        """ Redraws the (static) foreground. """
        
        screen.blit(self.foreground,(0,0))
   
    def draw(self,screen):
        """ Draws the objects in the screen.  
            background -> active elements -> foreground 
        """
        screen.blit(self.background,(0,0))
        
        if self.area:
            
            self.area.draw(screen)
            
        for button in self.buttons:
            
            button.draw(screen)
        
        for label in self.labels:
            
            label.draw(screen)
            
        for thing in self.animations:
            
            thing.draw(screen)
            
        screen.blit(self.foreground,(0,0))
            
        for thing in self.fg_animations:
            
            thing.draw(screen)
        
        pg.display.update()



class Scales:
    """ Keeps track of scales on the screen, doing interesting mathematics
        so that you don't have to. 
    """
    
    def __init__(self , screens , scale ):
        
        self.screen_width = screens[0]
        self.screen_height = screens[1]
    
        self.element_width = 9
        self.element_height = 4
    
        self.scale = scale
    
    def set_scale(self,size):
        
        self.scale = size
    
    def get_scale(self):
    
        return self.scale
    
    def get_screen_size(self):
        
        return (self.screen_width,self.screen_height)
    
    def get_element_size(self):

        x = scale * self.element_width
        y = scale * self.element_height
        
        return (x,y)
    

class TextBox:
    
    def __init__(self,message,pos= (0,0),size = 16):
        """ Creates a text message to write on the screen. """
        
        #
        # Position in center
        #
        self.position = pos
        
        self.size = size
        self.message = str(message)
        
        self.draw_message(size)
        
    def draw_message(self):
        
        size = self.size
        
        message = self.message
    
        outputfont = pg.font.SysFont(font,size)
        self. message = outputfont.render(message,1,color)
    
    def draw(self,screen):
   
        screen.blit(self.message,pos)

class Message:
    
    def __init__(self,pos,static,dynamic = None):
        
        self.x = pos[0]
        self.y = pos[1]
        self.base = static
        self.end = dynamic
        
        self.size = 20
    
    def set_size(self,size):
        
        self.size = size
    
    def update_variable(self,variable):
        
        self.end = variable
    
    def render(self):
        
        message = self.base + " " + self.end()
        self.message = make_label(message,self.size)
    
    def draw(self,screen):
        
        self.render()
        screen.blit(self.message,(self.x,self.y))

class FadeIn:
    
    def __init__(self,message,pos = (0,0),size = 36,color2 = WHITE,color1 = BLACK):
        
        
        self.msg = message
        
        self.x = pos[0]
        self.y = pos[1]
        
        self.size = size
        
        self.color1 = color1
        self.color2 = color2
        self.color = color1
        
        self.reset()
        
    def reset(self):
        
        self.time = 0
        self.color = self.color1
    
    def is_out(self,place):
        
        pass
    
    def update(self,dt):
        
        self.time += dt
        
        self.color = mix_colors(self.color1, self.color2, float(self.time) / 1000.0)
    
    def draw(self,screen):
        
        screenprint(screen,self.msg,(self.x,self.y),self.size,self.color)
    

class PlayArea:
    
    def __init__(self,corner,area,owner):
        
        self.owner = owner
        
        self.x = corner[0]
        self.y = corner[1]
        self.w = area[0]
        self.h = area[1]
        
        self.light = None
        self.switches = []
        self.program = []
        self.wires = []
    
    def is_clicked(self,pos):
        
        check_x = 0 < pos[0] - self.x < self.w
        check_y = 0 < pos[1] - self.y < self.h
        
        return check_x and check_y
        
    def get_item(self,item):
        
        for thing in self.program:
            
            if thing.is_clicked():
                
                self.program.remove(thing)
                
                return thing
            
        for wire in self.wires:
            
            for pad in wire.get_pads():
                
                if pad.is_clicked():
                    
                    pad.deregister()
                    
                    return wire
    

class ColorScheme:
    """ Defines a color scheme for the game. """
    
    def __init__(self):
        """ Set default colors for the color scheme. """
        
        self.bg = BLACK         # Background Color Default
        self.oc = DARK_GRAY     # Outline Color Default
        self.ic = GRAY          # Interior Color Default
        self.title = YELLOW     # Title Color Default
        self.text = WHITE       # Text Color Default
        self.on = RED           # Color when puzzle should be on
        self.off = DARK_RED     # Color when puzzle should be off
        self.light = YELLOW     # Color when player's answer should be on
        
        pass
        
    def set_background(self,color):
        
        self.bg = color
    
    def set_outline(self,color):
        
        self.oc = color
        
    def set_interior(self,color):
        
        self.ic = color
        
    def set_text(self,color):
        
        self.text = color
        
    def set_off(self,color):
        
        self.off = color
    
    def set_on(self,color):
        
        self.on = color
        
    def set_light(self,color):
        
        self.light = color
    
    def get_light(self,color):
        
        return self.light
    
    def get_on(self,color):
        
        return self.on
    
    def get_off(self,color):
        
        return self.off
        
    def get_background(self):
        
        return self.bg 
    
    def get_outline(self):
        
        return self.oc
        
    def get_interior(self):
        
        return self.ic
        
    def get_text(self):
        
        return self.text

    
def blank_background(size,color = (0,0,0)):
    
    if color == None:
        color = (1,1,1)
    
    background = pg.Surface(size)
    background.convert()
    background.fill(color)
    
    if color == (1,1,1):
        background.set_colorkey((1,1,1))
    
    return background

def make_label(message,size = 20,color = WHITE,font="Arial"):
    
    outputfont = pg.font.SysFont(font,size)
    
    return outputfont.render(message,1,color)
    

def centered(graphic,area):
    
    size = graphic.get_size()
    position = ( area[0] // 2 - size[0] // 2 , area[1] // 2 - size[1] // 2 )
    container = pg.Surface(area)
    container.convert()
    container.fill((1,1,1))
    container.blit(graphic,position)
    container.set_colorkey((1,1,1))
    
    return container
    
    
def mix_colors(color1,color2,percent):
    
    if percent < 0.0:
        
        percent = 0.0
    
    elif percent > 1.0:
        
        percent = 1.0
    
    dR = color2[0] - color1[0]
    dG = color2[1] - color1[1]
    dB = color2[2] - color1[2]
    
    new_R = int(color1[0] + float(dR) * percent)
    new_G = int(color1[1] + float(dG) * percent)
    new_B = int(color1[2] + float(dB) * percent)
    
    return ( new_R , new_G , new_B )
