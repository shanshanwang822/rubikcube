import numpy as np

############### Part A1 #######################
G = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21)

def mult(tup1, tup2):
    return tuple([tup1[i-1] for i in tup2])

upper = (4,5,6,7,8,9,10,11,12,1,2,3,13,14,15,16,17,18,19,20,21)
right = (17,18,16,3,1,2,7,8,9,10,11,12,13,14,15,19,20,21,4,5,6)
front = (12,10,11,4,5,6,7,8,9,13,14,15,16,17,18,2,3,1,19,20,21)

#put upper, right, front in parameter direction to turn the cube in state tup
def Turn(tup, direction):
    return mult(tup, direction)


############## Part A2 ######################
def subgroup_generated(tup ,gens):  
    g_elts = {}
    elts_new = {}
    elts_old = {}
    g_elts[tup] = None
    elts_new[tup] = None
    while elts_new != {}:
        elts_old = elts_new
        elts_new = {}
        for x in elts_old.keys():
            for y in gens:
                p = mult(x,y)
                if p not in g_elts.keys():
                    g_elts[p] = None
                    elts_new[p] = None
    return g_elts.keys()

subGroups = subgroup_generated(G, [upper, right, front])
print('Number of elements in H:')
print(len(subGroups))
print()


############### Part A3 ##################
'''
Since the previous answer is about 1/3 of the total subgroups, there must be
different permutations to get the the same state. There also can be patterns
that only exist on one cube, for example if the blue face is opposite of the 
yellow face, then the yellow face could never end up next to the blue face,
so there must be certain states that are just impossible to get to like the 
state that was just explained. Also the corners of the cube cannot be twisted 
fully, there are some states that cannot exist because of the corner not being able
to be twisted.
'''


########## Part B1 ###################
def inverse(tup):
    output = [0]*len(tup)
    for i, val in enumerate(tup, start = 1):
        output[val-1] = i
    return tuple(output)

upperInv = inverse(upper)
rightInv = inverse(right)
frontInv = inverse(front)

generators = (upper, right, front, upperInv, rightInv, frontInv)

def subgroup_generated_updated(tup ,gens):  
    g_elts = {}
    elts_new = {}
    elts_old = {}
    g_elts[tup] = []
    elts_new[tup] = []
    while elts_new != {}:
        elts_old = elts_new
        elts_new = {}
        for key, value in elts_old.items():
            for y in gens:
                p = mult(key,y)
                if p not in g_elts.keys():
                    newList = value.copy()
                    newList.append(y)
                    g_elts[p] = newList
                    elts_new[p] = newList
    return g_elts

totalMoves = subgroup_generated_updated(G, generators)
    

############# Part B2 #####################

#### a)
maxTurns = -1*np.inf
state = None
for key, value in totalMoves.items():
    if len(value) > maxTurns:
        maxTurns = len(value)
        state = key
print('Most number of quarter turns to solve any position: ')
print(maxTurns)
print()
#MaxTurns are 14

##### b) 
numStates = 0
for key, value in totalMoves.items():
    if len(value) == maxTurns:
        numStates += 1
print('Number of states that require the number of max turns:')
print(numStates)
print()
#Number of states with maxTurns are 276

##### c)
N = len(totalMoves)
avg = 0
for key, value in totalMoves.items():
    avg += len(value)
avg = avg/N
print('Average Number of turns: ')
print(avg)
print()
#The average number of turns in 10.666

########### Part B3 ###############

### Numbers of the types faces ###
topFace = (1,4,7,10)
frontFace = (3,11,14,17)
rightFace = (2,6,18,21)
leftFace = (8,12,13)
backFace = (5,9,19)
bottomFace = (15,16,20)

### Gets the oppossite face color on cube ###
def getOpposite(c):
    if c == 'b':
        return 'g'
    if c == 'y':
        return 'w' 
    if c == 'o':
        return 'p'
    if c == 'w':
        return 'y'
    if c == 'p':
        return 'o'
    if c == 'g':
        return 'b'

### Gets the middle strip that goes around cube with top face being color c ###
def getStrip(c):
    if c == 'b':
        return ['o','w','p','y']
    if c == 'y':
        return ['g','o','b','p']
    if c == 'o':
        return ['b','y','g','w']
    if c == 'w':
        return ['p','b','o','g']
    if c == 'p':
        return ['y','b','w','g']
    if c == 'g':
        return ['w','o','y','p']

colors = ['b','y','o','w','p','g']

correctColors = []

#This goes through each color and sets it as top color and finds the corresponding side colors
for i in range(len(colors)):
    top = colors[i]
    bottom = getOpposite(top)
    strip = getStrip(top)
    for j in range(4):
        output = [0]*21
        f = strip[0]
        r = strip[1]
        b = strip[2]
        l = strip[3]
        for pos in topFace:
            output[pos-1] = top
        for pos in bottomFace:
            output[pos-1] = bottom
        for pos in leftFace:
            output[pos-1] = l
        for pos in rightFace:
            output[pos-1] = r
        for pos in frontFace:
            output[pos-1] = f
        for pos in backFace:
            output[pos-1] = b
        correctColors.append(tuple(output))
        #This bottom line moves the last item in strip to the front
        strip = strip[-1:] + strip[:-1]


### This function converts the turns tuple into words for the main function
def turnsToWords(turns):
    output = []
    for turn in turns:
        if turn == right:
            output.append('Turn Right Clockwise')
        elif turn == rightInv:
            output.append('Turn Right Counter Clockwise')

        elif turn == front:
            output.append('Turn Front Clockwise')
        elif turn == frontInv:
            output.append('Turn Front Counter Clockwise')

        elif turn == upper:
            output.append('Turn Top Clockwise')
        elif turn == upperInv:
            output.append('Turn Top Counter Clockwise')
        else:
            output.append('ERROR HAPPENED')
    return output


### Updated Subgroup generator:
### Returns list of words once it finds a correct state
def subgroup_generated_updated_Quick(tup ,gens):  
    g_elts = {}
    elts_new = {}
    elts_old = {}
    g_elts[tup] = []
    elts_new[tup] = []
    while elts_new != {}:
        elts_old = elts_new
        elts_new = {}
        for key, value in elts_old.items():
            for y in gens:
                p = mult(key,y)
                if p not in g_elts.keys():
                    newList = value.copy()
                    newList.append(y)
                    if p in correctColors:
                        return newList
                    g_elts[p] = newList
                    elts_new[p] = newList
    return 'ERROR: Correct State not found'

### The main function to solve any 2x2 rubiks cube ###
### Does BFS from the input state to any of the 24 identity states
def solveCubeNew(state):
    moves = subgroup_generated_updated_Quick(state, generators)
    turns = turnsToWords(moves)
    for turn in turns:
        print(turn)

######### Part C ###########

### Numbers of the types faces ###
topFace = (1,4,7,10)
frontFace = (3,11,14,17)
rightFace = (2,6,18,21)
leftFace = (8,12,13)
backFace = (5,9,19)
bottomFace = (15,16,20)

faces = [topFace, frontFace, bottomFace, rightFace, leftFace, backFace]
colors = ['y', 'b']

correctColorsQ3 = []

for face in faces:
    output = [0]*21
    blueFaces = faces.copy()
    blueFaces.remove(face)
    for pos in face:
        output[pos-1] = 'y'
    for bFace in blueFaces:
        for pos in bFace:
                output[pos-1] = 'b'
    correctColorsQ3.append(tuple(output))

def subgroup_generated_updated_Q3(tups ,gens):  
    g_elts = {}
    elts_new = {}
    elts_old = {}
    for tup in tups:
        g_elts[tup] = []
        elts_new[tup] = []
    while elts_new != {}:
        elts_old = elts_new
        elts_new = {}
        for key, value in elts_old.items():
            for y in gens:
                p = mult(key,y)
                if p not in g_elts.keys():
                    newList = value.copy()
                    newList.append(y)
                    g_elts[p] = newList
                    elts_new[p] = newList
    return g_elts

newColorDic = subgroup_generated_updated_Q3(correctColorsQ3, generators)

### Length of H ###
print('Number of States: ')
print(len(newColorDic))
print()
#Length is 3780

### MaxTurns ###
maxTurns = -1*np.inf
state = None
for key, value in newColorDic.items():
    if len(value) > maxTurns:
        maxTurns = len(value)
        state = key
print('Max Number of turns to solve any state: ')
print(maxTurns)
print()
#MaxTurns are 7

### Number of States with MaxTurns ###
numStates = 0
for key, value in newColorDic.items():
    if len(value) == maxTurns:
        numStates += 1
print('Number of states with max turns: ')
print(numStates)
print()
#Number of states with maxTurns are 3

### Average turns ###
N = len(newColorDic)
avg = 0
for key, value in newColorDic.items():
    avg += len(value)
avg = avg/N
print('Average number of turns to solve any state')
print(avg)
print()
#The average number of turns in 4.48941798941799

### Special turns to words for Q3 ###
def turnsToWordsQ3(turns):
    output = []
    for turn in turns:
        if turn == right:
            output.append('Turn Right Counter Clockwise')
        elif turn == rightInv:
            output.append('Turn Right Clockwise')

        elif turn == front:
            output.append('Turn Front Counter Clockwise')
        elif turn == frontInv:
            output.append('Turn Front Clockwise')

        elif turn == upper:
            output.append('Turn Top Counter Clockwise')
        elif turn == upperInv:
            output.append('Turn Top Clockwise')
        else:
            output.append('ERROR HAPPENED')
    return output

### Alg to solve special yellow-blue cube ###
def solveCubeYB(state):
    moves = newColorDic[state].copy()
    moves.reverse()
    words = turnsToWordsQ3(moves)
    for turn in words:
        print(turn)

### This function takes a list positions as inputs and returns a 21 length tuple with
### y at the positions and every other position being b
### so positions should be a list with the position of where the yellow colors are on the cube
def getProblemState(positions):
    output = ['b']*21
    for pos in positions:
        output[pos-1] = 'y'
    return tuple(output)