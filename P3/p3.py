# notes about indices
# state positions are stored (x, y) now
# the access frequency and q-values are stored in row-major order
# access them like this data[state[1], state[0]]
# all methods have been updated to use this indexing scheme correctly
# and the obstacles list has been transposed to match

# imports #######################################################################
import numpy as np # 'pip install numpy' to install this module
import random as rnd

# global vars #######################################################################
width = 5 # width of maze
height = 6 # height of maze
obstacles = ((1, 1),    # EEEEE     E = Empty
             (1, 2),    # EOOEE     O = Obstacles
             (2, 1),    # EOGEE     G = Terminal
             (1, 3),    # EOOEE
             (2, 3),    # EOEEE
             (1, 4))    # EEEEE

terminal_state = (2, 2)
terminal_reward = 100

PROB_GO_FORWARD = 0.7
PROB_DRIFT = 0.15

DISP_SEPARATION_SIZE = 5
DISP_SEPARATOR = "     "
DISP_CELL_SEPARATOR = " "

# use list comprehension to get open spaces in maze
open_spaces = [(x, y) for x in range(width) for y in range(height) if (x, y) not in obstacles]

# functions #######################################################################
#
# return new state if action is taken and there is no error
def transition(curr_state, action):
    if (action == 0): # going west
        new_state = (curr_state[0] - 1, curr_state[1])
    elif (action == 1): # going north
        new_state = (curr_state[0], curr_state[1] - 1)
    elif (action == 2): # going east
        new_state = (curr_state[0] + 1, curr_state[1])
    elif (action == 3): # going south
        new_state = (curr_state[0], curr_state[1] + 1)
    
    if (new_state in obstacles # moving into obstacles
        or new_state[0] <= -1 or new_state[0] >= width # left or right of maze
        or new_state[1] <= -1 or new_state[1] >= height): # above or below maze
        return (curr_state[0], curr_state[1]) # stay where you are
    else:
        return new_state # new location

# returns P(Si+1 | Si, a)
def transitional_prob(state, action):
    # go in intended direction
    state_forward = transition(state, action)

    # drift counter clockwise (i.e., drift left)
    state_counter_clockwise = transition(state, (action - 1) % 4)

    # drift clockwise (i.e., drift right)
    state_clockwise = transition(state, (action + 1) % 4)

    # return states you can go to and their associated probabilities
    return ((state_forward, PROB_GO_FORWARD), # PROB_GO_FORWARD = 0.7
            (state_counter_clockwise, PROB_DRIFT), # PROB_DRIFT = 0.15
            (state_clockwise, PROB_DRIFT)) #PROB_DRIFT = 0.15

# return new state for action with possible drift
def transition_with_drift(state, action):

    # get possible transitions
    transitions = transitional_prob(state, action)

    # get random value
    choice = rnd.random()

    # for each possible state
    for t in transitions:

        # if value is within share of probability
        if choice <= t[1]:

            # return state of transition
            return t[0]
        else:

            # consume share
            choice -= t[1]
            
    # error if the code gets here
    print("Probability error in 'transition_with_error' function")
    
# returns all actions with the highest q-value for the given state
def max_actions(state, q_values):

    # retrieve q-values of actions
    actions = q_values[state[1], state[0]]

    # get all actions with maximal q-value
    max_actions = np.argwhere(actions == np.amax(actions))
    return max_actions

# returns the action with the highest q-value for the given state
# breaks ties randomly
def max_action(state, q_values):

    # retrieve max actions
    actions = max_actions(state, q_values)
    
    # choose random action
    index = rnd.randrange(len(actions))
    return actions[index]

# returns the reward for the given state-action pair
def reward(state, action):

    reward = 0
    # if the next state is terminal
    if transition(state, action) == terminal_state:

        # use terminal reward
        reward = terminal_reward
    else:
        # depend on direction
        if action == 0 or action == 2:
            reward = -2
        elif action == 1:
            reward = -3
        else:
            reward = -1
    return reward

# applies Q-Learning step
def update_q(state, action, next_state, access_freq, q_values):

    # increment access frequency
    access_freq[state[1], state[0]][action] += 1

    # todo

# returns a random position to start a path from
def start_state():
    # choose a random open space (excluding the terminal state)
    index = rnd.randrange(len(open_spaces)-1)

    # if chosen index is the terminal state
    if open_spaces[index] == terminal_state:

        # use the next index and loop if needed
        index = (index + 1) % len(open_spaces)
    
    return open_spaces[index]

# displays the values of a (state, action) list
def display(data, display_goal=True):

    # for each row
    for y, row in enumerate(data):

        # for each cell
        for x, cell in enumerate(row):

            # display first line
            if (x, y) in obstacles or (x, y) == terminal_state:
                # empty for obstacles and terminal states
                print(DISP_SEPARATOR + DISP_SEPARATOR + DISP_SEPARATOR + DISP_CELL_SEPARATOR, end='')
            else:
                # display north action
                print(DISP_SEPARATOR, end='')
                print(str(round(cell[1], 1)).center(DISP_SEPARATION_SIZE), end='')
                print(DISP_SEPARATOR + DISP_CELL_SEPARATOR, end='')

        # empty line
        print("\n")

        # for each cell
        for x, cell in enumerate(row):

            # display second line
            if (x, y) in obstacles:
                # display obstacle
                print(DISP_SEPARATOR + "####".center(DISP_SEPARATION_SIZE) + DISP_SEPARATOR + DISP_CELL_SEPARATOR, end='')
            elif (x, y) == terminal_state:
                if display_goal:
                    # display terminal reward
                    print(DISP_SEPARATOR + ("+" + str(terminal_reward)).center(DISP_SEPARATION_SIZE) + DISP_SEPARATOR + DISP_CELL_SEPARATOR, end='')
                else:
                    # display empty terminal state
                    print(DISP_SEPARATOR + DISP_SEPARATOR + DISP_SEPARATOR + DISP_CELL_SEPARATOR, end='')
            else:
                # display east and west actions
                print(str(round(cell[0], 1)).center(DISP_SEPARATION_SIZE), end='')
                print(DISP_SEPARATOR, end='')
                print(str(round(cell[2], 1)).center(DISP_SEPARATION_SIZE), end='')
                print(DISP_CELL_SEPARATOR, end='')

        # empty line
        print("\n")

        # for each cell
        for x, cell in enumerate(row):

            # display third line
            if (x, y) in obstacles or (x, y) == terminal_state:
                # empty for obstacles and terminal states
                print(DISP_SEPARATOR + DISP_SEPARATOR + DISP_SEPARATOR + DISP_CELL_SEPARATOR, end='')
            else:
                # display south action
                print(DISP_SEPARATOR, end='')
                print(str(round(cell[3], 1)).center(DISP_SEPARATION_SIZE), end='')
                print(DISP_SEPARATOR + DISP_CELL_SEPARATOR, end='')

        # empty line
        print("\n")

# displays the current policy
def display_policy(data):

    # for each row
    for y, row in enumerate(data):

        # for each cell
        for x, cell in enumerate(row):
            
            if (x, y) in obstacles:
                # display obstacle
                print("####", end='')
            elif (x, y) == terminal_state:
                # display terminal reward
                print(("+"+str(terminal_reward)).center(4), end='')
            else:
                # display policy
                policy = max_action((x, y), data)
                if policy==0:
                    print("<<<<", end='')
                elif policy==1:
                    print("^^^^", end='')
                elif policy==2:
                    print(">>>>", end='')
                elif policy==3:
                    print("VVVV", end='')
            print("    ", end='')
        print("\n")

# displays the policy and marks the given position (for testing)
def display_marked(data, mark):

    # for each row
    for y, row in enumerate(data):

        # for each cell
        for x, cell in enumerate(row):
            
            if (x, y) in obstacles:
                # display obstacle
                print("####", end='')
            elif (x, y) == terminal_state:
                # display terminal reward
                print(("+"+str(terminal_reward)).center(4), end='')
            elif (x, y) == mark:
                # display marked location
                print("MARK", end='')
            else:
                # display policy
                policy = max_action((x, y), data)
                if policy==0:
                    print("<<<<", end='')
                elif policy==1:
                    print("^^^^", end='')
                elif policy==2:
                    print(">>>>", end='')
                elif policy==3:
                    print("VVVV", end='')
            print("    ", end='')
        print("\n")


# script starts here ###################################################################
#
# access frequency
access_freq = np.zeros((height, width, 4), np.intc)

# q-values
q_values = np.zeros((height, width, 4), np.float64)

# current state
state = start_state()

# randomize q-values (for testing)
#for row in q_values:
#    for cell in row:
#        cell[0] = rnd.random()*10
#        cell[1] = rnd.random()*10
#        cell[2] = rnd.random()*10
#        cell[3] = rnd.random()*10

# display initial state
print("Initial")
display_marked(q_values, state)
print()

# limit to 25 steps for now
for i in range(25):

    # use max transition
    action = max_action(state, q_values)

    # get next state from transition
    next_state = transition_with_drift(state, action)

    # apply Q-Learning
    update_q(state, action, next_state, access_freq, q_values)

    # move to the next state
    state = next_state

    # display current policy and position (for testing)
    print("Step " + str(i+1))
    display_marked(q_values, state)
    print()

    # if the goal state is found
    if state == terminal_state:

        # end the path
        break;

# display q-values
print("Table of Q(s, a)")
display(q_values, True)
print()

# display access frequencies
print("Table of N(s, a)")
display(access_freq, False)
print()

# display policy
display_policy(q_values)
