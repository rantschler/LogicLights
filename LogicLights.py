#
# Project Title: Logic Lights
#
# Main Program
#
# Author: Jim Rantschler
#

#
# PACKAGES 
#

import random,math
from LogicScreen import *
from LogicGates  import *
from pygame.locals import *
import pygame as pg
from sys import exit

VERSION = "W0.4"

#
# CLASSES
#

class WingdingContainer:
    
    def __init__(self,Generated,generator=None,owner=None):
        
        self.Archetype = Generated
        
        self.game = owner
        
        self.limit = 500.0
        self.clear()
        
    def clear(self):
        
        self.time = 0
        self.elements = []
    
    def generate(self,time):
        
        pos = pg.mouse.get_pos()
        
        if random.random() < float(self.time)/self.limit:
            
            self.elements.append(self.Archetype(pos))
            self.time = 0
        
    def update(self,dt):
        
        self.time += dt
        
        self.generate(self.time)
        
        kill_list = []
        border = self.game.get_size()
        for element in self.elements:
            element.update(dt)
            if element.is_outside_of(border):
                kill_list.append(element)
        for the_dead in kill_list:
            self.elements.remove(the_dead)
        
    def draw(self,screen):
        
        for element in self.elements:
            
            element.draw(screen)
        
class Wingding:
    
    def __init__(self,position):
        
        self.x = float(position[0])
        self.y = float(position[1])
        self.angle = random.random() * 2 * math.pi
        self.rotation = random.random() * 0.4 - 0.2
        
        self.sides = random.choice([3,4,5,6,8])
        self.create_rotations()
        
        self.radius = random.choice([5,7,10,15,5,7,10,5,7,5,7,5,5,5])
        
        self.vx = (random.random()*2.0 - 1.0) * 15.0 / float(self.radius)
        self.vy = (random.random()*2.0 - 1.0) * 15.0 / float(self.radius)
        
        self.color = (  random.choice(range(128))+64    ,
                        random.choice(range(128))+64    ,
                        random.choice(range(128))+64    )
        
    def update(self,dt):
        """ Moves and rotates wingding. """
        self.x += self.vx
        self.y += self.vy
        self.angle += self.rotation
    
    def is_outside_of(self,area):
        """ Checks to see if the wingding is outside of its intended area. """
        
        in_x = -self.radius < self.x < area[0] + self.radius
        in_y = -self.radius < self.y < area[1] + self.radius
        
        return not in_x or not in_y
            
    def create_rotations(self):
        """ Sets up rotation matrix. """
        
        angle = 2 * math.pi / float(self.sides)
        
        self.rot = [[0.0,0.0],[0.0,0.0]]
        
        self.rot[0][0] = math.cos(angle)
        self.rot[1][1] = self.rot[0][0]
        self.rot[1][0] = math.sin(angle)
        self.rot[0][1] = -1.0 * self.rot[1][0]
    
    def draw(self,screen):
        
        x0 = float(self.radius) * math.cos(self.angle)
        y0 = float(self.radius) * math.sin(self.angle)
        
        pos = []
        pos.append([x0,y0])
        for application in range(self.sides-1):
            x0 = pos[-1][0] * self.rot[0][0]
            x0 += pos[-1][1] * self.rot[0][1]
            y0 = pos[-1][0] * self.rot[1][0]
            y0 += pos[-1][1] * self.rot[1][1]
            pos.append([x0,y0])
            
        for point in pos:
            point[0] += self.x
            point[1] += self.y
            point[0] = int(point[0])
            point[1] = int(point[1])
            
        pg.draw.polygon(screen,self.color,pos)
        
    
class Scrollbar:
    """ Scrolls up and down so user can choose the puzzle to play. """
    
    def __init__(self,levelbox):
        
        self.box = levelbox
        screen = levelbox.get_screen()
        list = levelbox.get_list_screen()
        
        size = screen.get_size()
        listsize = list.get_size()
        
        buttonsize = (20,20)
        self.buttonsize = buttonsize
        
        self.x = 2
        self.y = 27
        
        self.w = buttonsize[0]
        self.h = size[1] - 50 - 2 * buttonsize[1]
        
        self.buttons = []
        self.buttonsize = buttonsize[1]
        self.set_buttons()
        self.pos = 0
        self.max = listsize[1] - self.h
        
        self.listsize = listsize[1]
        
        self.slidersize = 10
        
    def is_clicked(self,pos):
        """ Checks to see if the level is clicked. """
        
        in_levelbox = ( pos[0] - self.x ,
                        pos[1] - self.y )
        
        check_x = 0 < in_levelbox[0] < self.w
        check_y = 0 < in_levelbox[1] < self.h + 2 * self.buttonsize
        
        return check_x and check_y 
    
    def get_box(self):
        """ Returns the container the scrollbar is attached to. """
        
        return self.box

    def set_buttons(self):
        """ Formats the buttons on the scrollbar. """
        
        size = [self.buttonsize]*2
        
        top_position = (self.x,self.y)
        bottom_position = (self.x,self.y + self.h + size[1] + 2)
        
        up = Button(size,top_position,self)
        up.set_ornament(draw_triangle(size,"Up"))
        up.set_action(move_scrollbar(self,-10))
        down = Button(size,bottom_position,self)
        down.set_ornament(draw_triangle(size,"Down"))
        down.set_action(move_scrollbar(self,10))
        
        self.buttons = [up,down]
        
    def scroll_to(self,pos,skip = False):
        """ Directly move to a position on the scrollbar. """
        
        for button in self.buttons:
            
            if not skip and button.is_clicked(pos):
                
                button.activate()
                
                return None
                
        self.pos = pos[1] - self.y - self.buttonsize - self.slidersize // 2
        
        if self.pos < 0:
            
            self.pos = 0
        
        if self.pos > self.h - self.slidersize:
            
            self.pos = self.h - self.slidersize 
            
        return self
    
    
    def get_position(self):
        """ Returns the position on the list that corresponds to the 
            position of the scrollbar.
        """
        
        return int(float(self.pos)/(self.h-self.slidersize)*(self.max-40))
    
    def get_buttons(self):
        """ Returns the scrollbar buttons. """
        
        return self.buttons
        
    def shift(self,amount):
        """ Shift the scrollbar up or down. """
        
        self.pos += amount
        
        if self.pos < 0:
            
            self.pos = 0
            
        if self.pos > self.h - self.slidersize:
            
            self.pos = self.h - self.slidersize
    
    def draw(self,screen):
        
        x = self.x
        y = self.y + self.buttonsize
        
        y0 = y + self.pos
        
        size = screen.get_size()
        pg.draw.rect(screen,(16,0,0) ,((x,y),(self.w,self.h)))
        pg.draw.rect(screen,GRAY,((x,y),(self.w,self.h)),2)

        pg.draw.rect(screen,GRAY,((x,y0),(self.w,self.slidersize)))

        
        for button in self.buttons:
            
            button.draw(screen)

class Button:
    """ Buttons for the scrollbar. """
    
    def __init__(self,size,pos = (0,0),owner = None):
        
        self.x = pos[0]
        self.y = pos[1]
    
        self.w = size[0]
        self.h = size[1]
        
        self.owner = owner
        
        self.action = None
        
        self.outline = BLACK   
        self.size = 1
        self.fill = GRAY
    
        self.ornament = None
    
    def is_clicked(self,pos):
        """ Check if the button has been clicked. """
        
        test_x = 0 < pos[0] - self.x < self.w
        test_y = 0 < pos[1] - self.y < self.h
        
        if test_x and test_y:
            return True
        else:
            return False
    
    def set_position(self,pos):
        """ Place the position of the button on the screen. """
        
        self.x = pos[0]
        self.y = pos[1]
    
    def set_border(self,color,thickness = None):
        
        self.outline = color
        
        if thickness:
            self.size = thickness
    
    def set_interior(self,color):
        
        self.fill = color
        
    def set_ornament(self,decoration):
        """ Place a drawing in the button. """
        
        self.ornament = decoration
    
    def set_action(self,action):
        """ Set the functionality of the button. """
        
        self.action = action
    
    
    def activate(self):
        """ Perform the action stored in self.action """
        
        if self.action:
            
            self.action()
    
    def draw(self,screen):
        
        ulc = (self.x,self.y)
        llc = (self.x,self.y+self.h)
        lrc = (self.x+self.w,self.y+self.h)
        
        size = (self.w,self.h)
        
        if self.fill:
            pg.draw.rect(screen,self.fill,(ulc,size))
##         
##         pg.draw.line(screen,self.outline,ulc,(ulc[0]+self.w,ulc[1]),1)
##         pg.draw.line(screen,self.outline,llc,(llc[0]+self.w,llc[1]),1)
##         
        if self.ornament:
            
            screen.blit(self.ornament,(self.x,self.y))
        
        if self.outline:
            pg.draw.rect(screen,self.outline,(ulc,size),self.size)
        

class LevelBox:
    """ Keeps track of the level and the puzzles for the level. """
    
    def __init__(self,level,pos,size,user):
        
        self.level = level
        self.puzzles = range(4 ** level)
        self.player = user
    
        self.scores = []
        
        for puzzle in self.puzzles:
            self.scores.append(None)
    
        self.x = pos[0]
        self.y = pos[1] 
    
        self.make_screen(size)
        self.make_list()
        self.make_foreground(size)
        
        self.scrollbar = Scrollbar(self)
        
        if level == 1:
            
            self.scrollbar = None
        
        self.top = 0
    
    def get_scores(self):
        """ Get a list of the results of the various puzzles of this level. """
        
        return tuple(self.scores)
    
    def get_level(self):
        """ Returns the level of the level box. """
         
        return self.level
    
    def get_position(self):
        """ Returns the position of the level box. """
        
        return (self.x,self.y)
    
    def get_random_puzzle(self):
        """ Returns a random puzzle. """
        
        return random.choice(self.puzzles)
    
    def get_screen(self):
        """ Returns the output screen. """
        
        return self.out
    
    def get_list_screen(self):
        """ Returns the screen list. """
        
        return self.list
    
    def get_puzzle_value(self,puzzle):
        """ Returns the status of a puzzle. """
        
        return self.scores[puzzle]
    
    def make_list(self):
        """ Makes a graphical display of the list of levels for the level. """
        
        x = self.out.get_size()[0] - 15
        y = len(self.puzzles) * 20 + 10
        
        self.list = pg.Surface((x,y))
        self.list.convert()
        self.list.fill((0,0,32))
        
        x = 0
        y = -15
        
        for n in self.puzzles:
            y += 20
            screenprint(self.list,str(n),(x,y),18)
            if self.scores[n] == True:
                pg.draw.circle(self.list,YELLOW,(x+60,y+9),7)
            elif self.scores[n] == False:
                pg.draw.circle(self.list,WHITE,(x + 60,y+9),7,1)
        
    def make_screen(self,size):
        """ Creates the main screen for the level. """
        
        self.out = pg.Surface(size)
        self.out.convert()
        self.out.fill((0,0,32))
    
    def make_foreground(self,size):
        """ Draws a foreground with a hole in it for viewing the levels. """
        
        self.fore = pg.Surface(size)
        self.fore.convert()
        self.fore.fill((192,128,128))
        self.fore.set_colorkey((192,128,128))
        
        x,y = size
        
        pg.draw.rect(self.fore,(32,0,0),((0,0),(20,y)))
        pg.draw.rect(self.fore,(32,0,0),((x - 20,0),(20,y)))
        pg.draw.rect(self.fore,(32,0,0),((0,0),(x,25)))
        
        if self.level == 1:
            pg.draw.rect(self.fore,(32,0,0),((0,125),(x,y - 100)))
        else:
            pg.draw.rect(self.fore,(32,0,0),((0,225),(x,y - 225)))
    
        if self.level == 0:
            out = "1 Switch"
        else:
            out = str(self.level)
            out += " Switches"
    
        screenprint(self.fore,out,(4,2),22)
        
        pg.draw.rect(self.fore,WHITE,((0,0),(x,y)),2)
    
    def is_clicked(self,pos):
        """ Checks to see if the level is clicked. """
        
        size = self.out.get_size()
        
        in_levelbox = ( pos[0] - self.x , pos[1] - self.y )
        
        check_x = 0 < in_levelbox[0] < size[0]
        check_y = 0 < in_levelbox[1] < size[1]
        
        if self.scrollbar:
            
            not_scrollbar = not self.scrollbar.is_clicked(in_levelbox)
        
        else:
            
            not_scrollbar = True
        
        
        return check_x and check_y and not_scrollbar
    
    def get_clicked(self,pos):
        """ Gets the level clicked by the user. Returns a random level if
            viable.
        """
        
        level = None
        
        size = self.out.get_size()
        
        in_levelbox = ( pos[0] - self.x - 20, pos[1] - self.y - 25 )
        
        if in_levelbox[0] < 0 or in_levelbox[1] < 0:
            
            level = None
            
        elif self.level > 1 and in_levelbox[1] > 200:
            
            level = random.choice(self.puzzles)   
            
        elif self.level == 1 and in_levelbox[1] > 200:
            
            level = "Tutorial"
        
        else:
            
            y = in_levelbox[1]
            
            if self.scrollbar:
                y += self.scrollbar.get_position()

            level = ( y - 5 ) // 20
          
            if self.level == 1 and level > 3:
                
                level = None
        
        return level
    
    def click_internals(self,pos):
        """ Checks if components of the level box are clicked. """
        
        size = self.out.get_size()
        
        in_levelbox = ( pos[0] - self.x , pos[1] - self.y )
        
        if self.scrollbar:
            
            if self.scrollbar.is_clicked(in_levelbox):
                
                self.scrollbar.scroll_to(in_levelbox)
        
    def set_puzzle_value(self,puzzle,score):
        """ Returns the result of a paticular puzzle. """
        
        self.scores[puzzle] = score
    
    def draw(self,screen,pos):
        """ Draw the level box on the screen with scrollbars, and levels. """
        
        x = 25
        y = 25
        if self.scrollbar:
            y -= self.scrollbar.get_position()
        
        self.out.blit(self.list,(x,y))
        
        self.out.blit(self.fore,(0,0))
        
        if self.level == 1:
            x = 40
            y = 225
            screenprint(self.out,"Tutorial",(x,y))
        else:
            
            x = 45
            y = 225
            screenprint(self.out,"Random",(x,y))
        
        if self.scrollbar:
            self.scrollbar.draw(self.out)
        
        x0 = self.x + pos[0]
        y0 = self.y + pos[1]
        
        screen.blit(self.out,(x0,y0))


class Tutorial:
    """ A set of instructions to help people play the game. """
    
    def __init__(self,tutorial = None): 
        
        self.current = 0
        
        self.levels = []
        
        self.load(tutorial)
        
    def __str__(self):
        
        n = 0
        for level in self.levels:
            n += 1
        
    def load(self,tutorial = None):
        """ Loads the tutorial from a text file. """
        
        if not tutorial:

            file = "tutorial.txt"

        read_file = open(file,"r")
        
        line = "/B/"
        line_head = "/B/"
        
        while line_head == "/B/":
            
            if len(line) >= 10 and line[4:10] == "LEVELS":
                
                num = 6
                
            line = read_file.readline().strip()
            line_head = line[0:3]
        
        for n in range(num):
            
            self.levels.append(TutorialLevel())
            
            code = "/"+str(n)+"/"
        
            while line_head == code:
                
                head = line[4:7]
                rest = line[8:]
                
                if head == "LVL":
                    
                    level = int(rest)
                    
                    self.levels[n].set_level(level)
                
                elif head == "PZL":
                    
                    puzzle = int(rest)
                    
                    self.levels[n].set_puzzle(puzzle)
                
                elif head == "MSG":
                    
                    x = int(rest[0:3])
                    y = int(rest[4:7])
                    x0 = int(rest[8:11])
                    y0 = int(rest[12:15])
                    msg = rest[16:]
                    
                    box = MessageBox(msg,(x,y),(x0,y0))
                    self.levels[n].add_message(box)
             
                line = read_file.readline().strip()
                line_head = line[0:3]
                
        read_file.close()
        
    def get_level(self):
        """ Returns the active tutorial level. """
        
        return self.levels[self.current].get_level()
    
    def get_puzzle(self):
        """ Returns the active puzzle in the tutorial. """
        
        return self.levels[self.current].get_puzzle()
        
    def display_current(self,screen):
        """ Displays the current message on the screen. """
        
        self.levels[self.current].display_message(screen)
        
    def is_clicked(self,pos):
        """ Has the tutorial message been clicked? """
        
        return self.levels[self.current].is_clicked(pos)
        
    def advance(self):
        """ Go to the next level. """
        
        self.current += 1
        
        if self.current >= len(self.levels):
            
            return True
        
        return False
        
    def advance_message(self):
        """ Go to the next level. """
        
        self.levels[self.current].advance()
        
class TutorialLevel:
    
    def __init__(self,level = 0,puzzle = 0):
        
        self.level = level
        self.puzzle = puzzle
        
        self.messages = []
        self.message = 0
        
    def get_level(self):
        
        return self.level
    
    def get_puzzle(self):
        
        return self.puzzle
        
    def set_level(self,level):
        
        self.level = level
    
    def set_puzzle(self,puzzle):
        
        self.puzzle = puzzle
        
    def add_message(self,message):
        
        self.messages.append(message)
        
    def display_message(self,screen):
        
        if self.message < len(self.messages):
            self.messages[self.message].draw(screen)
        
    def is_clicked(self,pos):
        
        if self.message < len(self.messages):
            return self.messages[self.message].is_clicked(pos)
        
        return False
    
    def advance(self):
        
        self.message += 1
        
    def next(self):
        
        if self.message < len(self.messages) - 1:
            self.message += 1
        
    def draw(self,screen): 
        
        if message:
            
            for message in messages:
                
                message.draw(screen)

class MessageBox:
        
    def __init__(self,message,pos=(0,0),line=(0,0)):
        
        self.x = pos[0]
        self.y = pos[1]
        
        self.line_x = line[0]
        self.line_y = line[1]
        
        self.make_message(message)
    
    def set_line(self,pos):
        
        self.line_x = pos[0]
        self.line_y = pos[1]
    
    def make_message(self,message):
        
        font = 12
        n = 2 * int(len(message)**0.5)
        if n < 15:
            n = 15
        lines = []
        x = 0
        y = 0
        i = 0
        for m in range(n):
            while len(message) > n + i and message[n+i] != " " :
                i += 1
            current_line = message[:n+i]
            lines.append(screenprint(None,current_line,(0,0),font))
            size = lines[-1].get_size()
            if not not current_line:
                if size[0] > x:
                    x = size[0]
                y += size[1] + 2
            
            message = message[n+i+1:]
        
        self.message = pg.Surface((x + 8,y + 8))
        self.message.convert()
        self.message.fill((0,0,0))
    
        pg.draw.rect(self.message,(255,255,255),((0,0),(x+8,y+8)),2)
    
        x = 4
        y = 4
        
        for line in lines:
            self.message.blit(line,(x,y))
            y += size[1] + 2

    def is_clicked(self,pos):
        
        w , h = self.message.get_size()
        
        test_x = 0 < pos[0] - self.x < w
        test_y = 0 < pos[1] - self.y < h
        
        return test_x and test_y
        
        
    def draw(self,screen):
        
        pos = (self.x,self.y)
        size = self.message.get_size()
        x = self.x + size[0] // 2 
        x0 = x + self.line_x
        y = self.y + size[1] // 2 
        y0 = y + self.line_y
        
        pg.draw.line(screen,WHITE,(x,y),(x0,y0),2)
        screen.blit(self.message,pos)
        
        

class Dude:
    """ Class containing the current player's inofrmation. """
    
    def __init__(self,name):
        
        self.name = name
        self.file = None
        
        self.level = 0
        self.levels = []
        self.puzzle = 0
        
        self.stars = []
        
        self.tutorial = None
        self.tutorial_active = False

        self.result = None

    def initialize_levels(self,x,y,size):
        
        for n in range(4):
            x += 175 
            n += 1
            current_level = LevelBox(n,(x,y),size,self)
        
            out = None
            for m in range(4**(n+1)):
              
                if out:
                    current_level.set_puzzle_value(m,out)
           
            self.add_level(current_level)
            
    #
    # File functions
    #
    def set_filename(self,name):
        """ Gives a file name to the player. """
        
        self.file = name
    
    def save(self):
        """ Save the player's data. """
        
        newfile = open("ids/"+self.file+".idf","w")
        
        for level in self.levels:
            for score in level.get_scores():
                if score == False:
                    newfile.write("Loss")
                elif score == True:
                    newfile.write("Win ")
                else:
                    newfile.write("None")
            newfile.write("\n")
        
        newfile.close()
        
        pass
    
    def load(self):
        """ Loads the player's data. """
        
        oldfile = open("ids/"+self.file+".idf","r")
        
        i = 0
        for line in oldfile:
            level = self.levels[i]
            n = 0
            for score in level.get_scores():
                start = n * 4
                end = start + 4
                if line[start:end] == "Loss":
                    level.set_puzzle_value(n,False)
                elif line[start:end] == "Win ":
                    level.set_puzzle_value(n,True)
                else:
                    level.set_puzzle_value(n,None)
                n += 1
            level.make_list()
            i += 1    
        oldfile.close()
        
        pass
    
    def initialize(self):
       
        size = (150,250)
        x = -75
        y = 250
        
        self.initialize_levels(x,y,size)
    
        file = find_file(self.name)
    
        if type(file) == str:
            self.file = file
            self.load()
        else:
            playername = self.name.lower()
            filename = playername[0]
        
            number = str(file)
        
            for i in range(15-len(number)):
                filename += "0"
            filename += number
        
            self.file = filename
            self.save()
        
            outline = filename + " " + self.name
        
            index = open("index.txt","a")
            index.write("\n")
            index.write(outline)
            index.close()
    
    #
    # Tutorial Functions
    #

    def new_tutorial(self):
        
        self.tutorial = Tutorial()
    
    def in_tutorial(self):
        
        return self.tutorial_active
    
    def flag_tutorial(self):
        
        self.tutorial_active = True
    
    def advance_tutorial(self):
        
        if self.tutorial.advance():
            self.tutorial = None
            
        self.tutorial_active = False
    
    def get_tutorial(self):
        
        return self.tutorial
    def complete_tutorial(self):
        
        self.tutorial = False
        
    #
    # Getters and Setters
    #

    def get_result(self):
        
        return self.result
        
    def get_levels(self):
        
        return tuple(self.levels)
  
    
    def get_name(self):
        """ Return the player's name. """
        return self.name
    
    def get_level(self):
        """ Get the current level. """
        
        return self.level
        
    def get_puzzle(self):
        """ Get the current puzzle. """
        
        return self.puzzle
        
    def get_puzzle_score(self,level,puzzle):
        """ Get the score for a particular puzzle. """
        
        return self.scores[level][puzzle]
    
    def get_puzzle_stars(self,level,puzzle):
        """ Get the number of star's the player earned for the puzzle. """
         
        return self.stars[level][puzzle]
        
    def set_puzzle(self,puzzle):
        """ Set the current puzzle. """
        
        self.puzzle = puzzle
    
    def set_level(self,level):
        """ Set the current level. """
        
        self.level = level
    
    def add_level(self,level):
        
        self.levels.append(level)
    
    def clear_result(self):
        
        self.result = None
    
    def mark_win(self):
        """ Registers a win in the level list. """
        
        self.result = True
        
        self.levels[self.level - 1].set_puzzle_value(self.puzzle,True)
        self.levels[self.level - 1].make_list()
        
    def mark_loss(self):
        """ Registers that a level has been tried but not won. """
        
        self.result = False
        
        if not self.levels[self.level - 1].get_puzzle_value(self.puzzle):
            
            self.levels[self.level - 1].set_puzzle_value(self.puzzle,False)
            self.levels[self.level - 1].make_list()

    def draw(self,screen):
        
        screenprint(screen,self.name)
        current = str(self.level) + " - " + str(self.puzzle)
        screenprint(screen,current,(0,24))

class Cursor:
    """ Current position of a person's hand.  May hold a logic element. """
    
    def __init__(self,position,size,object):
        
        self.x = position[0]
        self.y = position[1]
        
        self.w = size[0]
        self.h = size[1]
        
        self.contents = object
        self.origin = object.get_position()
    
    def get_thing_from(self,other):
        """ Get the selected widget. """
        
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
    
    def get_origin(self):
        
        return tuple(self.origin)
    
    def get_position(self):
        """ Get the position of the cursor. """
        
        return (self.x,self.y)
    
    def get_center(self):
        """ Get the center of the cursor. """
        
        return (self.x + self.w // 2 , self.y + self.h // 2)
    
    def get_size(self):
        """ Get the size of the cursor. """
        
        return (self.w,self.h)
    
    def get_thing(self):
        """ Get the thing held by the cursor. """
        
        return self.contents
        
    def drop(self,spaces):
        """ Drop the object somewhere. """
        
        pass
    
    def to_origin(self):
        
        self.contents.set_position(self.origin)
        
        return self.contents
        
    def update(self,position):
        """ Change the position of the widget. """
        
        self.x = position[0] - self.w // 2
        self.y = position[1] - self.h // 2

    def draw(self,screen):
        
        self.contents.draw(screen)

class Garbage:
    """ Gets rid of stuff. """
    
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
        """ Draw the garbage pail on the screen. """
        
        dw = self.w // 2
        x0 = self.x + dw
        y0 = self.y
        
        dx = self.w // 15
        dy = self.h // 20
        
        pg.draw.rect(screen,self.color,(self.x,self.y,self.w,self.h),1)
        screenprint(screen,"TRASH",(self.x+5,self.y+self.h//3))

     

#
# FUNCTIONS
#
def move_scrollbar(scrollbar,amount):
    """ Sets up the action for a scrollbar's button object. """
    
    #
    # I don't remember why I did this this way.  It seems like there should
    # be a more direct method to accomplish this.
    #
    # I did test it to see if it is still in use on 6/19/2016, and it is.
    #
    
    def move():
        
        scrollbar.shift(amount)
    
    return move

def draw_triangle(size,direction = "Up"):
    """ Draws a triangle to decorate a button. """
    
    square = pg.Surface(size)
    square.convert()
    square.fill(GRAY)
    
    x0 = size[0] * 0.1
    y0 = size[1] * 0.1
    
    xm = size[0] // 2
    
    xr = size[0] - x0
    
    yb = size[1] - y0
    
    w = size[0] - 2 * x0
    h = size[1] - 2 * y0
    
    
    if direction == "Up":
        
        point = ( xm , y0 )
        base1 = ( x0 , yb )
        base2 = ( xr , yb )
    
    elif direction == "Down":
        
        point = ( xm , yb )
        base1 = ( x0 , y0 )
        base2 = ( xr , y0 )
        
    else:
        
        point = ( x0 , y0 )
        base1 = ( x0 , yb )
        base2 = ( xr , yb )
        
    points = (point,base1,base2)
    
    pg.draw.polygon(square,BLACK,points)
    
    return square
        
def draw_field(field,background,color = BLACK):
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
    

def shift_to_corner(pos,n):
    """ Chooses one of four corners for n; used for backgrounds. """
    
    x = pos[0]
    y = pos[1]
    
    if n // 2:
        x0 = x + 2
    else:
        x0 = x - 2
    if n % 2:
        y0 = y + 2
    else:
        y0 = y - 2

    return x0 , y0
    
def shift_cardinal(pos,n):
    """ Chooses one of four carndinal directions based on the number n,
         0 - right , 1 - down , 2 - left , 3 - up
        Shifts the position by two pixels in that direction.
        Used for backgrounds. """
    
    x = pos[0]
    y = pos[1]
    
    if n == 0:
        x0 = x + 2
        y0 = y
    elif n == 1:
        x0 = x
        y0 = y + 2
    elif n == 2:
        x0 = x - 2
        y0 = y
    elif n == 3:
        x0 = x
        y0 = y - 2
    else:
        x0 = x
        y0 = y

    return x0 , y0


def find_file(name):
    """ Parses the index to find the file name for the user _name_
        If the index.txt file has it, this returns a filename.
        If it does not, this returns a number to use for the next 
            file.
        """
        
    file = open("index.txt",'r')
    
    n = 0
    for line in file:
        n += 1
        if ord(line[-1]) == 10 and line[17:-1] == name.upper(): 
            return line[:16]
        elif line[17:] == name.upper():
            return line[:16]
    
    file.close()
    
    return n


#
# MVC CLASSES
#

class Game:
    """ Keeps track of the game and its objects. """
    
    #
    # Game states:
    #
    #   0 - Login Screen ( No player logged in )
    #   1 - Spash Screen ( No puzzle chosen )
    #   2 - Game Screen ( No result on current puzzle )
    #   3 - Result Screen ( Current puzzle with result )
    #
    
    def __init__(self,screen_size):
        
        self.name = ""
        self.player = None
        
        self.size = (900,600)
        
        self.display = pg.display.set_mode(self.size,False,32)
        
        scale = 13
        self.scale = Scales( self.size , scale )
        
        self.state = 0
        self.states = []
        self.next_state = 1
        
        self.factories = []        
        self.generate_factories()
        
        self.time = 0
        self.clock = None
        
        garbage_location = ( 30 * scale , 16 * scale )
        garbage_size = ( 3 * scale , 4 *  scale )
        self.garbage = Garbage( garbage_location , garbage_size )
        
        self.elements = []
    
    def get_name(self):
        """ Returns the name of the current player or name in the login screen 
            before a player has been created. """
            
        return self.name
    
    def get_levels(self):
        
        return self.player.get_levels()
    
    def get_player(self):
        """ Returns the player object. """
        
        return self.player
        
    def get_background(self):
        """ Gets the background of the current game screen. """
        
        return self.states[self.state].get_background()
        
    def get_display(self):
        """ Returns the game window as last rendered. """
        
        return self.display
        
    def get_screen(self,state = None):
        """ Returns a game screen. The specified game screen if state is
            filled in, otherwise it returns the current screen."""
        
        if not state:
            state = self.state
            
        return self.states[state]
    
    def set_name(self,name):
        
        self.name = name
    
    def get_state(self):
        """ Returns the current state number. """
        
        return self.state
    
    def set_state(self,state):
        """ Sets the game state to a particular screen, if it exists. """
        
        if state < len(self.states):
            self.state = state
            
    def set_next_state(self,state):
        
        self.next_state = state
        
    def mark_loss(self):
        
        self.player.mark_loss()
        self.next_state = 4
        
    def advance(self):
        """ Moves the game to the next state in the sequence. """
        
        self.state += 1
        
        if self.state >= len(self.states):
            player.clear_puzzle()
            self.state = 1
            
    def login(self):
        """ Logs a player into the game. """
        
        player = Dude(self.name)
        player.initialize()
        self.player = player
    
    def logout(self):
        """ Clears player information. """
        
        self.name = ""
        self.player = None
        self.state = 0
    
    def add_screen(self,screen = None):
        """ Creates a new screen for the game. """
        
        if type(screen) == str:
            
            screen = Screen(screen,self)
        
        self.states.append(screen)
        
    def generate_factories(self):
        """ Creates the factories for the game. """
        
        scale = self.scale.get_scale()
        
        self.factories = []
        
        x = scale * 9 
        y = scale * 17
    
        x += scale * 11
    
        self.factories.append(Factory(LogicNot,(x,y),self.scale))
    
        x += scale * 11
    
        self.factories.append(Factory(LogicOr,(x,y),self.scale))
    
        x += scale * 11
    
        self.factories.append(Factory(LogicAnd,(x,y),self.scale))
    
    def get_factories(self):
        """ Returns the factories. """
        
        return self.factories
    
    def clear_animations(self):
        """ Removes all stored animations stored in . """
    
        self.states[self.state].clear_animations()
        
    def get_animations(self):
        """ Returns the current animations. """
        
        return self.animations
        
    def reset_timer(self):
        """ Resets the game clock to zero. """
        
        self.time = 0 
        self.clock = pg.time.Clock()
    
    def advance_state(self):
        
        self.clear_animations()
        self.state = self.next_state
    
    def update(self):
        """ Updates the game objects according to the clock. """
        
        if not self.clock:
            return None
        
        bg , mg , fg = self.states[self.state].get_animations()
        
        dt = self.clock.tick(30)
        self.time += dt
        
        kill_list = []
        for animation in bg + mg + fg:
            animation.update(dt)

    def handle_events(self,events = None):
        """ Handles input for the current screen. """
        
        if not events:
            events = pg.event.get()
        
        for event in events:
            self.states[self.state].handle_events(event)
    
    def end_game(self):
        
        if self.state == 2:
            self.player.mark_loss()
        if self.state != 0:
            self.player.save()
        exit()
        
        
    def keystroke(self,stroke):
        
        if self.state == 0 and key in key_dic:
            self.name += key_dic[event.key]
        elif event.key == K_RETURN:
            self.player = Dude(self.name)
            self.player.initialize()
        elif event.key == K_BACKSPACE:
            self.name = self.name[:-1]
    
    def mousedown(self,pos):
        
        program = self.screens[self.screen].get_program()
        
        for factory in self.factories:
            
            if program != None and factory.is_clicked(pos):
                self.held = Cursor(factory.create(pos))
                self.screen[self.screen].append(cursor)
    
    def mouseup(self,pos):
        
        program = self.screens[self.screen].get_program()
        
        if program:
            
            return None
        
        if self.garbage.is_clicked():
            
            self.program.remove(self.held) 
        
        pass
    
    def resize(self,size):
        
        for screen in self.screens:
            
            screen.resize(size)
        
        self.garbage.resize(size)
        
        for factory in self.factories:
            
            factory.resize(size)
    
    def draw(self,screen):
    
        self.screen.draw(screen)
        self.cursor.draw(screen)
        
        
class Viewer:
    
    def __init__(self,size,game):
        
        self.size = size
        self.screen = pg.display.set_mode(screen_size,False,32)
    
        self.game = game
    
    def resize(self,size):
        """ Resizes the display. """
        pass
        
        self.screen = pg.display.set_mode(size,RESIZABLE,32)
        for screen in self.game.get_screens():
            self.screen.resize(size)
        game.resize(size)
    
    def draw(self):
        
        self.screen.draw(screen)
        
        pg.display.update()
    
class Controller:
    
    def __init__(self,game):
        
        self.game = game
    
    def check(self):
        
        state = self.game.get_state()
        player = self.game.get_player()
        
        events = pg.event.get()
        
        for event in events:
                
            if event.type == KEYDOWN:
                # Key input for entering names
                if state == 0:
                    game.keystroke(event.key)
            
            elif event.type == MOUSEBUTTONDOWN:
                check_pos = pg.mouse.get_pos()
                game.mousedown(check_pos)
            
            elif event.type == MOUSEBUTTONUP:
                check_pos = pg.mouse.get_pos()
                game.mouseup(check_pos)
            
            elif event.type == VIDEORESIZE:
                # Resizes screen 
                new_size = event.size
                self.screen.resize(new_size)
        
            if event.type == QUIT:
                if state == 2:
                    # If game is being played, mark as tried.
                    player.mark_loss()
                    player.save()
                exit()
        
    
        

# 
# MVC FUNCTIONS
#

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
    
    screen.blit(background,(0,0))
    
    #
    # Draw all objects below.
    #
    
    for thing in things:
        thing.draw(screen)
    
    avatar.draw(screen)

    out = str(pg.mouse.get_pos())
    
    screenprint(screen,out,(5,575))
    
    if avatar.in_tutorial():
        avatar.get_tutorial().display_current(screen)
    
    #
    # Draw all objects aibove.
    #
        
    pg.display.update()
    
    pass
    
#
# SCREENS
#

def login_init(background):
    
    screen_size = background.get_size()
    x = screen_size[0] // 2 - 50
    y = screen_size[1] // 4
    screenprint(background,"Logic Lights",(x,y),36,YELLOW)
    version = make_label("Logic Lights Version "+VERSION,12)
    pos = screen_size[0] - version.get_size()[0] , screen_size[1] - version.get_size()[1]
    background.blit(version,pos)
    

def login(game):
    """ Creates the login screen. """
    
    game.logout()
    
    middle = game.get_screen()
    game.set_next_state(1)
    
    while game.get_state() == 0 :
        middle.draw()
        game.handle_events()
    
    game.login()
        
def win(game):
    """ Creates the winning screen. """
    
    screen = game.get_display()
    middle = game.get_screen()
    middle.set_background(screen)
    game.set_next_state(1)
    
    game.reset_timer()
    while game.get_state() == 3:
        game.update()
        middle.draw()
        game.handle_events()

def retire(game):
    """ Creates the winning screen. """
     
    screen = game.get_display()
    middle = game.get_screen()
    middle.set_background(screen)
    game.set_next_state(1)

    while game.get_state() == 4:
        middle.draw()
        game.handle_events()

def selection(game):
    """ Controls the spash page. """
    
    game.set_next_state(2)
    middle = game.get_screen()
    
    while game.get_state() == 1:

        middle.draw()
        game.handle_events()

def game(game):
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
    
    game.set_state(2)
    middle = game.get_screen()
    screen = game.get_display()
    player = game.get_player()
    screen_size = screen.get_size()
    background = middle.get_background()
    
    clock = pg.time.Clock()
    
    #
    # Initialize game objects and loop variables
    #
    
    player.clear_result()
    
    
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
    
    level = player.get_level()
        
    choice = player.get_puzzle()
    
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
    
    #
    #
    #

##     col = [YELLOW,DARK_GRAY,GRAY]
##     
    x = 50
    y = area_corner[1]
    
    buttons = []
    
    for n in range(level):
        y += area_size[1] // (level + 1)
        
        letter = chr(65 + n)
        button = LogicSwitch(letter)
        button.set_position((x,y))
        
        buttons.append(button)
        
    program1 = create_truth_table(buttons,choice)
    
    x = 850
    y = 250 - 3 * sc
    
    light1 = LogicLight()
    light1.static_program(program1)
    
    light1.set_position((x,y))
    
    lights = [light1]
    
    cursor = None
    
    do_update = True
    
    program = []
    #
    # Main loop for MVC game control.
    # 
    while player.get_result() == None:
        #
        # Update the time at the beginning of the loop.
        #
    
        interval = clock.tick(30)
        
        #
        # View: Draw all objects
        ## Send objects to the view function.
        #
        
        things = factories + buttons + program + lights + wires + [garbage] + list(middle.get_buttons())
        view(screen,background,player,things)
        
        #
        # Control: Take input from the user.
        ## Provide control of game state in the event loop.
        ## Call the control() function to control the avatar.
        #
        
        if cursor:
            
            cursor.set_position(pg.mouse.get_pos())
             
        events = pg.event.get()
        game.handle_events(events)
        check_pos = pg.mouse.get_pos() 
        for event in events:
            if event.type == MOUSEBUTTONDOWN: 
                
                for button in middle.get_buttons():
                    
                    if button.is_clicked(check_pos):
                    
                        button.activate()
                        game.set_next_state(4)
                
                for object in buttons:
                    
                    if object.is_clicked(check_pos):
                        object.toggle()
                        do_update = True
                        
                for thing in program:
                    
                    if thing.is_clicked(check_pos):
                        
                        cursor = thing 
                        return_space = check_pos
                
                if player.in_tutorial():
                    
                    if player.get_tutorial().is_clicked(check_pos):
                        
                        player.get_tutorial().advance_message()
                        
                found = False
                
                for wire in wires:
                    
                    for clasp in list(wire.get_clasps()):
                        
                        if not found and clasp.is_clicked(check_pos):
                            
                            cursor = wire.remove_clasp(clasp)
                            return_space = clasp
                            found = True
                
                for wire in wires:
                    
                    if not found and wire.is_clicked(check_pos):
                        
                        cursor = wire.get_segment(check_pos)
                        segments = wire.get_segments()
                        if cursor in (segments[0],segments[-1]):
                            wire.append_segment(cursor)
                
                for thing in buttons + lights + program:
                    
                    for pad in thing.get_pads():
                        
                        if pad.is_clicked(check_pos):
                            
                            if pad.get_connector():
                                
                                cursor = pad.disconnect()
                                return_space = pad
                                
                            else:
                            
                                cursor = LogicWire(pad)
                                cursor.set_position(check_pos)
                                pad.set_connector(cursor)
                                wires.append(cursor)
                                return_space = None

                for factory in factories:
                    
                    if factory.is_clicked(check_pos):
                        
                        cursor = factory.create(check_pos)
                        program.append(cursor)
                        return_space = None
                
            if event.type == MOUSEBUTTONUP:
                
                do_update = True
                
                if cursor and not cursor.gate_type():
                    cursor = None
                elif cursor:
                    
                    #
                    # Toss it in the garbage?
                    #
                    
                    in_garbage = garbage.is_clicked(check_pos)
                    
                    #
                    # Return to a  factory?
                    #
                    
                    for factory in factories:
                        
                        test1 = factory.is_clicked(check_pos)
                        
                        test2 = cursor.gate_type() == factory.gate_type()
                        
                        if test1 and test2:
                        
                            program.remove(cursor)
                            cursor.desolder(wires) 
                    
                    #
                    # 
                    #
                    
                    obj_pos = cursor.get_position()
                    obj_siz = cursor.get_size()
                    
                    
                    x1 = obj_pos[0] - area_corner[0]
                    y1 = obj_pos[1] - area_corner[1] 
                    
                    test_x = 0 < x1 < area_size[0] - obj_siz[0] 
                    test_y = 0 < y1 < area_size[1] - obj_siz[1] 
                    
                    #
                    # Is it placed in play?
                    #
                    
                    if not ( test_x and test_y ) and not in_garbage:
                        
                        if return_space:
                            
                            cursor.set_position(return_space)
                            
                        else: 
                            
                            if cursor in program:
                                program.remove(cursor)
                    
                    # Is the cursor a wire?
                    if cursor.get_type() == "Wire":
                        
                        found = False
                        
                        # Delete a wire placed in the trash.
                        if in_garbage:
                        
                            return_space = None
                            cursor.deregister()
                            wires.remove(cursor)
                            found = True
                         
                        # Delete a wire with both ends at the same terminal.    
                        elif cursor.get_pads():
                            
                            for pad in cursor.get_pads():
                                
                                if pad.is_clicked(check_pos):
                                
                                    cursor.deregister()
                                    wires.remove(cursor)
                                    
                                    found = True
                                    
                        if not found:
                            
                            # Connect a wire to a logic element's terminal.
                            for item in buttons + lights + program:
                            
                                for pad in item.get_pads():
                                
                                    clicked = pad.is_clicked(check_pos)
                                
                                    wired = pad.is_wired()
                                
                                    is_input = pad.get_type() == "Input"
                                
                                    if clicked and not ( wired and is_input ):
                                    
                                        if cursor.connect(pad):
                                            cursor.force_update()
                                            found = True
                            
                            # Attach a probe to a wire and an output wire to
                            # the probe.
                            if not found and not cursor.get_input():
                                
                                for wire in wires:
                                    
                                    is_self = wire == cursor
                                    clicked = wire.is_clicked(check_pos)
                                    
                                    if clicked and not is_self:

                                        clasp = wire.add_clasp(check_pos)
                                        cursor.connect(clasp)
                                        found = True
                        
                        if not found:
                            
                            if return_space:
                                
                                cursor.connect(return_space)
                                cursor.set_position(return_space.get_position())
                                if return_space.is_clasp():
                                    return_space.get_owner().append_clasp(return_space)     

                            else:
                                
                                cursor.deregister()
                                if cursor in wires:
                                    wires.remove(cursor)
                    
                    # The cursor is a logic element. 
                    else:

                        placed = []
                        
                        # Delete an element?
                        if in_garbage:
                            
                            cursor.desolder(wires) 
                            program.remove(cursor)
                    
                        # Direct connection between two elements?
                        for thing in buttons + lights + program:
                            
                            for pad1 in cursor.get_pads():
                                    
                                for pad2 in thing.get_pads():
                                        
                                    type1 = pad1.get_type()
                                    type2 = pad2.get_type()
                                    
                                    pos1 = pad1.get_position()
                                    pos2 = pad2.get_position()
                                    
                                    check1 = pad1.is_clicked(pos2)
                                    check2 = pad2.is_clicked(pos1)
                                    
                                    checkA = type1 != type2
                                    
                                    checkB = type1 == "Input"
                                    checkB = not(checkB and pad1.is_wired())
                                    
                                    checkC = type1 == "Input"
                                    checkC = not(checkC and pad1.is_wired())
                                    
                                    available = checkA and checkB and checkC
                                    
                                    if ( check1 or check2 ) and available:
                                        
                                        placed.append((pad1,pad2))
                                
                                
                        for pair in placed:
                        
                            pad1 , pad2 = pair
                        
                            new_wire = LogicWire(pad1)
                            new_wire.connect(pad2)
                            pad1.set_connector(new_wire)
                            wires.append(new_wire)
                            new_wire.initial_segments()
                                
                            new_wire = None
                        
                        if not placed:
                            
                            cursor.set_position(check_pos)
                        
                        else:
                            
                            cursor.reset_pads()
                        
                    return_space = None
                    cursor = None
                        
        
        if do_update:
            for light in lights:
                win = light.evaluate(buttons)
                if win:
                    player.mark_win()
                    if player.in_tutorial():
                        player.advance_tutorial()
                    game.set_next_state(3)
            do_update = False

    game.advance_state()
    
    things = factories + buttons + program + lights + wires + [garbage]
    view(screen,background,player,things)
    player.save()

    return win


def setup(game):
    """ Sets up the game screens. """
    
    #
    # Initialize screen and clock
    #
    
    screen_size = game.get_display().get_size()
    
    x = screen_size[0] // 2 - 50
    y = screen_size[1] // 4
    x0 = x - 100
    y0 = y + 150
    
    #
    # Create Buttons
    #
    
    halt_size = (300,30)
    halt_pos = (325,400)
    halt_msg = "Press Any Key to Continue"
    halt_button = Button(halt_size,halt_pos,game)
    halt_button.set_action(game.advance_state)
    halt_button.set_interior(BLACK)
    halt_button.set_border(WHITE)
    halt_button.set_ornament(centered(make_label(halt_msg),halt_size))
    
    button_size = (75,30)
    retire_pos = (0,525)
    retire_button = Button(button_size,(0,525))
    retire_button.set_action(game.mark_loss)
    retire_button.set_interior(BLACK)
    retire_button.set_border(WHITE)
    retire_button.set_ornament(centered(make_label("Retire"),button_size))
    
    logout_pos = (825,0)
    logout_button = Button(button_size,logout_pos,game)
    logout_button.set_action(game.logout)
    logout_button.set_interior(BLACK)
    logout_button.set_border(WHITE)
    logout_button.set_ornament(centered(make_label("Logout"),button_size))
    
    quit_decoration = Quit(game.end_game)
    
    #
    # Set Up the Game Object
    #
    
    screen = game.get_display()
    
    game.add_screen("login")
    game.get_screen(0).set_init(login_init)
    game.get_screen(0).initialize_background()
    game.get_screen(0).add_label(Message((x0,y0),"Enter Your Name:",game.get_name))
    game.get_screen(0).get_label(0).set_size(24)
    game.get_screen(0).add_input(quit_decoration)
    game.get_screen(0).add_input(SingleKey({K_RETURN:game.advance_state}))
    game.get_screen(0).add_input(KeyboardInput(game))

    
    game.add_screen("selection")
    splash_bg = game.get_screen(1).get_background()
    screenprint(splash_bg,"Logic Lights",(x,y),36,YELLOW)
    game.get_screen(1).add_button(logout_button)
    game.get_screen(1).add_input(quit_decoration)
    game.get_screen(1).activate_levels()

    
    game.add_screen("game")
    game.get_screen(2).add_button(retire_button)
    game.get_screen(2).add_input(quit_decoration)

    game.add_screen("win")
    game.get_screen(3).animations.append(WingdingContainer(Wingding,None,game.get_screen(3)))
    win_fg = game.get_screen(3).get_foreground()        
    for n in range(4):
            x0 , y0 = shift_to_corner((x,y),n)
            screenprint(win_fg,"Logic Lights",(x0,y0),36,BLACK)
            x0 , y0 = shift_cardinal((x,y),n)
            screenprint(win_fg,"Logic Lights",(x0,y0),36,BLACK)
    screenprint(win_fg,"Logic Lights",(x,y),36,BLACK)
    game.get_screen(3).fg_animations.append(FadeIn("Logic Lights",(x,y),36,YELLOW))
    x1 = x + 12
    y1 = y + 150
    for n in range(4):
        x0 , y0 = shift_to_corner((x1,y1),n)
        screenprint(win_fg,"You Win!",(x0,y0),36,BLACK)
        x0 , y0 = shift_cardinal((x1,y1),n)
        screenprint(win_fg,"You Win!",(x0,y0),36,BLACK)
    screenprint(win_fg,"You Win!",(x1,y1),36,BLACK)
    game.get_screen(3).fg_animations.append(FadeIn("You Win!",(x1,y1),36,WHITE))
    game.get_screen(3).add_button(halt_button)
    game.get_screen(3).add_input(AnyKey(game.advance_state))
    game.get_screen(3).add_input(quit_decoration)

    game.add_screen("retire")
    retire_fg = game.get_screen(4).get_foreground()
    for n in range(4):
            x0 , y0 = shift_to_corner((x,y),n)
            screenprint(retire_fg,"Logic Lights",(x0,y0),36,BLACK)
            x0 , y0 = shift_cardinal((x,y),n)
            screenprint(retire_fg,"Logic Lights",(x0,y0),36,BLACK)
    screenprint(retire_fg,"Logic Lights",(x,y),36,YELLOW)
    x1 += 20
    for n in range(4):
        x0 , y0 = shift_to_corner((x1,y1),n)
        screenprint(retire_fg,"Retired",(x0,y0),36,BLACK)
        x0 , y0 = shift_cardinal((x1,y1),n)
        screenprint(retire_fg,"Retired",(x0,y0),36,BLACK)
    screenprint(retire_fg,"Retired",(x1,y1),36,WHITE)
    game.get_screen(4).add_button(halt_button)
    game.get_screen(4).add_input(AnyKey(game.advance_state))
    game.get_screen(4).add_input(quit_decoration)
    
    result = True
    

def main():
    
    ''' Function that controls the program state.'''    
    
    screen_size = (900,600)
    
    central = Game(screen_size)
    
    setup(central)
    
    central.set_state(0)
    while True:
        
        if central.get_state() == 0:
            
            login(central)
        
        else:
        
            game(central)

            if central.get_state() == 3:
                win(central) 
            else:
                retire(central)
                
        selection(central)

#
# START UP
#

pg.init()
main()

