# Authors: Alexander Rosati and Isaac Hampshire
# Class: CIS 479
#
# Grid System
# 
# Key:
#   E = Empty Space
#   O = Obstacle
#   S = Start
#   G = Goal
#   
#   X 0 1 2 3 4
#   Y 
#   0 E E E E E
#   1 E O O E E
#   2 E O G E E
#   3 S O O E E
#   4 E O E E E
#   5 E E E E E

# class for maze
class Maze:
    # content is a list of lists
    def __init__(self, content):
        self.content = content
        self.width = len(content[0]) # should be 5
        self.height = len(content) # should be 6
        self.valid_moves = [(-1, 0), (0, -1), (1, 0), (0, 1)] # left, right, up, down

        self.move_costs = {
            "west": 2,
            "north": 3,
            "east": 2,
            "south": 1
        }


# general class for other node classes
class GeneralNode:
    #positions is a tuple and parent is a referent to another General Node
    def __init__(self, position, parent):
        self.position = position # what position on grid?
        self.parent = parent # for testing
    
    # other is another General Node
    def __eq__(self, other):
        return self.position == other.position

# specialized node class for a-star algorithm
class AStarNode(GeneralNode):
    
    # position is a tuple and parent is another AStarNode
    def __init__(self, position, parent):
        GeneralNode.__init__(self, position, parent)
        self.g = 0 # cost from start to node
        self.h = 0 # estimated cost from node to goal
        self.f = 0 # g + h = f

# modified manhatten distance. accounts for wind.
#   position is a tuple
#   goal is a tuple
def modif_manhattan_dist(position, goal):
    x_diff = goal[0] - position[0]
    y_diff = goal[1] - position[1]
    x_component = 2 * abs(x_diff)
    y_component = y_diff if y_diff > 0 else -3 * y_diff
    return x_component + y_component

# construct path from start to goal
# goal node is an astar node
# not required but implemented for testing purposes
def construct_solution(goal_node):

    # list that will contain positions
    path = []

    # point to goal node
    curr_node = goal_node

    # move along path
    while (curr_node is not None):
        path.append(curr_node.position)
        curr_node = curr_node.parent
    
    # reverse list
    path = path[::-1]

    # return list full of positions along path
    return path

# displays output
def display_output(maze):

    # print header
    print("A* Search")
    print("------------------")

    # print content
    content = ""
    for row in maze:
        for elem in row:
            if elem is -1:
                content += "##"
            elif elem < 10:
                content += ("0" + str(elem))
            else:
                content += str(elem)
                
            content += " "

        content += "\n"
    
    print(content, end="")
    print("------------------")
    


# a-star algorithm
# maze is an object of type Maze. start and goal are tuples
def a_star_alg(maze, start, goal):
    
    # make a copy of maze to keep track of the order in which nodes
    # are added to the frontier
    maze_copy = []
    
    for row in maze.content:
        maze_copy.append(row.copy())
    
    # replace ones with #
    for i in range(maze.height):
        for j in range(maze.width):
            if maze_copy[i][j] is 1:
                maze_copy[i][j] = -1

    #initialize vars
    current_node = None
    new_position = None
    new_node = None
    num_added_to_frontier = 1
    new_positions = []
    children_nodes = []

    # create frontier
    frontier = []

    # create explored set
    explored = []

    # add initial state to frontier
    frontier.append(AStarNode(start, None))

    # create goal node
    goal_node = AStarNode(goal, None)

    # while frontier is not empty
    while len(frontier) > 0:
        
        # get node with lowest f
        current_node = frontier[0]

        for node in frontier:
            if (node.f < current_node.f):
                current_node = node

        # remove current node from frontier
        frontier.remove(current_node)

        # add current node to explored set
        explored.append(current_node)

        # see if we reached goal
        if current_node == goal_node:
            display_output(maze_copy)
            return

        # find adjacent nodes
        for move in maze.valid_moves:
            # calculate new position: eithier left, right, up or down from current
            new_position = (current_node.position[0] + move[0],
                            current_node.position[1] + move[1])
            
            # ensure new position is within bounds
            if (new_position[0] < 0 or
                new_position[0] >= maze.width or
                new_position[1] < 0 or
                new_position[1] >= maze.height):
                continue
            
            # make sure new position is not on an obstacle
            if (maze.content[ new_position[1] ][ new_position[0] ] is 1):
                continue

            new_positions.append(new_position)

        # look at adjacent nodes
        for position in new_positions:
            
            # create new node
            new_node = AStarNode(position, None)

            # if node has already been explored, ignore it
            if new_node in explored or new_node in frontier:
                continue

            # if node is not in frontier
            else:
                
                # determine whether new node is west, north, east, or south of
                # current node
                move = (new_node.position[0] - current_node.position[0],
                        new_node.position[1] - current_node.position[1])
                
                # calculage g
                if (move == (-1, 0)): # we moved west
                    new_node.g = current_node.g + maze.move_costs["west"]

                elif (move == (0, -1)): # we moved north
                    new_node.g = current_node.g + maze.move_costs["north"]

                elif (move == (1, 0)): # we moved east
                    new_node.g = current_node.g + maze.move_costs["east"]

                elif (move == (0, 1)): # we move south
                    new_node.g = current_node.g + maze.move_costs["south"]
                
                # calculate h
                new_node.h = modif_manhattan_dist(new_node.position, goal)

                # calculate f
                new_node.f = new_node.g + new_node.h

                # add new node to frontier
                frontier.append(new_node)

                # put label in copy of maze
                maze_copy[ new_node.position[1] ][ new_node.position[0] ] = num_added_to_frontier
                num_added_to_frontier += 1

                # new nodes parent is current node
                new_node.parent = current_node

        # reset everything
        new_positions.clear()
        children_nodes.clear()



# where script begins
if __name__ == "__main__":
    #keep track of where obstacles are
    maze = Maze (
                [[0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0]]
            )
    
    #initialize vars
    start = (0, 3) # (x, y) initialize start
    goal = (2, 2) # (x, y) initialize end

    #call a-star algorithm
    a_star_alg(maze, start, goal)