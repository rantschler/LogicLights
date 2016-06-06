import pygame as pg
import LogicGates

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
        
        if colors == None:
            self.colors = ColorScheme()
        else:
            self.colors = colors
            
        self.size = (900,600)
        self.background = blank_background(self.size,self.colors.get_background())
    
    def get_background(self):
        
        return self.background
    
    def set_backgound(self,background):
        
        self.background = background
    
    def get_colors(self):
        
        return self.game.get_colors()
    
    def get_play_area(self):
        
        return self.play_area
        
    def set_play_area(self,corner,area):
        
        self.area = PlayArea(corner,area,self)
   
    def draw(self,screen):
        
        screen.blit(self.background,(0,0))
        
        if self.area:
            
            self.area.draw(screen)

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
    
    background = pg.Surface(size)
    background.convert()
    background.fill(color)
    
    return background
    