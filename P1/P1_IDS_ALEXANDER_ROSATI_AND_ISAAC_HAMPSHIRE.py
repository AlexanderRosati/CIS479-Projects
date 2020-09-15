#Authors: Alexander Rosati and Isaac Hampshire
import queue;

#Tracks what step the algorithm is on
step_counter = 0

#Returns the display value of the given index within the space
def get_display(x, y):
    return str(space[y][x])

#Displays the current state of the space
def display_space():
    border_string = ""

    for j in range(0, width):
            border_string += "--"

            if j != width-1:
                border_string += "--"

    print(border_string)

    for i in range(0, height):

        row_string = ""
        for j in range(0, width):
            row_string += get_display(j, i)

            if j != width:
                row_string += "  "
        
        print(row_string)

    print(border_string)

#Resets all non-wall nodes to empty nodes
def reset_space():

    for i in range(0,height):
        for j in range(0,width):

            if (not space[i][j].solid):
                space[i][j] = Node(False, j, i)

#Stores the data at a given space, acting as a graph node
class Node:

    #Constructor
    def __init__(self, solid, x, y):
        
        #Whether the node can be traversed
        self.solid = solid

        #The position of the node
        self.pos = [x, y]

        #The state of the node in the algorithm
        self.state = 0

        #The step this node was visited on
        self.visited_on = -1

        #The depth of this node on the path
        self.depth = -1

        #The path cost to reach this node
        self.cost = -1

    #String conversion for display
    def __str__(self):
        msg = "  "

        if (self.solid):
            msg = "##"

        elif (self.state == 2):
            msg = str(self.visited_on)

            if (self.visited_on < 10):
                msg = "0" + msg
        
        return msg

    #Compares the priority of this node with another
    def __lt__(self, other):
        selfPriority = self.cost
        otherPriority = other.cost
        return selfPriority < otherPriority

    #Marks this node as scanned by the search algorithm
    #(Placed into the frontier)
    def scan(self, parent, depth, cost, step_number):

        #Mark state
        self.state = 1

        #Set the parent node, depth, and cost
        self.parent = parent
        self.depth = depth
        self.cost = cost

        #Set step visited on
        self.visited_on = step_number
    
    #Marks this node as visited by the search algorithm
    def visit(self):

        #Mark state
        self.state = 2

#Scans the given node position, adding it to the frontier
def scan(parent, nodePos, depth, cost):

    #Retrieve step counter value
    global step_counter

    #If in bounds
    if ((nodePos[0] >= 0 and nodePos[0] < width) and (nodePos[1] >= 0 and nodePos[1] < height)):

        #Get the node from the position
        node = space[nodePos[1]][nodePos[0]]

        #If the node isn't a wall and has not been scanned
        if ((not node.solid) and node.state == 0):
                
            #Mark the node as scanned and add to the queue
            node.scan(parent, depth, cost, step_counter)
            q.put(node)

            #Increment the step counter
            step_counter += 1
    

#Visits the given node, adding new neighbors to the frontier
def visit(node):

    #Mark the node as visited
    node.visit()

    #If not at depth limit
    if (node.depth < depth_limit):

        #Scan neighbors
        scan(node, [node.pos[0]-1, node.pos[1]], node.depth+1, node.cost+2)
        scan(node, [node.pos[0], node.pos[1]-1], node.depth+1, node.cost+3)
        scan(node, [node.pos[0]+1, node.pos[1]], node.depth+1, node.cost+2)
        scan(node, [node.pos[0], node.pos[1]+1], node.depth+1, node.cost+1)

#-------------------------------------------------------------------------------

#Initializing the space
width = 5
height = 6
space = [[Node(False, i, j) for i in range(width)] for j in range(height)]

#Create walls
space[1][1].solid = True
space[2][1].solid = True
space[3][1].solid = True
space[4][1].solid = True
space[1][2].solid = True
space[3][2].solid = True

#Starting coordinates
start = [0, 3]

#Initialize search
depth_limit = 1
depth_increment = 1
max_depth = 9

#Continue until all nodes traversed
while (depth_limit <= max_depth):

    #Initialize step counter
    step_counter = 0
    
    #Initialize queue with start position
    q = queue.LifoQueue()
    scan(None, start, 0, 0)

    #Until depth is fully traversed
    while (not q.empty()):

        #Get the next node
        node = q.get()

        #Visit the node
        visit(node)

    #Display pass results
    display_space()

    #Increment depth limit
    depth_limit += depth_increment

    #Reset the space
    reset_space()


