import turtle
import math
import random
import copy
import time

t = turtle.Turtle()
wn = turtle.Screen()
turtle.setup(800,600)
player = 0
b = [['0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0'],['0','0','0','0','0','0','0','0']]
temp_b = [['0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', 'r', 'b', '0', '0', '0'], ['0', '0', '0', 'b', 'r', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0']]
importance = [[10,3,7,6,6,7,3,10],[3,1,3,3,3,3,1,3],[7,4,5,5,5,5,4,7],[6,3,5,0,0,5,3,6],[6,3,5,0,0,5,3,6],[7,4,5,5,5,5,4,7],[3,1,3,3,3,3,1,3],[10,3,7,6,6,7,3,10]]
t.shape('circle')
t.shapesize(2,2,2)

#def tree_(value, branches=[]):
	#return [value] + list(branches)

def root(tree):
	return tree[0]

def branches(tree):
	return tree[1:]

def is_leaf(tree):
	return not branches(tree)

def is_tree(tree):
	if type(tree) != list or len(tree) < 1 :
		return False
	for branch in branches(tree):
		if not is_tree(branch):
			return False
	return True

def print_tree(t, indent=0):
    print('  ' * indent + str(root(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def flatten(lst): #this is used to calculate the score
    candy_cane = []
    for item in lst:
        if type(item) == type([]):
            candy_cane.extend(flatten(item))
        else:
            candy_cane.append(item)
    return candy_cane

def square(n):
    t.pd() #pendown
    t.seth(0) #set heading
    t.forward(n)
    t.seth(270)
    t.forward(n)
    t.seth(180)
    t.forward(n)
    t.seth(90)
    t.forward(n)
    t.seth(0)
    t.pu()

def board(n):
    turtle.tracer(0,0)
    t.pu() #pen up
    t.goto(-200,200)
    square(400)
    for j in range(n):
        for i in range(n):
            square(400/n)
            t.forward(400/n)
        t.goto(-200,200 - (j+1) * (400/n))

def start_othello(): #delete this if you want to make your own board
    global b
    board(8)
    turtle.tracer(0,0)
    t.goto(-25,25)
    t.color('black')
    t.stamp()
    t.goto(25,-25)
    t.stamp()
    t.goto(-25,-25)
    t.color('red')
    t.stamp()
    t.goto(25,25)
    t.stamp()
    b = update_board(b,'b',3,4)
    b = update_board(b,'b',4,3)
    b = update_board(b,'r',3,3)
    b = update_board(b,'r',4,4)
    turtle.tracer(1,0)
    turtle.hideturtle()

def mid_box(x,y): #takes in the x and y cordinates and returns where the piece should stamp
    return [((((int((8/(400/(200 + x))))) - 4) * 50) + 25),((((int((8/(400/(200 + y))))) - 4) * 50) + 25)]

def mid_box2(x,y): # takes in columns and rows and returns where pieces should stamp
    return [int((x * 50) - 200) + 25, int((y * 50) - 200) + 25]

def move_done(board,x,y):
    return board[x][y] == 'b' or board[x][y] == 'r'  #returns true or false if the move is done on the board

def box_location(x,y): # x is counted left to right, y is counted bottom to the top
    if x <= -200 or x >= 200: # if it is off the board return invalid places on the board
        return [-1,-1]
    if y <= -200 or y >= 200:
        return [-1,-1]
    a = (int((8/(400/(200 + x)))))
    c = (int((8/(400/(200 + y))))) # b is already used
    return [a,c]
    #returns the row and column for the grid


def update_board(board,player,x,y): # board is a global variable called 'b' is row and column right? Shouldn't they be flopped?
    board1 = copy.deepcopy(board)
    board1[x][y] = str(player)
    return board1

def calculate_score(board,player):
    flat = flatten(board)
    return score_helper(flat,player)

def score_helper(board,player):
    if board == []:
        return 0
    if board[0] == player:
        return 1 + calculate_score(board[1:],player)
    else:
        return calculate_score(board[1:],player)

def update_score():
    t.goto()

def player_color(player):
    if player % 2 == 0:
        return 'b'
    else:
        return 'r'

def mousePressed(x,y):
    global b
    global player
    g = box_location(x,y)[0] # g and h are used because a and b are already used a == g == x AND b == g == y
    h = box_location(x,y)[1]
    if [g, h] == [-1,-1]:
        print ('not on the board')
        return
    if valid_move(player_color(player),b,g,h):
        turtle.tracer(1,0)
        t.pu()
        t.goto(mid_box(x,y)[0],mid_box(x,y)[1])
        if player % 2 == 0: #rewrite so that it is its own function?
            t.color('black')
            t.stamp()
            b = update_board(b,player_color(player),g,h)
            flip_pieces(b,player_color(player),g,h)
            if not(possible_moves(opposite_of(player_color(player)),b) == []):
                computer_move() # comment out to disable computer moves
            else:
                player += 1
        else:
            t.color('red')
            t.stamp()
            b = update_board(b,player_color(player),g,h)
            flip_pieces(b,player_color(player),g,h)
            if not(possible_moves(opposite_of(player_color(player)),b) == []):
                computer_move() # remove to disable computer moves
            else:
                player += 1
        player += 1
        temp_b = b
    else:
        print ('you cannot do this move')

def opposite_of(color): # return opposite color
    if color == 'r':
        return 'b'
    if color == 'b':
        return 'r'
    return -1

def horizontal_list(board,row):
    lst = []
    for i in range(len(b)):
        lst += [board[i][row]]
    return lst

def diagonal_list1(board,column,row): # this one goes from bottom to top from left to right
    if column == 7 or row == 7:
        return [board[column][row]]
    else:
        return [board[column][row]] + diagonal_list1(board,column + 1,row + 1)

def diagonal_list2(board,column,row): # this one goes from top to bottom from left to right
    if column == 7 or row == 0:
        return [board[column][row]]
    else:
        return [board[column][row]] + diagonal_list2(board,column + 1,row - 1)

def diagonal_list3(board,column,row): # this one goes from bottom to top from right to left
    if column == 0 or row == 7:
        return [board[column][row]]
    else:
        return [board[column][row]] + diagonal_list3(board,column - 1,row + 1)

def diagonal_list4(board,column,row): # this one goes from top to bottom from right to left
    if column == 0 or row == 0:
        return [board[column][row]]
    else:
        return [board[column][row]] + diagonal_list4(board,column - 1,row - 1)

def diagonal_check(color,board,x,y):
    if not(x == 7) and not(y == 7):
        if (diagonal_list1(board,x,y)[1] == opposite_of(color)) and (color in diagonal_list1(board,x,y)[2:]) and list_check(diagonal_list1(board,x,y)[2:],color):
            return True
    if not(x == 7) and not(y == 0):
        if (diagonal_list2(board,x,y)[1] == opposite_of(color)) and (color in diagonal_list2(board,x,y)[2:]) and list_check(diagonal_list2(board,x,y)[2:],color):
            return True
    if not(x == 0) and not(y == 7):
        if (diagonal_list3(board,x,y)[1] == opposite_of(color)) and (color in diagonal_list3(board,x,y)[2:]) and list_check(diagonal_list3(board,x,y)[2:],color):
            return True
    if not(x == 0) and not(y == 0):
        if (diagonal_list4(board,x,y)[1] == opposite_of(color)) and (color in diagonal_list4(board,x,y)[2:]) and list_check(diagonal_list4(board,x,y)[2:],color):
            return True
    return False

def list_check(lst,color):
	if lst == []:
		return True
	if lst[0] == opposite_of(color):
		return list_check(lst[1:],color)
	if lst[0] == color:
		return True
	else:
		return False

def list_check_opposite(lst,color):
	if lst == []:
		return True
	if lst[-1] == opposite_of(color):
		return list_check_opposite(lst[:-1],color)
	if lst[-1] == color:
		return True
	else:
		return False


def horizontal_check(color,board,x,y): # color should be 'b' or 'r' and is denoted by global variable player
    if not(x == 7):
        if (board[x + 1][y] == opposite_of(color)) and (color in horizontal_list(board,y)[x:]) and list_check(horizontal_list(board,y)[x + 1:],color):
                return True
    if not(x == 0):
        if (board[x - 1][y] == opposite_of(color)) and (color in horizontal_list(board,y)[:x]) and list_check_opposite(horizontal_list(board,y)[:x -1],color):
                return True
        return False

def verticle_check(color,board,x,y):
    if not(y == 7):
        if (board[x][y + 1] == opposite_of(color)) and (color in board[x][y:]) and list_check(board[x][y + 1:],color):
                return True
    if not(y == 0):
        if (board[x][y - 1] == opposite_of(color)) and (color in board[x][:y]) and list_check_opposite(board[x][:y - 1],color):
                return True
    return False

def valid_move(color,board,x,y): # x and y start at 0  FIX SO THAT IT STOPS if THERE IS A ZERO
    if move_done(board,x,y):
        return False
    if horizontal_check(color,board,x,y):
        return True
    if verticle_check(color,board,x,y):
        return True
    if diagonal_check(color,board,x,y):
        return True
    return False

def next_board(board,player,x,y):
    board = update_board(board,player,x,y)
    return board

def possible_moves(color,board):
    lst = []
    for x in range(8):
        for y in range(8):
            if valid_move(color,board,x,y):
                lst += [[x,y]]
    return lst

def temp_b_horizontal_flip1(board,player,x,y):
    global temp_b
    evaluate = horizontal_list(board,y)
    if board[x][y] == player:
        if x < 7:
            if evaluate[x + 1] == opposite_of(player) and (player in evaluate[(x + 1):]) and list_check(horizontal_list(board,y)[x + 1:],player):
                temp_b = update_board(board,player,x + 1,y)[:]
                temp_b_horizontal_flip1(temp_b,player,x + 1, y)

def horizontal_flip1(board,player,x,y):
    global b
    evaluate = horizontal_list(board,y)
    if board[x][y] == player: # this is so horizontal flip can be done recursively
        if x < 7:
            if evaluate[x + 1] == opposite_of(player) and (player in evaluate[(x + 1):]) and list_check(horizontal_list(board,y)[x + 1:],player):
                b = update_board(board,player,x + 1,y)
                t.goto(mid_box2(x + 1,y)[0],mid_box2(x + 1,y)[1])
                t.stamp()
                horizontal_flip1(b,player,x + 1, y)

def temp_b_horizontal_flip2(board,player,x,y):
    global temp_b
    evaluate = horizontal_list(board,y)
    if board[x][y] == player:
        if x > 0:
            if evaluate[x - 1] == opposite_of(player) and (player in evaluate[:(x - 1)]) and list_check_opposite(horizontal_list(board,y)[:x -1],player):
                temp_b = update_board(board,player,x - 1,y)
                temp_b_horizontal_flip2(temp_b,player,x - 1, y)

def horizontal_flip2(board,player,x,y):
    global b
    evaluate = horizontal_list(board,y)
    if board[x][y] == player:
        if x > 0:
            if evaluate[x - 1] == opposite_of(player) and (player in evaluate[:(x - 1)]) and list_check_opposite(horizontal_list(board,y)[:x -1],player):
                b = update_board(board,player,x - 1,y)
                t.goto(mid_box2(x - 1,y)[0],mid_box2(x - 1,y)[1])
                t.stamp()
                horizontal_flip2(b,player,(x - 1),y)

def temp_b_verticle_flip1(board,player,x,y):
    global temp_b
    evaluate = board[x]
    if board[x][y] == player:
        if y < 7:
            if evaluate[y + 1] == opposite_of(player) and (player in evaluate[(y + 1):]) and list_check(board[x][y + 1:],player):
                temp_b = update_board(board,player,x,y + 1)
                temp_b_verticle_flip1(temp_b,player,x,y + 1)


def verticle_flip1(board,player,x,y):
    global b
    evaluate = board[x]
    if board[x][y] == player: # this is so horizontal flip can be done recursively
        if y < 7:
            if evaluate[y + 1] == opposite_of(player) and (player in evaluate[(y + 1):]) and list_check(board[x][y + 1:],player):
                b = update_board(board,player,x,y + 1)
                t.goto(mid_box2(x,y + 1)[0],mid_box2(x,y + 1)[1])
                t.stamp()
                verticle_flip1(b,player,x,y + 1)

def temp_b_verticle_flip2(board,player,x,y):
    global temp_b
    evaluate = board[x]
    if board[x][y] == player:
        if y > 0:
            if evaluate[y - 1] == opposite_of(player) and (player in evaluate[:(y - 1)]) and list_check_opposite(board[x][:y - 1],player):
                temp_b = update_board(board,player,x,y - 1)[:]
                temp_b_verticle_flip2(temp_b,player,x,y - 1)

def verticle_flip2(board,player,x,y):
    global b
    evaluate = board[x]
    if board[x][y] == player:
        if y > 0:
            if evaluate[y - 1] == opposite_of(player) and (player in evaluate[:(y - 1)]) and list_check_opposite(board[x][:y - 1],player):
                b = update_board(board,player,x,y - 1)
                t.goto(mid_box2(x,y - 1)[0],mid_box2(x,y - 1)[1])
                t.stamp()
                verticle_flip2(b,player,x,y - 1)

def temp_b_diagonal_flip1(board,player,x,y):
    global temp_b
    if not(x == 7) and not(y == 7):
        if (diagonal_list1(board,x,y)[1] == opposite_of(player)) and (player in diagonal_list1(board,x,y)[2:]) and list_check(diagonal_list1(board,x,y)[2:],player):
            temp_b = update_board(board,player,x + 1,y + 1)[:]
            temp_b_diagonal_flip1(temp_b,player,x + 1,y + 1)

def diagonal_flip1(board,player,x,y):
    global b
    if not(x == 7) and not(y == 7):
        if (diagonal_list1(board,x,y)[1] == opposite_of(player)) and (player in diagonal_list1(board,x,y)[2:]) and list_check(diagonal_list1(board,x,y)[2:],player):
            b = update_board(board,player,x + 1,y + 1)
            t.goto(mid_box2(x + 1,y + 1)[0],mid_box2(x + 1,y + 1)[1])
            t.stamp()
            diagonal_flip1(b,player,x + 1,y + 1)

def temp_b_diagonal_flip2(board,player,x,y):
    global temp_b
    if not(x == 7) and not(y == 0):
        if (diagonal_list2(board,x,y)[1] == opposite_of(player)) and (player in diagonal_list2(board,x,y)[2:]) and list_check(diagonal_list2(board,x,y)[2:],player):
            temp_b = update_board(board,player,x + 1,y - 1)
            temp_b_diagonal_flip2(temp_b,player,x + 1,y - 1)

def diagonal_flip2(board,player,x,y):
    global b
    if not(x == 7) and not(y == 0):
        if (diagonal_list2(board,x,y)[1] == opposite_of(player)) and (player in diagonal_list2(board,x,y)[2:]) and list_check(diagonal_list2(board,x,y)[2:],player):
            b = update_board(board,player,x + 1,y - 1)
            t.goto(mid_box2(x + 1,y - 1)[0],mid_box2(x + 1,y - 1)[1])
            t.stamp()
            diagonal_flip2(b,player,x + 1,y - 1)

def temp_b_diagonal_flip3(board,player,x,y):
    global temp_b
    if not(x == 0) and not(y == 7):
        if (diagonal_list3(board,x,y)[1] == opposite_of(player)) and (player in diagonal_list3(board,x,y)[2:]) and list_check(diagonal_list3(board,x,y)[2:],player):
            temp_b = update_board(board,player,x - 1,y + 1)
            temp_b_diagonal_flip3(temp_b,player,x - 1,y + 1)

def diagonal_flip3(board,player,x,y):
    global b
    if not(x == 0) and not(y == 7):
        if (diagonal_list3(board,x,y)[1] == opposite_of(player)) and (player in diagonal_list3(board,x,y)[2:]) and list_check(diagonal_list3(board,x,y)[2:],player):
            b = update_board(board,player,x - 1,y + 1)
            t.goto(mid_box2(x - 1,y + 1)[0],mid_box2(x - 1,y + 1)[1])
            t.stamp()
            diagonal_flip3(b,player,x - 1,y + 1)

def temp_b_diagonal_flip4(board,player,x,y):
    global temp_b
    if not(x == 0) and not(y == 0):
        if (diagonal_list4(board,x,y)[1] == opposite_of(player)) and (player in diagonal_list4(board,x,y)[2:]) and list_check(diagonal_list4(board,x,y)[2:],player):
            temp_b = update_board(board,player,x - 1,y - 1)
            temp_b_diagonal_flip4(temp_b,player,x - 1,y - 1)

def diagonal_flip4(board,player,x,y):
    global b
    if not(x == 0) and not(y == 0):
        if (diagonal_list4(board,x,y)[1] == opposite_of(player)) and (player in diagonal_list4(board,x,y)[2:]) and list_check(diagonal_list4(board,x,y)[2:],player):
            b = update_board(board,player,x - 1,y - 1)
            t.goto(mid_box2(x - 1,y - 1)[0],mid_box2(x - 1,y - 1)[1])
            t.stamp()
            diagonal_flip4(b,player,x - 1,y - 1)

def flip_pieces(board,player,x,y):
	global b
	diagonal_flip1(board,player,x,y)
	diagonal_flip2(b,player,x,y)
	diagonal_flip3(b,player,x,y)
	diagonal_flip4(b,player,x,y)
	horizontal_flip1(b,player,x,y)
	horizontal_flip2(b,player,x,y)
	verticle_flip1(b,player,x,y)
	verticle_flip2(b,player,x,y)

def temp_flip_pieces(board,player,x,y):
    global temp_b
    temp_b = copy.deepcopy(update_board(board,player,x,y))
    temp_b_diagonal_flip1(temp_b,player,x,y)
    temp_b_diagonal_flip2(temp_b,player,x,y)
    temp_b_diagonal_flip3(temp_b,player,x,y)
    temp_b_diagonal_flip4(temp_b,player,x,y)
    temp_b_horizontal_flip1(temp_b,player,x,y)
    temp_b_horizontal_flip2(temp_b,player,x,y)
    temp_b_verticle_flip1(temp_b,player,x,y)
    temp_b_verticle_flip2(temp_b,player,x,y)
    return temp_b


def computer_move():
	global b
	global player
	player += 1
	p = player_color(player)
	move = minimax(tree(b,p))
	t.goto(mid_box2(move[0],move[1])[0],mid_box2(move[0],move[1])[1])
	if p == 'r':
		t.color('red')
	else:
		t.color('black')
	t.stamp()
	b = update_board(b,p,move[0],move[1])
	flip_pieces(b,p,move[0],move[1])
	if possible_moves(opposite_of(p),b) == []:
		player += 1
		computer_move()

def tree_nope(board,p,depth):
    global temp_b
    board2 = copy.deepcopy(board)
    if depth == 0:
        return []
    else:
        lst = []
        moves = possible_moves(p,board2)
        if moves == []:
            return []
        for i in moves:
            lst += tree_(temp_flip_pieces(board2,p,i[0],i[1]))
            temp_b = copy.deepcopy(board)
            lst += tree_(tree_nope((temp_flip_pieces(board2,p,i[0],i[1])),opposite_of(p),(depth - 1)))
    return lst

def bonsai(board,p,depth):
	global temp_b
	board2 = copy.deepcopy(board)
	if depth == 0:
		return []
	else:
		lst = []
		moves = possible_moves(p,board2)
		if moves == []:
			return []
		for i in moves:
			if depth == 1:
				lst += tree_(temp_flip_pieces(board2,p,i[0],i[1]))
			temp_b = copy.deepcopy(board)
			lst += tree_(bonsai((temp_flip_pieces(board2,p,i[0],i[1])),opposite_of(p),(depth - 1)))
	return lst

def evaluate(lst,color):
	lst = flatten(lst)
	lst_ = []
	counter = 0
	for i in lst:
		if not(i == 'r' or i == 'b' or i == '0'):
			lst_ += [counter]
			counter = 0
		if i == '0' or i == opposite_of(color):
			pass
		if i == color:
			counter += 1
	lst_ += [counter]
	return lst_

wn.onclick(mousePressed) #keep the stuff below at the end of the code so it is fine
start_othello()


def for_tester(list):
    lst = []
    for i in list:
        lst += [i]
    return lst


def tree1(board,p,depth=1):
	if not(len(board) == 8):
		return []
	else:
		global temp_b
		moves = possible_moves(p,board)
		lst = []
		for i in moves:
			temp_b = copy.deepcopy(board)
			lst += (temp_flip_pieces(board,p,i[0],i[1]) + [depth])
		return lst

def tree2(list_of_boards,p,depth):
	big_list = []
	if depth < 2:
		lst = []
		for i in [list_of_boards]:
			big_list += tree1(i,p,depth)
		return big_list
	else:
		for j in list_of_boards:
			big_list += tree1(j,p,depth)
			tree2(tree1(j,p,depth)[:-1],opposite_of(p),depth - 1)

def minimax(buh):
	thing = [float(0),float(0),float(0)]
	if buh == []:
		return []
	for i in buh:
		if float(i[2]) + (float(importance[0][1]/4)) > thing[2]:
			thing = i
	return 	thing

def tree(board,p,depth=1):
	moves = possible_moves(p,board)
	lst = []
	for i in moves:
		temp_b = copy.deepcopy(board)
		lst += [[i[0],i[1],calculate_score(temp_flip_pieces(board,p,i[0],i[1]),p)]]
	return lst

def pick_best(thing):
	lst = []
	counter = 0
	for i in thing:
		counter += 1
		lst += [counter,i[2]]





# things to do:
# get pieces to flip
# make computer select a random possible move so that it can play against you
