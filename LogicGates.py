# import gameclass_0_97 as gc
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
        
        self.color = GRAY
        
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
    
    def disconnect(self):
        """ Remove the wire from the terminal, returns the wire. """
        
        if self.type == "Output":
            
            wire = self.connector[0]
            self.connector.remove(wire)
        
        else:
            
            wire = self.connector
            self.connector = None
        
        wire.disconnect(self)
        
        
        return wire
        
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
        
        for pad in self.get_pads():
                            
            wire = pad.get_connector()
                            
            if wire:
                wire.deregister()
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
        
        self.container = None
        self.replacement = None
        
        if node and node.get_type() == "Output":
        
            self.input = node
            self.output = None
        
        elif node and node.get_type() == "Input":
            
            self.input = None
            self.output = node
        
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        
        self.locked = False
    
    def deregister(self):
        """ Completely disconnects the wire from both terminals. """
        
        if self.input:
            self.input.disconnect()
            self.input = None
        if self.output:
            self.output.disconnect()
            self.output = None
    
    def gate_type(self):
        
        return "Wire"
    
    def get_pads(self):
        """ Returns the device terminals that the wire is connected to. """
        
        pads = []
        
        if self.input:
            
            pads.append(self.input)
        
        if self.output:
            
            pads.append(self.output)
        
        return pads
    
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
        
        if not self.input and node.get_type() == "Output":
            
            if self.output.get_owner() == node.get_owner():
                
                return False
            
            self.input = node
            node.set_connector(self)
        
        elif not self.output and node.get_type() == "Input":
            
            if self.input.get_owner() == node.get_owner():
                
                return False
            
            self.output = node
            node.set_connector(self)
            
        else:
            
            return False
        
        return True
    
    def get_type(self):
        """ Returns the type of the logic element. """
        
        return "Wire"
    
    def disconnect(self,node):
        """ Disconnects the terminal from the wire.  """
        
        if node == self.input:
            
            self.input = None
        
        else:
            
            self.output = None
    
    def draw(self,screen):
        """ Draws the wire between nodes. """
        
        if self.locked:
            
            self.draw_static(screen)
        
        else:
            
            if self.input:
                
                pos_A = self.input.get_position()
            
            else:
                
                pos_A = ( self.x , self.y )
            
            if self.output:
                
                pos_B = self.output.get_position()
                
            else:
                
                pos_B = ( self.x , self.y )
            
            center_A = ( ( pos_A[0] + pos_B[0] ) // 2 , pos_A[1] )
            center_B = ( center_A[0] , pos_B[1] )
            
            
            pg.draw.line(screen,GRAY,pos_A,center_A,3)
            pg.draw.line(screen,GRAY,center_A,center_B,3)
            pg.draw.line(screen,GRAY,center_B,pos_B,3)
        

class LogicNot(LogicElement):
    """ A two terminal Not gate. """
    
    def __init__(self):
        
        self.container = None
        
        self.input = Pad(self,(-20,-20),"Input")
        
        self.output = Pad(self,(-20,-20),"Output")
        
        self.pads = [self.input,self.output]
        
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
        
        self.pads = [self.input_A,self.input_B,self.output]
        
        self.value = None
        
        self.locked = False
        
        self.replacement = Or
        
        self.x = 0
        self.y = 0
        self.w = WIDTH * SCALE
        self.h = HEIGHT * SCALE
        
        self.symbol = draw_or2()
    
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
    
    def __init__(self,Machine,position):
        
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
    
class LogicLight(LogicElement):
    """ An indicator that turns on its base when its program is satisfied
        and turns on a central light when the player's logical structure 
        is satified.
    """
    
    def __init__(self):
        
        self.container = None
        
        self.input = Pad(self,(-20,-20),"Input")
        
        self.pads = [self.input]
        
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
    
    def get_pads(self):
        
        return self.pads
    
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
            program_color = (32,32,64)
           
        
        radius = size[1]//2
        puzzle_radius = radius - 2
        inner_radius = radius - 5
        light_radius = radius - 7
        
        
        start = (position[0],center[1])
        
        pg.draw.line(screen,GRAY,start,center,3)
        pg.draw.circle(screen,program_color,center,puzzle_radius)
        pg.draw.circle(screen,GRAY,center,radius,2)
        pg.draw.circle(screen,GRAY,center,inner_radius,2)
         
        
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
        
        screenprint(screen,self.label,label_pos,3*sw_radius//2,BLACK)
    
        self.output.draw(screen)
        

def draw_switch_base():
    """ Draws out the switch. """
    
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
    
    pg.draw.line(container,GRAY,start,center,3)
    pg.draw.circle(container,GRAY,start,6)
    pg.draw.circle(container,GRAY,left_center,radius)
    pg.draw.circle(container,GRAY,right_center,radius)
    pg.draw.rect(container,GRAY,(large_corner,box_size))
    pg.draw.circle(container,DARK_GRAY,left_center,light_radius)
    pg.draw.circle(container,DARK_GRAY,right_center,light_radius)
    pg.draw.rect(container,DARK_GRAY,(small_corner,small_size))
    
    return container
    

def draw_switch_on():
    
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    container = draw_switch_base()
    
    color = YELLOW
    
    sw_center = (center[0] + size[0] // 9 , center[1])
    
    sw_radius = size[1] // 2 - 8
    
    light_radius = size[1] // 2 - 4
        
    pg.draw.circle(container,GRAY,sw_center,light_radius)
    pg.draw.circle(container,color,sw_center,sw_radius)
    
    container.set_colorkey((0,0,0))
    
    return container
    
def draw_switch_off():
    
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    container = draw_switch_base()

    color = DARK_GRAY
    
    light_radius = size[1] // 2 - 4
    
    sw_center = (center[0] - size[0] // 9 , center[1])    
    sw_radius = size[1] // 2 - 8
                
    pg.draw.circle(container,GRAY,sw_center,light_radius)
    pg.draw.circle(container,color,sw_center,sw_radius)
    
    container.set_colorkey((0,0,0))
    
    return container
        
def draw_not():
    """ Draws out the Not gate and saves it as a transparent picture for
        blitting. 
    """
        
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
    
    pg.draw.line(container,GRAY,start,center,3)
    pg.draw.line(container,GRAY,lead,center,3)
        
    pg.draw.polygon(container,GRAY,external)
    pg.draw.circle(container,GRAY,circle_spot,radius)
    pg.draw.polygon(container,DARK_GRAY,internal)
    pg.draw.circle(container,DARK_GRAY,circle_spot,light_radius)
    
    container.set_colorkey((0,0,0))
    
    return container

def draw_or():
    """ Draws out the Or gate and saves it as a transparent picture for
        blitting.
    """
    
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
    container = pg.Surface(size)
    
    radius = size[1]*5//9
    light_radius = radius - 4
    
    side_center = (center[0] + size[0] // 9, center[1])
    arc_corner = (position[0] + size[0] //9 - 3, position[1])
    other_corner = (arc_corner[0],position[1] - size[1] //2)    
    
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
    
    
    
    pg.draw.rect(container,GRAY,(corner,square_size))
    
    pg.draw.arc(container,GRAY,(arc_corner,arc_size),0.3,1.575,23)
    pg.draw.arc(container,GRAY,(other_corner,arc_size),4.705,5.98,23)
        
    pg.draw.arc(container,GRAY,(arc_corner,small_arc),0.3,1.575,23)
    pg.draw.arc(container,GRAY,(other_corner,small_arc),4.705,5.98,23)
        
    pg.draw.circle(container,BLACK,blackout_center,radius)
    
    pg.draw.line(container,GRAY,start,center,3)
    pg.draw.line(container,GRAY,top_lead,top_end,3)
    pg.draw.line(container,GRAY,bottom_lead,bottom_end,3)
    
    container.set_colorkey((0,0,0))
    
    return container
    
def draw_or2():
    """ Draws out the Or gate and saves it as a transparent picture for
        blitting.
    """
    
    size = ( WIDTH * SCALE , HEIGHT * SCALE )
    position = ( 0 , 0 )
    center = ( size[0] // 2 , size[1] // 2 )
    
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
    
    
    
    pg.draw.rect(container,GRAY,(corner,square_size))
     
    pg.draw.arc(container,GRAY,(arc_corner,arc_size),0.3,1.575,23)
    pg.draw.arc(container,GRAY,(other_corner,arc_size),4.705,5.98,23)
        
        
    pg.draw.circle(container,BLACK,blackout_center,radius)
    
    pg.draw.line(container,GRAY,start,center,3)
    pg.draw.line(container,GRAY,top_lead,top_end,3)
    pg.draw.line(container,GRAY,bottom_lead,bottom_end,3)
    
    container.set_colorkey((0,0,0))
    
    return container
    
def draw_and():
    """ Draws the And gate and saves it as a transparent picture for
        blitting. 
    """
    
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
    
    pg.draw.line(container,GRAY,start,center,3)
    pg.draw.line(container,GRAY,top_lead,top_end,3)
    pg.draw.line(container,GRAY,bottom_lead,bottom_end,3)
    
    pg.draw.circle(container,GRAY,side_center,radius)
    pg.draw.rect(container,GRAY,(corner,square_size))
    pg.draw.circle(container,DARK_GRAY,side_center,light_radius)
    pg.draw.rect(container,DARK_GRAY,(internal_corner,small_size))
    
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
    