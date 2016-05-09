import pygame as pg
import LogicGates

class Screen:
    
    def __init__(self,name,game):
        
        self.name = name
        
        self.game = game 
        
        self.area = None
        
        size = (900,600)
        self.background = blank_background(size,(0,0,0))
    
    def get_background(self):
        
        return self.background
    
    def set_backgound(self,background):
        
        self.background = background
        
    def get_play_area(self):
        
        return self.play_area
        
    def set_play_area(self,corner,area):
        
        self.area = PlayArea(corner,area,self)
   
    def draw(self,screen):
        
        screen.blit(self.background,(0,0))
        
        if self.area:
            
            self.area.draw(screen)

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
    
def blank_background(size,color = (0,0,0)):
    
    background = pg.Surface(size)
    background.convert()
    background.fill(color)
    
    return background
    