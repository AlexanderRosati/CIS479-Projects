# Authors: Alexander Rosati and Isaac Hampshire
# Class: CIS479
# Professor: Shengquan Wang
# Written: 10-31-2020
# Program Name: Program 2
# Python Version: Python 3.6.9
# OS: Ubuntu

# imports #######################################################################
import numpy as np # 'pip install numpy' to install this module

# global vars #######################################################################
width = 5 # width of maze
height = 6 # height of maze
obstacles = ((1, 1),    # EEEEE     E = Empty
             (1, 2),    # EOOEE     O = Obstacles
             (2, 1),    # EOEEE
             (3, 1),    # EOOEE
             (3, 2),    # EOEEE
             (4, 1))    # EEEEE

DETECT_WALL = 0.75 # bot senses wall and there is one
FAIL_TO_DETECT_WALL = 0.25 # bot senses wall and there isn't one
DETECT_OPEN = 0.8 # bot senses empty space and there is one
FAIL_TO_DETECT_OPEN = 0.2 # bot senses empty space and there isn't one

WEST = 0 # these are here to
NORTH = 1 # make things easier to read

agenda = [[0, 0, 0, 0],  # Z1
          WEST,          # First Action
          [1, 1, 0, 1],  # Z2
          NORTH,         # Second Action
          [1, 1, 0, 1]]  # Z3

agenda_item = 'evidence'

PROB_GO_FORWARD = 0.7
PROB_DRIFT = 0.15

# use list comprehension to get open spaces in maze
open_spaces = [(x, y) for x in range(6) for y in range(5) if (x, y) not in obstacles]

# functions #######################################################################
#
# return new state if action is taken and there is no error
def transition(curr_state, action):
    if (action == 0): # going west
        new_state = (curr_state[0], curr_state[1] - 1)
    elif (action == 1): # going north
        new_state = (curr_state[0] - 1, curr_state[1])
    elif (action == 2): # going east
        new_state = (curr_state[0], curr_state[1] + 1)
    elif (action == 3): # going south
        new_state = (curr_state[0] + 1, curr_state[1])
    
    if (new_state in obstacles # moving into obstacles
        or new_state[0] <= -1 or new_state[0] >= height # above or below maze
        or new_state[1] <= -1 or new_state[1] >= width): # left or right of maze
        return (curr_state[0], curr_state[1]) # stay where you are
    else:
        return new_state # new location

# returns P(Zi = evidence | Si = state)
def evidence_cond_prob(evidence, state):
    prob = 1.0 # probability we return
    is_wall = [] # is wall to w, n, e, s

    # iterate through directions in order of w, n, e, s
    for action in range(4):
        if state == transition(state, action): # if hit wall
            is_wall.append(1) # wall in that direction
        else: # didn't hit wall
            is_wall.append(0) # open space in that direction
    
    # iterate thought directions in order of w, n, e, s
    for dir in range(4):
        if is_wall[dir] == 1 and evidence[dir] == 1: # correctly detected wall
            prob *= DETECT_WALL # mulitiply by factor of 0.75
        elif is_wall[dir] == 0 and evidence[dir] == 0: # correctly detect open space
            prob *= DETECT_OPEN # multiply by factor of 0.8
        elif is_wall[dir] == 0 and evidence[dir] == 1: # incorrectly detect wall
            prob *= FAIL_TO_DETECT_OPEN # multiply by factor of 0.2
        elif is_wall[dir] == 1 and evidence[dir] == 0: # incorrectly detect open space
            prob *= FAIL_TO_DETECT_WALL # multiply by factor of 0.25
    
    return prob # return result

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

# displays distribution
def display(dist):
    for row in dist:
        for cell in row:
            if cell < 1e-8:
                print('####    ', end='')
            else:
                if len("{prob:.2f}".format(prob=cell*100)) == 5:
                    print("{prob:.2f}   ".format(prob=cell*100), end='')
                else:
                    print("{prob:.2f}    ".format(prob=cell*100), end='')
        print()

# sensing update
def filtering(dist, evidence):
    for os in open_spaces: # iterate through open spaces
        dist[os[0], os[1]] *= evidence_cond_prob(evidence, os) # calculate p1,...,p24
    dist /= np.sum(dist) # calculate p1/(p1+...+p24),...,p24/(p1+...+p24)

# motion update
def prediction(dist, action):
    new_dist = np.zeros((height, width), np.float64) # numpy array of zeros
    for os in open_spaces: # iterate though open spaces
        for (state, prob) in transitional_prob(os, action): # iterate though spaces we can travel to
            # add on term for total probability
            # dist[os[0], os[1]] is a result from the last round of filtering
            new_dist[state[0], state[1]] += prob * dist[os[0], os[1]] 
    return new_dist # update distribution

# script starts here ###################################################################
#
# initialize distribution
dist = []

# create list
for _ in range(6):
    dist.append([0.0, 0.0, 0.0, 0.0, 0.0]) # append list to list

dist = np.array(dist) # create numpy array
initial_prob = 1.0 / len(open_spaces) # each open space is equally likely

# iterate through open spaces
for os in open_spaces:
    dist[os[0], os[1]] = initial_prob # put initial prob into open space

# print initial distribution
print('Initial Location Probabilities')
display(dist)
print()

# process agenda until agenda is empty
while len(agenda) != 0:
    if agenda_item == 'evidence':
        agenda_item = 'action' # process action next time
        evidence = agenda.pop(0) # get evidence
        filtering(dist, evidence) # sensing update
        print('Filtering after Evidence ' + str(evidence))
        display(dist) # display dist
    else:
        agenda_item = 'evidence' # process evidence next time
        action = agenda.pop(0) # get action
        dist = prediction(dist, action) # motion update
        print('Prediction after Action ' + ('W' if action == 0 else 'N'))
        display(dist) # display distribution
    
    print() # new line character