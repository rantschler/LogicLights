 #
# Project Title: 
#
# Author:  
#

#
# PACKAGES
#

import gameclass_0_97 as gc
import pygame as pg
from pygame.locals import *
from sys import exit
from LogicLogic import *
from LogicGates import *



DARK_GRAY = (169,169,169)
DIM_GRAY = (105,105,105)
GRAY = (128,128,128)
WHITE = (255,255,255)

#
# CLASSES
#


class Cursor:
    """ Current position of a person's hand.  May hold a logic element. """
    
    def __init__(self,position,size,object):
        
        self.x = position[0]
        self.y = position[1]
        
        self.w = size[0]
        self.h = size[1]
        
        self.contents = object
    
    def get_thing_from(self,other):
        
        if self.contents:
            return None
        
        thing = other.get_thing()
        
        if thing and thing.get_type() == "Factory":
            
            self.contents = thing.create(self)
            
            self.contents.set_container(self)
            
        elif thing and not thing.is_locked():
            
            self.contents = thing
            
            thing.set_container(self)
            
            other.remove_thing()
    
    def get_position(self):
        
        return (self.x,self.y)
    
    def get_center(self):
        
        return (self.x + self.w // 2 , self.y + self.h // 2)
    
    def get_size(self):
        
        return (self.w,self.h)
    
    def get_thing(self):
        
        return self.contents
        
    def drop(self,spaces):
        
        pass
        
    def update(self,position):
        
        self.x = position[0] - self.w // 2
        self.y = position[1] - self.h // 2

    def draw(self,screen):
        
        self.contents.draw(screen)

class Garbage:
    
    def __init__(self,pos,size):
        
        self.x = pos[0]
        self.y = pos[1] 
        
        self.w = size[0]
        self.h = size[1]
        
        self.contents = None
        
        self.color = DARK_GRAY
    
    def is_clicked(self,pos):
        """ Checks to see if a position is within the space. """
        
        test_x = 0 < pos[0] - self.x < self.w
        test_y = 0 < pos[1] - self.y < self.h
        
        return test_x and test_y
        
    def draw(self,screen):
        
        dw = self.w // 2
        x0 = self.x + dw
        y0 = self.y
        
        dx = self.w // 15
        dy = self.h // 20
        
        
        
        pg.draw.rect(screen,self.color,(self.x,self.y,self.w,self.h),1)

#
# FUNCTIONS
#

def draw_field(field,background,color = gc.BLACK):
    """ Modfies the background to mirror the playing surface.
    
        field - the gameclass Field object that represents the physical
                playing surface.
        background - the gameclass Background object that contains the 
                background image and scaling information to draw objects
                on the screen.
        color - the color of the background.
    """
    
    #
    # Import important quantities from background and field.
    #
    
    bg = background.get_size()
    fd = field.get_size()
    sz = field.get_fill()
    of = field.get_offset()
    
    #
    # Calculate scale and offset to be stored in the background class.
    #
    
    sc = float(bg[0])*sz/float(fd[0])
    background.set_scale(sc)
    offx = int(float(bg[0]) * of[0])
    offy = int(float(bg[1]) * of[1])
    background.set_offset((offx,offy))
    
    #
    # Fill the background with a single color and calculate the field
    # size in pixels.
    #
    
    field = pg.Surface(bg)
    field.convert()
    field.fill(color)
    
    field_size = (fd[0] * sc,fd[1] * sc)
    
    #
    # Draw your background below using the quantities above.
    #
    
    
    
    
    #
    # Draw onto the background.
    #
    
    background.detail(field,(offx,offy))
    
    pass
    

# 
# MVC FUNCTIONS
#

def engine(interval = 0,field = None,avatar = None,objects = []):
    ''' 
    The engine models the physics of your game by updating object
    positions, checking for collisions, and resolving them. 
    
        
        interval - time from last engine() call
        field - the field object that defines the playing area
        avatar - the player object
        objects - anything the avatar can interact with
                -or- another object can interact with.
    '''
    
    return None

def view(screen,background,avatar = None,things = [],foreground = None):
    ''' The view function draws things to the screen. 
    
        screen - The name of the screen to draw objects on.
        background - the background object containing the background
                    picture and scaling information for the objects.
        avatar - the object under the player's direct control.
        objects - other objects that need to be drawn in the game.
        foreground - a single PyGame surface to overlay on top of the 
                    objects.
    '''
    
    background.draw(screen)
    scale = background.get_scale()
    offset = background.get_offset()
    
    #
    # Draw all objects below.
    #
    
    for thing in things:
        thing.draw(screen)

    out = str(pg.mouse.get_pos())
    gc.screenprint(screen,out,(5,575))

    #
    # Draw all objects above.
    #
        
    pg.display.update()
    
    pass
    
def control(events,avatar = None, buttons = None):
    ''' Evaluates player input and sends messages to the avatar. 
    
        events - The pygame event list.
        avatar - The player object.
        buttons - A list of buttons that can directly control the avatar.
    '''

    pass
    
#
# MAIN
#

def win(screen):
    
    time = 0
    limit = 5000
    wait = True
    
    clock = pg.time.Clock()
    while wait and time < limit:
        
        time += clock.tick(30)
        
        screen_size = screen.get_size()
        
        x = screen_size[0] // 2 - 50
        y = screen_size[1] // 4
        
        gc.screenprint(screen,"Logic Lights",(x,y),24,gc.YELLOW)
        
        x += 12
        y += 150
        gc.screenprint(screen,"You Win!",(x,y),36,gc.WHITE)
        pg.display.update()
        
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == VIDEORESIZE:
                new_size = event.size
                screen = pg.display.set_mode(new_size,RESIZABLE,32)
                background.resize(new_size)
                field.imprint(draw_field,background)
            if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                
                wait = False

def splash(screen):
    
    wait = True
    
    while wait:
        
        
        background = gc.Background(screen.get_size(),gc.BLACK)
        
        screen_size = screen.get_size()
        
        x = screen_size[0] // 2 - 50
        y = screen_size[1] // 4
        
        background.draw(screen)
        gc.screenprint(screen,"Logic Lights",(x,y),24,gc.YELLOW)
        pg.display.update()
        
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == VIDEORESIZE:
                new_size = event.size
                screen = pg.display.set_mode(new_size,RESIZABLE,32)
                background.resize(new_size)
                field.imprint(draw_field,background)
            if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                
                wait = False

def game(screen,level):
    ''' 
    Function that controls the game.
    Includes:   (1) Initialization of variables, objects and lists
                (2) Game model, including:
                    (a) a call to your physics engine
                (3) Calls to view function
                (4) Calls to control function.
    '''    
    
    #
    # Initialize screen and clock
    #
    
    background = gc.Background(screen.get_size(),gc.BLACK)
    field_size = (80.0,60.0)
    field_scale = 0.5
    field_offset = (0.0,0.0)
    field = gc.Field(field_size,field_scale,field_offset)
    field.imprint(draw_field,background)
    
    clock = pg.time.Clock()
    
    #
    # Initialize game objects and loop variables
    #
    
    #
    # Active Area
    #
    
    area_corner = (100,50)
    area_size = (700,400)
    
    #
    # Grid Spaces:
    #
    
    sc = 13
    w = sc * 9
    h = sc * 4
    
    #
    # Toolbar
    #
    
    wires = []
    
    garbage = Garbage((800,475),(75,100))
    
    factories = []
    
    x = int( sc * 9 )
    y = 450
    
    x += sc * 11
    
    factories.append(Factory(LogicNot,(x,y)))
    
    x += sc * 11
    
    factories.append(Factory(LogicOr,(x,y)))
    
    x += sc * 11
    
    factories.append(Factory(LogicAnd,(x,y)))
    
    x += sc * 11
##     
##     Factory(LogicWire,tools[0])
##     
##     factories = [or_factory]
    
    #
    #
    #

    col = [gc.YELLOW,DARK_GRAY,gc.GRAY]
    
    x = 50
    y = 100 + sc
    
    buttonA = LogicSwitch("A")
    buttonA.set_position((x,y))
    
    y += sc * 10
    
    buttonB = LogicSwitch("B")
    buttonB.set_position((x,y))
    
    y += sc * 10
    
    buttonC = LogicSwitch("C")
    buttonC.set_position((x,y))
    
    buttons = [buttonA,buttonB,buttonC]
    
    program1 = create_truth_table(buttons,6)
    
    expression1 = And(Or(buttonA,buttonB),Or(And(Not(buttonA),buttonB),buttonC))
    
    x = 850
    y = 250 - 3 * sc
    
    light1 = LogicLight()
    #light1.program(expression1)
    light1.static_program(program1)
    
    light1.set_position((x,y))
    
    lights = [light1]
    
    cursor = None
    
    do_update = True
    
    win = False
    program = []
    #
    # Main loop for MVC game control.
    # 
    while not win:
        #
        # Update the time at the beginning of the loop.
        #
    
        interval = clock.tick(30)
        
        #
        # Model: All game mechanics
        ## Send physics problems to the engine.
        ## Resolve other mechanics (scoring, etc) here or in
        ## other functions
        #
        
        result = engine(interval,field)
        
        #
        # View: Draw all objects
        ## Send objects to the view function.
        #
        
        things = buttons + program + factories + lights + wires + [garbage]
        view(screen,background,None,things)
        
        #
        # Control: Take input from the user.
        ## Provide control of game state in the event loop.
        ## Call the control() function to control the avatar.
        #
        
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == VIDEORESIZE:
                new_size = event.size
                screen = pg.display.set_mode(new_size,RESIZABLE,32)
                background.resize(new_size)
                field.imprint(draw_field,background)
            if event.type == MOUSEBUTTONDOWN:
                check_pos = pg.mouse.get_pos()
                
                for object in buttons:
                    if object.is_clicked(check_pos):
                        object.toggle()
                        do_update = True
                        
                for thing in program:
                    
                    if thing.is_clicked(check_pos):
                        
                        cursor = thing 
                        return_space = check_pos
                    
                        
                for thing in buttons + lights + program:
                    
                    
                    for pad in thing.get_pads():
                        
                        if pad.is_clicked(check_pos):
                            
                            if pad.get_connector():
                                
                                cursor = pad.disconnect()
                                return_space = pad
                                
                            else:
                            
                                cursor = LogicWire(pad)
                                pad.set_connector(cursor)
                                wires.append(cursor)
                                return_space = None

                for factory in factories:
                    if factory.is_clicked(check_pos):
                        
                        cursor = factory.create(check_pos)
                        program.append(cursor)
                        return_space = None
                
            if event.type == MOUSEBUTTONUP:
                
                check_pos = pg.mouse.get_pos()
                do_update = True
                
                if cursor:
                    
                    if garbage.is_clicked(check_pos):
                        
                        if cursor.get_type() == "Wire":
                                
                            return_space = None
                            
                        else:
                        
                            program.remove(cursor)
                        
                            for pad in cursor.get_pads():
                            
                                wire = pad.get_connector()
                            
                                if wire:
                                    wire.deregister()
                                    wires.remove(wire)
                    
                    test_x = 0 < check_pos[0] - area_corner[0] < area_size[0]
                    test_y = 0 < check_pos[1] - area_corner[1] < area_size[1]
                    
                    if not ( test_x and test_y ) and cursor.get_type() != "Wire":
                        
                        if return_space:
                            
                            cursor.set_position(return_space)
                        
                        else: 
                            
                            if cursor in program:
                                program.remove(cursor)
                    
                    if cursor.get_type() == "Wire":
                        
                        found = False
                        
                        for item in buttons + lights + program:
                            
                            for pad in item.get_pads():
                                
                                clicked = pad.is_clicked(check_pos)
                                
                                wired = pad.is_wired()
                                
                                is_input = pad.get_type() == "Input"
                                
                                if clicked and not ( wired and is_input ):
                                    
                                    if cursor.connect(pad):
                                        
                                        found = True
                        
                        if not found:
                            
                            if return_space:
                                
                                cursor.connect(return_space)
                            
                            else:
                                
                                cursor.deregister()
                                wires.remove(cursor)
                        
                        
                    return_space = None
                    cursor = None
                        
        if cursor:
            
            cursor.set_position(pg.mouse.get_pos())
        
        if do_update:
            for light in lights:
                light.clear()
                win = light.evaluate(buttons)
            do_update = False
                


def main():
    
    ''' Function that controls the program state.'''    
    
    #
    # Initialize screen and clock
    #
    
    screen_size = (900,600)
    screen = pg.display.set_mode(screen_size,RESIZABLE,32)
    
    # login(screen)
    
    while True:
        
        level = splash(screen)
        
        game(screen,level)

        win(screen) 


#
# START UP
#



pg.init()

main()

