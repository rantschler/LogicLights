import pygame as pg
from LogicLogic import *

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


COLOR1 = GRAY
COLOR2 = DARK_GRAY
COLOR3 = GRAY
LIGHT_ON = YELLOW
LIGHT_OFF = DARK_GRAY

LETTER_ON = BLACK
LETTER_OFF = BLACK

## COLOR1 = GREEN
## COLOR2 = BLACK
## COLOR3 = GREEN

## LIGHT_ON = YELLOW
## LIGHT_OFF = BLACK

## LETTER_ON = BLACK
## LETTER_OFF = WHITE

class Segment:
    """ Creates a horizontal or vertical segment of wire. 
        This is always a part of a LogicWire element and is used to 
            make a more manipulable wire with an arbitrary number of
            wire segments.
    """
    
    def __init__(self,wire,posA,posB,horizontal = None):
        """ Initializes the segment. """
        
        self.start = None
        self.end = None
        self.start_pos = list(posA)
        self.end_pos   = list(posB)
        
        self.owner = wire
        
        if horizontal == None:
            self.horizontal = self.check_horizontal()
        else:
            self.horizontal = horizontal
            
        self.color = COLOR3
    
    def gate_type(self):
        
        return None
        
    def is_horizontal(self):
        """ Returns True for a horizontal wire segment. """
        
        return self.horizontal
            
    def check_horizontal(self):
        """ Checks to see if the wire segment is horizontal or vertical. """
        
        if self.start_pos[1] == self.end_pos[1]:
            return True
        else:
            return False
    
    def is_clicked(self,pos,sense):
        """ Checks to see if the wire segment has been clicked. """
        
        if self.is_horizontal():
            t1 = min( self.start_pos[0] , self.end_pos[0] )
            t2 = max( self.start_pos[0] , self.end_pos[0] )
            testH = t1 < pos[0] < t2
            testV = -sense < pos[1] - self.start_pos[1] < sense
        else:
            t1 = min( self.start_pos[1] , self.end_pos[1] )
            t2 = max( self.start_pos[1] , self.end_pos[1] )
            testH = -sense < pos[0] - self.start_pos[0] < sense
            testV = t1 < pos[1] < t2
        
        if testH and testV:
            return True
        else:
            return False
    
    def get_location(self,length):
        """ Returns the point along the wire a distance _length_ from 
            the starting position of the wire.
        """
        
        if self.is_horizontal():
            dx = self.end_pos[0] - self.start_pos[0]
            if dx != 0:
                sign =int(float( dx )/ abs(dx))
            else: 
                sign = 0
            nx = self.start_pos[0] + sign * length
            ny = self.start_pos[1]
        else:
            dy = self.end_pos[1] - self.start_pos[1]
            if dy != 0:
                sign = int(float( dy ) / abs(dy))
            else:
                sign = 0
            nx = self.start_pos[0]
            ny = self.start_pos[1] + sign * length
            
        
        return [ nx , ny ]
        
    def set_starting_position(self,pos):
        """ Sets the starting position of the segment and keeps its
            direction constant.
        """ 
        
        horaz = self.is_horizontal()
        
        self.start_pos = list(pos)
        if horaz:
            self.end_pos[1] = pos[1]
        else:
            self.end_pos[0] = pos[0]
    
    def set_ending_position(self,pos):
        """ Sets the ending position of the segment and keeps its
            direction constant.
        """ 
        
        horaz = self.is_horizontal()
        
        self.end_pos = list(pos)
        if horaz:
            self.start_pos[1] = pos[1]
        else:
            self.start_pos[0] = pos[0]
    
    def get_starting_position(self):
        
        return list(self.start_pos)
    
    def get_ending_position(self):
        
        return list(self.end_pos)
    
    def get_ends(self):
        
        return list(self.start_pos) , list(self.end_pos)
    
    def set_position(self,pos):
        """ Moves the wire segment when it is the cursor. 
            The wire segment should move horizontally or vertically,
                but not both.
        """
        
        if self.is_horizontal():
            self.start_pos[1] = pos[1]
            self.end_pos[1] = pos[1]
        else:
            self.start_pos[0] = pos[0]
            self.end_pos[0] = pos[0]
        
        if self.start:
            self.start.set_ending_position(self.start_pos)
        if self.end:
            self.end.set_starting_position(self.end_pos)
        
        self.owner.update_clasps()
    
    def set_start(self,segment):
        
        self.start = segment
    
    def set_end(self,segment):
        
        self.end = segment
    
    def get_length(self):
        
        lx = self.end_pos[0] - self.start_pos[0]
        ly = self.end_pos[1] - self.start_pos[1]
        
        return abs(lx) + abs(ly)
    
    def get_distance(self,pos):
        
        if self.is_horizontal():
            return abs(pos[0] - self.start_pos[0])
        else:
            return abs(pos[1] - self.start_pos[1])
    
    def draw_light(self,screen):
        
        start = ( int(self.start_pos[0]) , int(self.start_pos[1]) )
        end   = ( int(self.end_pos[0])   , int(self.end_pos[1])   )
        
        pg.draw.line( screen, self.color , start, end , 3 )
    
    def draw_dark(self,screen):
        
        start = ( int(self.start_pos[0]) , int(self.start_pos[1]) )
        end   = ( int(self.end_pos[0])   , int(self.end_pos[1])   )
        
        pg.draw.line( screen, BLACK ,      start, end , 5 )
        
    

class Pad:
    """ Terminal object that connects a logic gate to a wire. """
    
    def __init__(self,element,position,type = "Output"):
        """ Initializes the terminal. """
        
        self.x = position[0]
        self.y = position[1]
        
        self.container = element
        
        if type == "Output":
            self.connector = []
        else:
            self.connector = None
        
        self.color = COLOR3
        
        self.type = type
        
        self.r = 6
    
    def set_connector(self,connector):
        """ Connects a wire to the pad. """
        
        if self.type == "Output":
            self.connector.append(connector)
        else:
            self.connector = connector
    
    def get_position(self):
        
        return ( self.x , self.y )
    
    def get_owner(self):
        """ Returns the logic element that owns the terminal. """
        
        return self.container
    
    def get_connector(self):
        """ Returns the wire connected to the pad.  """
        
        if self.type == "Output":
            
            if self.connector:
                
                return self.connector[0]
            
            else:
                
                return None
        
        return self.connector
        
    def get_type(self):
        """ Returns the type of the pad: 'Input' or 'Output'. """
        
        return self.type
    
    def program(self):
        """ Manages the behavior of the pad during the programming chain
            that turns a wiring diagram into a logical statement. """
            
        if self.type == "Input" and self.connector:
            
            return self.connector.program()
        
        elif self.type == "Output":
            
            return self.container.program()
        
        else:

            return None
    
    def disconnect(self,connected = None):
        """ Remove the wire from the terminal, returns the wire. """
        
        if self.type == "Output":
            
            if connected:
                wire = connected
            else:
                wire = self.connector[0]
            
            self.connector.remove(wire)
        
        else:
            wire = self.connector
            self.connector = None
        wire.disconnect(self)

        return wire
        
    def is_clasp(self):
        return False
        
    def is_clicked(self,pos):
        """ Checks to see if the pad has been clicked. """
        
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        
        return dx * dx + dy * dy < self.r * 8
        
    def is_wired(self):
        """ Checks to see if the pad is already connected to a wire. """
        
        if self.connector:
            
            return True
        
        else:
            
            return False

    def evaluate(self):
        """ Passes the pad through the evaluation chain. """
        
        if not self.connector:
            
            return None
        
        if self.type == "Input":
            
            value = self.connector.evaluate()
        
        else:
            
            value = self.container.evaluate()
            
        return value

    def get_value(self):
        """ Passes the pad through the evaluation chain. """
        
        if self.type == "Input":
            
            if self.connector:
            
                value = self.connector.get_value()
            
            else: 
                
                value = None
        
        else:
            
            value = self.container.get_value()
            
        return value
    
    def set_position(self,position):
        """ Sets the screen position of the pads for drawing. """
        
        self.x = position[0]
        self.y = position[1]
        
        
        if self.connector:
            if self.get_type() == "Output":
                for connector in self.connector:
                    connector.update_input()
            else:
                self.connector.update_output()
        
    def get_position(self):
        """ Returns the screen position of the terminal. """
        
        return ( self.x , self.y )

    def draw(self,screen):
        """ Draws the pad, open if unconnected or closed when connnected. """
        if self.connector:
            
            pg.draw.circle(screen,self.color,(self.x,self.y),self.r)
            
        else:
            
            pg.draw.circle(screen,self.color,(self.x,self.y),self.r)
            pg.draw.circle(screen,BLACK,(self.x,self.y),self.r // 2)


class LogicClasp(Pad):
    
    def __init__(self,wire,position,type = "Output"):
        """ Initializes the clasp.
            Takes a LogicWire object as self.container.
            Clasps are probes and so are always outputs.
        """
        
        
        self.pos = position 
        self.x = 0
        self.y = 0
        
        # self.container - wire the clasp probes.
        # self.connector - wires coming out of the clamp.
        
        self.container = wire
        
        self.connector = []
        
        self.set_position(position)
        
        self.color = COLOR3
        
        self.type = "Output"
        
        
        self.r = 6
    
    def connect(self,wire):
        
        self.connector.append(wire)
        
    def is_clasp(self):
        return True
        
    def set_position(self,position = None):
        
        if not self.pos:
            
            pos = position
        
        else:
            
            pos = self.pos
        
        self.x , self.y = self.container.get_relative_position(pos)
        
        for connector in self.connector:
            connector.force_update()
    
    def reset_wires(self):
        
        for connector in self.connector:
            connector.update_input()
            
    def disconnect(self,connected = None):
        """ Remove the wire from the terminal, returns the wire. """
        
        if connected:
            wire = connected
        else:
            wire = self.connector[0]
        
        
        
        self.connector.remove(wire)
        wire.disconnect(self)
        
        self.container.remove_clasp(self)

        return self.container
        
    def acquire_wire(self):
        """ Returns one wire connected to the clasp, deleting it. """
        wire = None
        
        if self.connector:
            wire = self.connector[0]
            wire.disconnect(self)
        
        return wire 
    
    def delete(self):
        
        more_wires = list(self.connector)
        for wire in self.connector:
            more_wires += wire.deregister()
        return more_wires
    
    def draw(self,screen):
        """ Draws the clasp, which looks like a connected pad. """
        
        self.x , self.y = self.container.get_relative_position(self.pos)
        
        pg.draw.circle(screen,self.color,(self.x,self.y),self.r)
        
class LogicElement:
    """ Overarching parent class for all logic gates, buttons, and wires. """
    
    def __init__(self):
         
        self.container = None
        
        self.input = None
        
        self.output = None
        
        self.pads = []
        
        self.value = None
        
        self.locked = True
        
        self.replacement = None
        
        self.symbol = None
        
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
    
    def get_position(self):
        
        return ( self.x , self.y )
    
    def get_type(self):
        """ Returns the type of logic gate. Should be overwritten. """
        
        return "Element"
    
    def gate_type(self):
        
        return "Generic"
    
    def get_pads(self):
        """ Returns the input and output terminals of the element in a tuple.
            Doesn't usually need to be overwritten.
        """
        return tuple(self.pads)
        
    def get_value(self):
        """ Returns the value found in the last evaluation of the element. 
            Usually doesn't need to be overwritten.
        """
        
        return self.value
        
    def get_pads(self):
        """ Returns all the device's pads. Should not be overwritten. """
        
        return tuple(self.pads)
    
    def get_size(self):
        
        return (self.w,self.h)
    
    def set_replacement(self,Class):
        """ Sets the replacement class for the device's programming mode. """
        
        self.replacement = Class
    
    def program(self):
        """ Default programming behavior for a device: passthrough. 
            Needs to be overwritten for most devices. 
        """

        if self.input:
            
            return self.input.program()
        
        else:
            
            return None
            
    
    def is_clicked(self,pos):
        """ Checks if the button has been pressed.
            Returns True if mouse is in field of the button
                and the button is active.
            Returns False if the mouse is not in the field or
                the button is not active. """
        
        position = (self.x,self.y)
        size = (self.w,self.h)
        center = (self.x + self.w//2, self.y + self.h//2)
        
        clicked = False
        
        x , y = position
        w , h = size
        
        w //= 9
        x += w * 2 
        w *= 5
        
        in_x = 0 < pos[0] - x < w
        in_y = 0 < pos[1] - y < h
        
        clicked = in_x and in_y
        
        return clicked
    
    def set_position(self,pos):
        """ Sets the position of the device's upper left hand corner. 
            This usually should not be overwritten.
        """
        
        self.x = pos[0] - self.w // 2
        self.y = pos[1] - self.h // 2
        
        self.reset_pads()
    
    def evaluate(self):
        """ Evaluates the value of the device in the """ 
        
        return None
        
    def is_locked(self):
        """ Chekcs to see if the device is locked in place.  Probably shouldn't
            be overwritten.
        """
        
        return self.locked
    
    def lock(self):
        """ Locks the object so that it cannot be moved.  Probably shouldn't
            be overwritten.
        """
        
        self.locked = True
    
    def unlock(self):
        """ Unlocks the object so that it can be moved.  Probably shouldn't
            be overwritten.
        """
        
        self.locked = False
        
    def reset_pads(self):
        """ Resets the pads.  Needs to be overwritten. """
        
        pass
        
    def desolder(self,wire_list):
        """ Resets the pads, deleting all connected wires. """
        
        wires = []
        for pad in list(self.get_pads()):
            wire = pad.get_connector()
            if wire:
                wires += [wire]
                wires += wire.deregister()
        wires = list(set(wires))
        for wire in wires:
            wire_list.remove(wire)
        
            
    def get_position(self):
        """ Gets the screen position of the logic element. Probably shouldn't
            be overwritten.
        """
        
        return self.x,self.y
        
    def add_drawing(self,surface):
        """ Sets the shape to use when drawing the element to the screen. """
        
        self.symbol = surface
        
        self.w , self.h =  surface.get_size() 
        
    def draw(self,screen):
        """ Draws the element and its terminals on the screen. """
        
        if self.symbol:
            
            screen.blit(self.symbol,(self.x,self.y))
            
            for pad in self.pads:
                
                pad.draw(screen)
    
class LogicWire(LogicElement):
    """ A wire that connects devices together. """
    
    def __init__(self,node = None):
        
        self.container   = None
        self.replacement = None
        self.clasps      = []
        
        if node and node.get_type() == "Output":
        
            self.input  = node
            self.output = None
        
        elif node and node.get_type() == "Input":
            
            self.input  = None
            self.output = node
        
        
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        
        self.initial_segments()
        
        self.center = 0.5
        
        self.color = COLOR3
        
        self.sensitivity = 5
        
        self.locked = False
        
    def get_type(self):
        """ Returns the type of the logic element. """
        
        return "Wire" 
    
    def gate_type(self):
        
        return "Wire"
    
    def get_clasps(self):
        
        return tuple(self.clasps)
    
    def remove_clasp(self,clasp):
        
        wire = None
        
        if clasp in self.clasps:
            
            wire = clasp.acquire_wire()
            self.clasps.remove(clasp)
        
        return wire
        
    def append_clasp(self,clasp):
        
        if not clasp in self.clasps:
            self.clasps.append(clasp)
            self.update_clasps()
            
    def add_clasp(self,pos):
        """ Adds a probe to the wire so that another wire can be connected
            to it.
        """
        
        length = self.get_length()
        segment = self.get_segment(pos)
        i = 0
        abs_pos = 0
        while i < len(self.segments) - 1 and self.segments[i] != segment:
            abs_pos += self.segments[i].get_length()
            i += 1
        
        abs_pos += self.segments[i].get_distance(pos)
        
        spot = float(abs_pos) / length
            
        new_clasp = LogicClasp(self,spot)
        
        self.clasps.append(new_clasp)
        
        return new_clasp

    def get_pads(self):
        """ Returns the device terminals that the wire is connected to. """
        
        pads = []
        
        if self.input:
            
            pads.append(self.input)
        
        if self.output:
            
            pads.append(self.output)
        
        pads += self.clasps
        
        return tuple(pads)
    
    def get_input(self):
        
        return self.input
        
    def deregister(self):
        """ Completely disconnects the wire from both terminals. """
        
        connected = []
        
        if self.input:  
            self.input.disconnect(self)
        self.input = None
        if self.output:
            self.output.disconnect()
        self.output = None
        for clasp in list(self.clasps):
            connected += clasp.delete()
        self.clasps = []
        
        return connected
    
    def get_length(self):
        """ Calculates the lengthof the wire by evaluating its component 
            segments. 
        """
        
        length = 0
        for segment in self.segments:
            length += segment.get_length()
        
        return length    
    
    def get_relative_position(self,spot):
        """ Finds the location of a point on the wire as a percentage
            of its length.
        """
        
        length = self.get_length()
        position = int(spot * float(length))
        
        i = 0
        check_A = True
        check_B = position > self.segments[0].get_length()
        while  check_A and check_B:
            position -= self.segments[i].get_length()
            i += 1
            check_A = i < len(self.segments) - 1
            check_B = position > self.segments[i].get_length()
            
        return self.segments[i].get_location(position)

    def update_clasps(self):
        
        for clasp in self.clasps:
            clasp.set_position()

    def get_segment(self,pos):
        """ Gets a segment that has been clicked so that it can be used
            elsewhere. 
        """
        
        segments = list(self.segments)
        for segment in segments:
            if segment.is_clicked(pos,self.sensitivity):
                return segment
        
        return None
    
    def get_segments(self):
        
        return list(self.segments)

    def append_segment(self,segment):
        """ Adds a segment to the end of the wire when moving one of the end
            segments. """
            
        if segment == self.segments[0]:
            
            if self.input:
                pos1 = self.input.get_position()
            else:
                pos1 = (self.x,self.y)
                
            pos2 = segment.get_starting_position()
            horaz = not segment.is_horizontal()
            
            new_segment = Segment(self,pos1,pos2,horaz)
            
            segment.set_start(new_segment)
            new_segment.set_end(segment)
            
            self.segments = [new_segment] + self.segments
        
        elif segment == self.segments[-1]:
            
            pos1 = segment.get_ending_position()
            pos2 = self.output.get_position()
            horaz = not segment.is_horizontal()
            
            new_segment = Segment(self,pos1,pos2,horaz)
            
            new_segment.set_start(segment)
            segment.set_end(new_segment)
            
            self.segments =  self.segments + [new_segment] 
            

    def is_clicked(self,pos):
        """ Check to see if the wire is clicked. """
        
        for segment in self.segments:
            if segment.is_clicked(pos,self.sensitivity):
                return True
            
        return False
    
    def reset_pads(self):
        
        if not self.input:
            
            self.segments[0].set_starting_position((self.x,self.y))
        
        elif not self.output:
            
            self.segments[-1].set_ending_position((self.x,self.y))
        
        for clasp in self.clasps:
            clasp.reset_wires()
            
        self.initial_segments()
    
    def force_update(self):
        
        self.update_input()
        self.update_output()
    
    def update_input(self):
        
        self.segments[0].set_position(self.input.get_position())
        self.segments[0].set_starting_position(self.input.get_position())
        
    def update_output(self):
        
        self.segments[-1].set_position(self.output.get_position())
        self.segments[-1].set_ending_position(self.output.get_position())
        
        self.update_clasps()
    
    def evaluate(self):
        """ Passes the input state to the output state in the evaluation
            chain.
        """
        
        if self.input:
            
            return self.input.evaluate()
        
        else:
            
            return None  
            
    def connect(self,node):
        """ Connects the wire to the node (device terminal) if it can. 
            Returns True if connection is viable, False if it is not.
        """
        
        #
        # Only connects the input of the wire to an output terminal,
        #      ... or vice-versa.
        #
        # Does not allow connections between the same object. 
        #
        
        node_type = node.get_type() == "Output" 
        
        if not self.input and node_type:
            
            if self.output.get_owner() == node.get_owner():
                
                return False
            
            self.input = node
            node.set_connector(self)
        
        elif not self.output and not node_type:
            
            if self.input.get_owner() == node.get_owner():
                
                return False
            
            self.output = node
            node.set_connector(self)
        
        elif not self.input and node.is_clasp():
            
            self.input = node
            node.set_connector(self)
        
        else:
            
            return False
        
        return True
    
    def disconnect(self,node):
        """ Disconnects the terminal from the wire.  """
        
        if node == self.input:
            
            self.input = None
        
        else:
            
            self.output = None
    
    
    def get_endpoints(self):
        """ Finds the endpoints fo the wire. """
        
        if self.input:
                
            pos_A = self.input.get_position()
            
        else:
                
            pos_A = ( self.x , self.y )
            
        if self.output:
                
            pos_B = self.output.get_position()
                
        else:
                
            pos_B = ( self.x , self.y )
        
        return pos_A , pos_B
        
    def initial_segments(self):
        
        posA , posZ = self.get_endpoints()
           
        if self.input:
            
            posM = (posZ[0],posA[1])
            first_horaz = True
        
        else:
            
            posM = (posA[0],posZ[1])
            first_horaz = False
        
        segmentA = Segment(self,posA,posM,first_horaz)
        segmentZ = Segment(self,posM,posZ,not first_horaz)
        
        segmentA.set_end(segmentZ)
        segmentZ.set_start(segmentA)
        
        self.segments = [segmentA,segmentZ]
        
    def draw(self,screen):
        
        for segment in self.segments:
            segment.draw_dark(screen)
        
        for segment in self.segments:
            segment.draw_light(screen)
            
        for clasp in self.clasps:
            clasp.draw(screen)
    
class LogicNot(LogicElement):
    """ A two terminal Not gate. """
    
    def __init__(self):
        
        self.container = None
        
        self.input = Pad(self,(-20,-20),"Input")
        
        self.output = Pad(self,(-20,-20),"Output")
        
        self.pads = (self.input,self.output)
        
        self.value = None  
        
        self.locked = False
        
        self.symbol = draw_not()
        
        self.x = 0
        self.y = 0
        self.w , self.h = self.symbol.get_size()
        
    def gate_type(self):
        
        return "Not"
    
    def reset_pads(self):
        """ Resets the pad positions in a two terminal device. """
        
        position = ( self.x , self.y )
        size = ( self.w , self.h )
        center = ( self.x + self.w // 2 , self.y + self.h // 2 )
        
        input_pos = [position[0],center[1]]
        output_pos = [position[0] + size[0],center[1]]
        
        self.input.set_position(input_pos)
        
        self.output.set_position(output_pos)
        
    def program(self):
        """ Programming behavior for the not-gate during answer validation. """
        
        input_terminal = self.input.program()
        
        if input_terminal:
                
            return Not(input_terminal)
        
        return None
        
    def evaluate(self):
        """ Evaluation behavior for the gate when determining logic flow 
            from the switches. 
        """
        
        value = self.input.evaluate()
        
        if value != None:
        
            self.value = not value
        
        else:
            
            self.value = None
        
        return self.value  
        
        

class Logic3Terminal(LogicElement):
    """ Base class for three terminal devices with two inputs and one
        output.
    """
    
    def reset_pads(self):
        """ Sets the terminal positions for a three terminal device when 
            the logic gate moves. 
        """
        
        position = ( self.x , self.y )
        size = ( self.w , self.h )
        center = ( self.x + self.w // 2 , self.y + self.h // 2 )
        
        input_A_pos = [position[0],center[1] - size[1] // 4]
        input_B_pos = [position[0],center[1] + size[1] // 4]
        output_pos = [position[0] + size[0],center[1]]
        
        self.input_A.set_position(input_A_pos)
        self.input_B.set_position(input_B_pos)
        
        self.output.set_position(output_pos)
        
        
    def get_size(self):
        
        return (self.w,self.h)

class LogicOr(Logic3Terminal):
    """ A three terminal Or gate. """
    
    def __init__(self):
        
        self.container = None
    
        self.input_A = Pad(self,(-20,-20),"Input")
        
        self.input_B = Pad(self,(-20,-20),"Input")
        
        self.output = Pad(self,(-20,-20),"Output")
        
        self.pads = (self.input_A,self.input_B,self.output)
        
        self.value = None
        
        self.locked = False
        
        self.replacement = Or
        
        self.x = 0
        self.y = 0
        self.w = WIDTH * SCALE
        self.h = HEIGHT * SCALE
        
        self.symbol = draw_or()
    
    def gate_type(self):
        
        return "Or"
        
    def program(self):
        """ Programming behavior for the Or gate when the  
        """
        
        input_A = self.input_A.program()
            
        input_B = self.input_B.program()
    
        if input_A and input_B:
            
            return Or(self.input_A.program(),self.input_B.program())
            
        return None    
    
    def evaluate(self):
        """ Evaluates the value of the gate using its inputs. """
        
        value_A = self.input_A.evaluate()
            
        value_B = self.input_B.evaluate()
        
        if value_A != None and value_B != None:
            
            self.value = value_A or value_B
            
        else:
            
            self.value = None
            
        return self.value
        
        
            
class LogicAnd(Logic3Terminal):
    """ A three-terminal And gate. """
    
    def __init__(self):
        
        self.containter = None
    
        self.input_A = Pad(self,(-20,-20),"Input")
        
        self.input_B = Pad(self,(-20,-20),"Input")
        
        self.output = Pad(self,(-20,-20),"Output")
        
        self.pads = [self.input_A,self.input_B,self.output]
        
        self.value = None
        
        self.replacement = And
         
        self.x = 0
        self.y = 0
        self.w = WIDTH * SCALE
        self.h = HEIGHT * SCALE
        self.locked = False
        
        self.symbol = draw_and()
    
    def gate_type(self):
        
        return "And"
    
    def program(self):
        """ Programming behavior for an And gate in answer validation. """
        
        input_A = self.input_A.program()
            
        input_B = self.input_B.program()
    
        if input_A and input_B:
            
            return And(self.input_A.program(),self.input_B.program())
            
        return None
    
    def evaluate(self):
        """ Evalutes the value of the gate using the values of its 
            terminals. 
        """
        
        value_A = self.input_A.evaluate()
            
        value_B = self.input_B.evaluate()
        
        if value_A != None and value_B != None:
            
            self.value = value_A and value_B
            
        else:
            
            self.value = None
            
        return self.value
        
class Factory(LogicElement):
    """ A factory for creating logic gates. """
    
    def __init__(self,Machine,position,scale = 1.0):
        
        self.container = None
        
        self.Product = Machine
        
        self.x , self.y = position
        self.w , self.h = ( SCALE * WIDTH , SCALE * HEIGHT )  
    
        self.locked = True
        
        self.factory_model()
    
    def get_type(self):
        """ Returns the fact that this is a factory. """
        
        return "Factory"
    
    def gate_type(self):
        
        return self.instance.gate_type()
    
    def create(self,position):
        """ Creates a new instance of the factory's element. """
        
        new_machine = self.Product()
        
        new_machine.set_position(position)
        
        return new_machine
        
    def factory_model(self):
        """ Creates a factory model. """
        
        self.instance = self.Product()
        
        self.instance.set_position((self.x + self.w // 2,self.y + self.h // 2))
        
        self.instance.lock()
    
    def draw(self,screen):
        """ Draws the kind of object the factory creates. """
        
        self.instance.draw(screen)
    
class LogicGround(LogicElement):
    """ Will ground out a signal from a switch. """
    
    def __init__(self):
        
        self.container = None
        
        self.input = Pad(self,(-20,-20),"Input")
        
        self.pads = [self.input]
        
        self.color = COLOR3
        
        self.answer_value = True
        self.user_value = False
        
        self.answer = []
        self.user = []
        
        self.locked = True
        
        self.x = 0
        self.y = 0
        self.w = WIDTH * SCALE
        self.h = HEIGHT * SCALE
        
        self.symbol = draw_ground()
        
    def gate_type(self):

        return "Ground"
    
    def reset_pads(self):
        """ Resets the position of the input pad. """
        
        position = (self.x,self.y)
        size = (self.w,self.h)
        center = (self.x + self.w//2, self.y + self.h//2)
        
        input_pos = [position[0],center[1] ]
        
        self.input.set_position(input_pos)
    
    
class LogicLight(LogicElement):
    """ An indicator that turns on its base when its program is satisfied
        and turns on a central light when the player's logical structure 
        is satified.
    """
    
    def __init__(self):
        
        self.container = None
        
        self.input = Pad(self,(-20,-20),"Input")
        
        self.pads = [self.input]
        
        self.color = COLOR3
        
        self.answer_value = True
        self.user_value = False
        
        self.answer = []
        self.user = []
        
        self.locked = True
        
        self.x = 0
        self.y = 0
        self.w = WIDTH * SCALE
        self.h = HEIGHT * SCALE
        
    def gate_type(self):

        return "Light"
    
    def reset_pads(self):
        """ Resets the position of the input pad. """
        
        position = (self.x,self.y)
        size = (self.w,self.h)
        center = (self.x + self.w//2, self.y + self.h//2)
        
        input_pos = [position[0],center[1] ]
        
        self.input.set_position(input_pos)
        
    def dyanmic_program(self,buttons,first_node):
        """ Programs the light using the first node of the logic tree. """
        
        self.program = TruthTable(buttons,[first_node])
    
    def static_program(self,program):
        """ Programs the light with a truth table. """
        
        self.program = program
    
    def clear(self):
        """ Clear the value of the player's program from the light's memory. """
        
        self.user_value = None
    
    def evaluate(self,buttons = None):
        """ Evaluates both the programmed (expected) value and the current
            value of the user's input. 
        """
        
        if type(self.program) == list:
            n = 1
            x = 0
            for button in buttons:
                if button.get_value() == True:
                    x += n 
                n *= 2
            self.answer_value = self.program[x]
        else:
            self.answer_value = self.program.evaluate()
        
        self.user_value = self.input.evaluate()
    
        if buttons and self.user_value != None:
            
            if type(self.program) == list:
                
                input_program = self.input.program()
                
                truth_table = TruthTable(buttons,[input_program])
                
                if truth_table.compare(self.program):
                    
                    return True
                
            else:
            
                input_program = self.input.program() 
            
                truth_table = TruthTable(buttons,[self.program,input_program])
            
                if truth_table.equal():
                
                    return True
   
    def draw(self,screen):
        
        position = (self.x,self.y)
        size = (self.w,self.h)
        center = (self.x + self.w//2, self.y + self.h//2)
        
        if self.answer_value:
            program_color = (192,0,0)
        else:
            program_color = (64,0,0)
           
        
        radius = size[1]//2
        puzzle_radius = radius - 2
        inner_radius = radius - 5
        light_radius = radius - 7
        
        
        start = (position[0],center[1])
        
        pg.draw.line(screen,self.color,start,center,3)
        pg.draw.circle(screen,program_color,center,puzzle_radius)
        pg.draw.circle(screen,self.color,center,radius,2)
        pg.draw.circle(screen,self.color,center,inner_radius,2)
         
        
        if self.user_value:
            
            puzzle_color = YELLOW
            pg.draw.circle(screen,puzzle_color,center,light_radius)
     
        self.input.draw(screen)

class LogicSwitch(LogicElement):
    
    def __init__(self,label = None):
        
        self.container = None
        
        self.output = Pad(self,(-20,-20),"Output")
        
        self.pads = [self.output]
        
        self.value = True
        
        self.locked = True
        
        self.label = label
        
        self.on_color = LETTER_ON
        self.off_color = LETTER_OFF
        
        self.symbol_on = draw_switch_on()
        
        self.symbol_off = draw_switch_off()
        
        
        
        self.x = 0
        self.y = 0
        self.w = SCALE * WIDTH
        self.h = SCALE * HEIGHT
        
    def gate_type(self):
        
        return "Switch" 
    
    def is_reducible(self):
        """ Returns True if the expression can be evaluated """
        
        return False
            
    def reset_pads(self):
        """ Repositions the terminals on the screeen when the logic
            elements are moved.
        """
        
        if self.container:
        
            position = self.container.get_position()
            center = self.container.get_center()
            size = self.container.get_size()
        
        else:
            
            position = (self.x,self.y)
            size = (self.w,self.h)
            center = (self.x + self.w//2, self.y + self.h//2)
        
        output_pos = [position[0] + size[0],center[1] ]
        
        self.output.set_position(output_pos)
    
    def program(self):
        """ Returns self as an input of the program in the programming chain."""
        
        return self
    
    def evaluate(self):
        """ Pretends to do an evaluation, but instead just returns the 
            status of the button. """
            
        return self.value
    
    def get_value(self):
        """ Returns the status of the button. """
        
        return self.value
        
    def get_name(self):
        """ Returns the button's label. """
        
        return self.label
    
    def get_type(self):
        
        return "Button"
        
    def Class(self):
        """ Returns the kind of node to replace the button with when a 
            tree is copied.
        """
        
        return Variable
    
    def activate(self):
        ''' Sets the activation status of the button to active. '''
        
        self.active = True
        
    def deactivate(self):
        ''' Sets the activation status of the button to inactive. '''
        
        self.active = False
        
    def toggle(self):
        ''' Switches the position of the button. '''
        
        self.value = not self.value
    
    def get_inputs(self):
        """ Returns the input nodes as if the button were a node.  """
        
        return None
        
        
    def draw(self,screen):
        
        if self.container:
        
            position = self.container.get_position()
            center = self.container.get_center()
            size = self.container.get_size()
        
        else:
            
            position = (self.x,self.y)
            size = (self.w,self.h)
            center = (self.x + self.w//2, self.y + self.h//2)
        
        radius = size[1]//2
        light_radius = radius - 4
        left_center  = (center[0] - size[0] // 9 , center[1])
        right_center = (center[0] + size[0] // 9 , center[1])
        
        if self.value:
            screen.blit(self.symbol_on,position)
            sw_center = right_center
        else:
            screen.blit(self.symbol_off,position)
            sw_center = left_center
        
        sw_radius = radius - 8
        label_pos = (sw_center[0] - sw_radius // 2,sw_center[1] - sw_radius)
        
        if self.value:
            screenprint(screen,self.label,label_pos,3*sw_radius//2,self.on_color)
        else:
            screenprint(screen,self.label,label_pos,3*sw_radius//2,self.off_color)
    
        self.output.draw(screen)



def draw_switch_base(color1 = None, color2 = None,color3 = None):
    """ Draws out the switch. """
    
    if not color1:
        color1 = COLOR1
    if not color2:
        color2 = COLOR2
    if not color3:
        color3 = COLOR3
        
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    container = pg.Surface(size)
    
    radius = size[1]//2
    light_radius = radius - 4
    left_center  = (center[0] - size[0] // 9 , center[1])
    right_center = (center[0] + size[0] // 9 , center[1])
    box_size = (size[0] // 9 * 2 , size[1])
    small_size = (box_size[0],size[1] - 8)
    large_corner = (left_center[0],position[1])
    small_corner = (large_corner[0],position[1] + 4)
    
    start = (position[0]+size[0],center[1])
    
    pg.draw.line(container,color3,start,center,3)
    pg.draw.circle(container,color3,start,6)
    pg.draw.circle(container,color1,left_center,radius)
    pg.draw.circle(container,color1,right_center,radius)
    pg.draw.rect(container,color1,(large_corner,box_size))
    pg.draw.circle(container,color2,left_center,light_radius)
    pg.draw.circle(container,color2,right_center,light_radius)
    pg.draw.rect(container,color2,(small_corner,small_size))
    
    return container
    

def draw_switch_on(color1 = None, color2 = None):
    
    if not color1:
        color1 = COLOR1
    if not color2:
        color2 = LIGHT_ON
        
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    container = draw_switch_base()
    
    color = YELLOW
    
    sw_center = (center[0] + size[0] // 9 , center[1])
    
    sw_radius = size[1] // 2 - 8
    
    light_radius = size[1] // 2 - 4
        
    pg.draw.circle(container,color1,sw_center,light_radius)
    pg.draw.circle(container,color2,sw_center,sw_radius)
    
    container.set_colorkey((0,0,0))
    
    return container
    
def draw_switch_off(color1 = None, color2 = None):
    
    if not color1:
        color1 = COLOR1
    if not color2:
        color2 = LIGHT_OFF
        
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    container = draw_switch_base()
    
    light_radius = size[1] // 2 - 4
    
    sw_center = (center[0] - size[0] // 9 , center[1])    
    sw_radius = size[1] // 2 - 8
                
    pg.draw.circle(container,color1,sw_center,light_radius)
    pg.draw.circle(container,color2,sw_center,sw_radius)
    
    container.set_colorkey((0,0,0))
    
    return container
        

def draw_ground(color = None):
    """ Draws out the ground and saves it as a transparent picture for
        blitting. 
    """
    
    if not color:
        color = COLOR3
    
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    start = (position[0]+size[0],center[1])
    lead = (position[0],center[1] )
    container = pg.Surface(size)
    
    top = [center[0],0]
    bottom = [center[0],size[1]]
    dx = 8
    dy = size[1] // 9
    
    pg.draw.line(container,color,lead,center,3)
    for i in range(3):
        bottom[1] -= dy
        top[1] += dy
        pg.draw.line(container,color,top,bottom,3)
        top[0] += dx
        bottom[0] += dx
        
    container.set_colorkey((0,0,0))
    
    return container
    
def draw_not(color1 = None, color2 = None,color3 = None):
    """ Draws out the Not gate and saves it as a transparent picture for
        blitting. 
    """
    
    if not color1:
        color1 = COLOR1
    if not color2:
        color2 = COLOR2
    if not color3:
        color3 = COLOR3
    
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    container = pg.Surface(size)
        
    radius = size[1]//6
    light_radius = radius - 3
        
    corner = (position[0] + 2 * size[0] // 9,position[1])
    internal_corner = ( corner[0] + 3 , corner[1] + 6 )
    bottom = (corner[0],position[1]+size[1])
    internal_bottom = ( bottom[0] + 3 , bottom[1] - 6)
    final = (corner[0] + 4 * size[0] // 9 , center[1])
    internal_final = (final[0] - 8 , final[1])
    external = (corner,bottom,final)
    internal = (internal_corner,internal_bottom,internal_final)
    
    circle_spot = (final[0] + radius,final[1])
    
    start = (position[0]+size[0],center[1])
    lead = (position[0],center[1] )
    
    pg.draw.line(container,color3,start,center,3)
    pg.draw.line(container,color3,lead,center,3)
        
    pg.draw.polygon(container,color1,external)
    pg.draw.circle(container,color1,circle_spot,radius)
    pg.draw.polygon(container,color2,internal)
    pg.draw.circle(container,color2,circle_spot,light_radius)
    
    container.set_colorkey((0,0,0))
    
    return container

    
def draw_or(color1 = None, color2 = None,color3 = None):
    """ Draws out the Or gate and saves it as a transparent picture for
        blitting.
    """
    
    if not color1:
        color1 = COLOR1
    if not color2:
        color2 = COLOR2
    if not color3:
        color3 = COLOR3
    
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    r = size[1] / 1.5
    
    container = pg.Surface(size)
    
    radius = size[1]*5//9
    light_radius = radius - 4
    
    side_center = (center[0] + size[0] // 9, center[1])
    arc_corner = (position[0] + size[0] //9 - 3, position[1])
    other_corner = (arc_corner[0],position[1] - size[1] //2) 
    arc_corner2 = (arc_corner[0]+3, arc_corner[1]+2)
    other_corner2 = (other_corner [0]+3,other_corner[1] -2)    
    
    blackout_center = (position[0] + size[0]//9,center[1])
    
        
    corner = (position[0] + 2 * size[0] // 9,position[1])  
    internal_corner = ( corner[0] + 3 , corner[1] + 3 )
    square_size = (size[1] // 2 ,size[1])
    arc_size = (size[1] * 10 ** 0.5 // 2, size[1] * 3 // 2)
    small_size = (size[1] - 8 , size[1]-6)
    small_arc = (arc_size[1] - 3 , arc_size[1]-3)    
    start = (position[0]+size[0],center[1])
    top_lead = (position[0],center[1] + size[1] // 4 )
    bottom_lead = (position[0],center[1] - size[1] // 4)
    top_end = (center[0],top_lead[1])
    bottom_end = (center[0],bottom_lead[1])
    
    pg.draw.line(container,color3,start,center,3)
    pg.draw.line(container,color3,top_lead,top_end,3)
    pg.draw.line(container,color3,bottom_lead,bottom_end,3)
    
    for i in range(size[1]):
        
        x0 = corner[0]
        y1 = corner[1] + i
        x1 = int( ( r * r - ( y1 - r * 3.0 / 4.0  ) ** 2.0  )**0.5 )
        if i < size[1] / 2.0:
            x1p = int( ( 4 * r * r - ( y1 - r * 1.4 ) ** 2.0  )**0.5 )
        else:
            x1p = int( ( 4 * r * r - ( y1 - r * 0.1) ** 2.0  )**0.5 )
        x2 = arc_size[0] * x1p / r - 1.6 * r - 2
        
        pg.draw.line(container,color2,(x1,y1),(x2,y1),1)
        
    for i in range(size[1]):
        
        x0 = corner[0]
        y1 = corner[1] + i
        x1 = int( ( r * r - ( y1 - r * 3.0 / 4.0  ) ** 2.0  )**0.5 )
        if i < size[1] / 2.0:
            x1p = int( ( 4 * r * r - ( y1 - r * 1.4 ) ** 2.0  )**0.5 )
            x1q = 5 - int( float( i % size[1] ) / float(size[1]) * 6.0)
        else:
            x1p = int( ( 4 * r * r - ( y1 - r * 0.1) ** 2.0  )**0.5 )
            x1q = 5 - int( (1.0-(float( i % size[1] ) / float(size[1]))) * 6.0)
        x2 = arc_size[0] * x1p / r - 1.6 * r - 2
        
        if i < 3 or i > size[1] - 4:
            pg.draw.line(container,color1,(x1,y1),(x2,y1),1)
        pg.draw.line(container,color1,(x1 - 3 ,y1),(x1,y1),1)
        pg.draw.line(container,color1,(x2 - 3 - x1q ,y1),(x2,y1),1)
    
    container.set_colorkey((0,0,0))
    
    return container
    
def draw_and(color1 = None, color2 = None,color3 = None):
    """ Draws the And gate and saves it as a transparent picture for
        blitting. 
    """
    
    if not color1:
        color1 = COLOR1
    if not color2:
        color2 = COLOR2
    if not color3:
        color3 = COLOR3
    
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    container = pg.Surface(size)
        
    radius = size[1]//2
    light_radius = radius - 4
    
    side_center = (center[0] + size[0] // 9, center[1])
    corner = (position[0] + 2 * size[0] // 9,position[1])
    internal_corner = ( corner[0] + 3 , corner[1] + 3 )
    square_size = (size[1] - 3 ,size[1])
    small_size = (size[1] - 8 , size[1]-6)
    
    start = (position[0]+size[0],center[1])
    top_lead = (position[0],center[1] + size[1] // 4 )
    bottom_lead = (position[0],center[1] - size[1] // 4)
    top_end = (center[0],top_lead[1])
    bottom_end = (center[0],bottom_lead[1])
    
    pg.draw.line(container,color3,start,center,3)
    pg.draw.line(container,color3,top_lead,top_end,3)
    pg.draw.line(container,color3,bottom_lead,bottom_end,3)
    
    pg.draw.circle(container,color1,side_center,radius)
    pg.draw.rect(container,color1,(corner,square_size))
    pg.draw.circle(container,color2,side_center,light_radius)
    pg.draw.rect(container,color2,(internal_corner,small_size))
    
    container.set_colorkey((0,0,0))
    
    return container

def screenprint(screen = None,message="",position = [0,0],size = 20,color = WHITE,font = "Arial"):
    ''' Prints a message on the PyGame screen. 
            screen - the PyGame object on which to place text
            message - the string object to print on the screen
            positon - a two-element list of integers describing where to
                        print the message on the screen
            size - an integer representing the size of text to print
            color - a PyGame color or a gameclass color constant
            font - a string representing the font to print on the screen  
    '''

    position = (int(position[0]),int(position[1]))
    
    message = str(message)
    
    outputfont = pg.font.SysFont(font,size)
    outputmessage = outputfont.render(message,1,color)
    
    if screen:
        screen.blit(outputmessage,position)
        
    return outputmessage
    