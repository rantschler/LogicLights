#
# Base logic functions for Logic Lights
#

class Node:
    """ Parent class for logical contructions. """
    
    def __init__(self):
        """ Initialize the node. """
        
        self.value = None
    
    def __str__(self):
        """ Returns a string of the truth value of the node. """
        
        return str(self.value)
        
    def get_name(self):
        """ Returns the name of the node.  Usually only Variables are
            named. """
        
        return "Unnamed"
        
    def get_type(self):
        """ Returns the type of node. """
        
        return "Node"
        
    def Class(self):
        """ Returns the object's class when copying the tree. """
        
        return Node
    
    def is_reducible(self):
        """ Returns True if the expression can be evaluated """
        
        return True
        
    def evaluate(self):
        """ Determines the truth value of the node. """
        
        return self.value

    def get_value(self):
        """ Returns the last evaluated value of the node. """
        
        return self.value
    
    def get_inputs(self):
        """ Returns the input nodes to the current node.  """
        
        return None

class Not(Node):
    """ A not operation, switching the value of the Boolean input.
                    True -> False       False -> True
    """
    
    def __init__(self, input_terminal):
        """ Initializes the not node, specifying its input node. """
        
        self.terminal = input_terminal
        
        self.evaluate()
        
    def get_type(self):
        """ Returns a string describing the type of node, i.e., Not. """
        
        return "Not"
        
    def Class(self):
        """ Returns the Not class for copying the answer tree. """
        
        return Not
    
    def evaluate(self):
        """ Evaluates the truth value of the node. """
        
        self.value = not self.terminal.evaluate()
        
        return self.value
    
    def get_inputs(self):
        """ Returns the inputs to the node. """
        
        return tuple([self.terminal])
    
    
class Or(Node):
    """ An or operation, comparing two inputs and returning True iff at
        least one input is True. 
            True True -> True   True False -> True
            False True -> True  False False -> False
    """
        
    def __init__(self, left, right):
        """ Sets up the Or node, keeping the two input nodes and evaluating
            its truth condition.
        """
        
        self.terminal_a = left
        self.terminal_b = right
        
        self.evaluate()
        
    def get_type(self):
        """ Returns the name of the operation. """
        
        return "Or"
        
    def Class(self):
        """ Returns the object's class for use copying the tree. """
        
        return Or
        
    def evaluate(self):
        """ Evalutates the current truth-value of the node. """
        
        self.value = self.terminal_a.evaluate() or self.terminal_b.evaluate()
        
        return self.value
    
    def get_inputs(self):
        """ Returns the input nodes. """
        
        return (self.terminal_a,self.terminal_b)
    
class And(Node):
    """ An and operation, comparing two inputs and returning True iff both
        inputs are True. 
            True True -> True   True False -> False
            False True -> False  False False -> False
    """
    
    def __init__(self, left, right):
        """ Sets up the And node, keeping the two input nodes and evaluating
            its truth condition.
        """
        
        self.terminal_a = left
        self.terminal_b = right
        
        self.evaluate()
    
    def get_type(self):
        """ Returns the name of the operation. """
        
        return "And"
        
    def Class(self):
        """ Returns the object's class for use copying the tree. """
        
        return And
        
    def evaluate(self):
        """ Evalutates the current truth-value of the node. """
        
        self.value = self.terminal_a.evaluate() and self.terminal_b.evaluate()
        
        return self.value
    
    def get_inputs(self):
        """ Returns the input nodes. """
        
        return (self.terminal_a,self.terminal_b)
        

class Value(Node):
    """ This is a constant-valued leaf for the logic tree. """
    
    def __init__(self,value):
        """ Creates a node with a constant value of value. """ 
        
        self.value = value
        self.terminal = None
        
    def get_type(self):
        """ Returns the type of node. """
        
        return "Value"
        
    def Class(self):
        """ Returns the class of the node for copying a tree. """
        
        return Value
        
class Variable(Node):
    """ This is leaf whose value can be changed by the program. """
    
    def __init__(self,name):
        """ Sets up the variable with a variable name. """
        
        self.name = name
        
        self.value = False
        self.terminal = None
        
    def get_type(self):
        """ Returns the name of the variable. """
        
        return "Variable"
    
    def Class(self):
        """ Returns the class of the variable for copying purposes. """
        
        return Variable
    
    def get_name(self):
        """ Returns the name of the variable for making headers, sorting,
            and other control functions in the program. 
        """
            
        return self.name
    
    def set(self,value):
        """ Sets the variable to a predetermined value. """
        
        self.value = value
    
    def toggle(self):
        """ Swaps between truth values. """
        
        self.value = not self.value
        

class TruthTable:
    """ Creates a truth table from a set of inputs and outputs, creating
        a specific value for the outputs, allowing truth functions to be
        compared. 
    """
        
    def __init__(self,inputs,outputs):
        """ Creates the truth table.  Inputs should be either buttons or
            variables, outputs should be the root node of an expression or
            a fully-programmed light.
        """
        
        self.controls = tuple(inputs)
        
        self.create_dictionary()
        
        self.originals = tuple(outputs)
        
        self.reformat_statements()
        
        self.value = self.evaluate()
    
    def __str__(self):
        """ Prints out the truth table. """
        
        switches = self.internals
        lights = self.statements
        
        output = ""
        
        for state in range(2 ** len(switches)):
            temp_state = state
            print state,
            for input in switches:
                x = temp_state % 2 
                temp_state //= 2
                if x:
                    input.set(True)
                else:
                    input.set(False)
                print input,
            print " | ",
            for statement in lights:
                statement.evaluate()
                print statement,
            print
            
        return output
    
    def create_dictionary(self):
        """ Takes a set of programmer/user controllable variables or buttons, 
            converts them into a duplicate set of Variables, and creates a
            mapping from the originals to the new ones.
        """
            
        internals = []
        primatives = {}
        
        for input in self.controls:
            primative = Variable(input.get_name())
            primatives[input] = primative
            internals.append(primative)
            
        self.relationships = primatives
        self.internals = internals
        
    def reformat_statements(self):
        """ Takes the problem statement and converts it into something 
            tractable for making a truth table, using the new leaves created
            when putting the dictionary. 
        """
        
        statements = []
        
        for statement in self.originals:
            statements.append(copy_node(statement,self.relationships))
        
        self.statements = statements
    
    def evaluate(self):
        """ Evaluates the value of the truth table.  The value of the 
            table is presented in columns of 2^(# of inputs) height,
            starting from all elements False and going to all elements
            True.
        """
        
        value = []
        number = 0
        for statement in self.statements:
            number += 1
            row = []
            for state in range(2 ** len(self.internals)):
                temp_state = state
           
                for input in self.internals:
                    x = temp_state % 2 
                    temp_state //= 2
                    if x:
                        input.set(True)
                    else:
                        input.set(False)
                row.append(statement.evaluate())
            value.append(row)
        return value
    
    def get_value(self):
        """ Returns the value of the truth table. """
        
        return self.value
        
    def equal(self):
        """ Determines if two statements are equal. """
        
        if len(self.statements) == 2:
            
            result = True
            
            switches = list(self.internals)
            lights = list(self.statements)
            
            for state in range(2 ** len(switches)):
                
                temp_state = state
                
                for input in switches:
                    x = temp_state % 2 
                    temp_state //= 2
                    if x:
                        input.set(True)
                    else:
                        input.set(False)
                
                evaluation = []
                
                for statement in lights:
                    
                    evaluation.append(statement.evaluate())
                    
                result = result and (evaluation[0] == evaluation[1])
            
            return result
            
        else:
            
            return None
        
    def compare(self,program):
        """ Compares the result of a statement to an answer list. """ 

        if len(self.statements) == 1:
            
            result = True
            
            switches = list(self.internals)
            lights = list(self.statements)
            
            for state in range(2 ** len(switches)):
                
                temp_state = state
                
                for input in switches:
                    x = temp_state % 2 
                    temp_state //= 2
                    if x:
                        input.set(True)
                    else:
                        input.set(False)
                
                evaluation = []
                
                statement = lights[0]
                    
                evaluation = statement.evaluate()
                    
                result = result and (evaluation == program[state])
            
            return result
            
        else:
            
            return None
        
    
def copy_node(node,var_dic):
    """ Creates a copy of the node and all of its inputs, replacing 
        variables using the variable dictionary (var_dic) provided.
        The dictionary should work like:
            var_dic[original_Button] = local_table_Variable
    """

    inputs = node.get_inputs()
    
    if inputs == None:
        
        return var_dic[node] 
    
    elif len(inputs) == 1:

        new_input = copy_node(inputs[0],var_dic)
        new_node = node.Class()(new_input)
    
    elif len(inputs) == 2:

        input_a = copy_node(inputs[0],var_dic)
        input_b = copy_node(inputs[1],var_dic)
        new_node = node.Class()(input_a,input_b)
    
    else:
        
        print "Error: Node type not coded."
        exit()
    
    return new_node






def create_truth_table(buttons,number):
    
    out = []
    
    for n in range( 2 ** len(buttons) ):
        
        x = number % 2
        number = number // 2
        
        if x:
            
            out.append(True)
        
        else:
            
            out.append(False)
        
    return out

## #  Define some variables
## a = Variable("A")
## b = Variable("B")
## not_a = Not(a)
## not_a_or_b = Or(Not(a),b)

## print a,not_a
## a.toggle()
## not_a.evaluate()
## print a, not_a

## c = Variable("C")
## print "C"
## d = Variable("D")
## print "D"

## new_one = copy_node(not_a_or_b,{a:c,b:d})


## #  Make a Truth Table
## table = TruthTable([a,b],[a,not_a,not_a_or_b])
## print table
## table = TruthTable([c,d],[new_one])
## print table

## for A in (True,False):
##     for B in (True,False): 
##         for C in (True,False):
##             print A or ( B and not C ),
##             print Or(Value(A),And(Value(B),Not(Value(C))))

