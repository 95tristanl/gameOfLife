import random
import time
from copy import copy, deepcopy
import math


def gameOfLife(dim, level, iter, timestep, iterType):
	matrix = [ [0] * dim for i in range(dim) ] # create matrix
	initState(dim, matrix, level) # create init matrix state

	if iterType == 'I':
		print("InstantChange:")
		iterate_instantChange(dim, matrix, iter, timestep)
	elif iterType == 'W':
		print("WaveChange:")
		iterate_waveChange(dim, matrix, iter, timestep)
	elif iterType == 'R':
		print("RandomChange:")
		iterate_randomChange(dim, matrix, iter, timestep)

	print("")
	print("Done")
	return matrix


def initState(dim, matrix, level):
	c = 0
	for l in range(level): # keep narrowing down 1's per state level. The more levels, the less amount of 1's = live cells
		for y in range(dim):
			for x in range(dim):
				if l == 0:
					r = random.randint(0, 1)  # 0 or 1
					matrix[y][x] = r
					if r == 1:
						c += 1
				elif (l > 0 and matrix[y][x] == 1): # after first init state
					r = random.randint(0, 1)  # 0 or 1
					matrix[y][x] = r
					c -= 1
					if r == 1:
						c +=1
	print("Matrix size: " + str(dim*dim))
	print("Start: " + str(c))


#changes take place based on exact previous state, not based on it as it changes through the state iteratively
# basically it 'looks' like the changes are made in an instant based on previous state/window/iteration
def iterate_instantChange(dim, matrix, iter, timestep):
	printSideBySide(dim, matrix, 0)
	time.sleep(timestep)  # sleep for 2 seconds before next iteration
	for i in range(iter):
		matrix_copy = deepcopy(matrix) # dont want to change the prev state while changing the current state => matrix_copy
		# - - - - - Disease
		dis_x = random.randint(0, dim - 1)
		dis_y = random.randint(0, dim - 1)
		# - - - - - Disease
		# - - - - - Good Health
		num_gh = random.randint(0, math.ceil(dim / 5) + 3)
		gh_stack = []
		for j in range(num_gh):
			gh_x = random.randint(0, dim - 1)
			gh_y = random.randint(0, dim - 1)
			tup = [gh_y, gh_x]
			while tup in gh_stack:
				gh_x = random.randint(0, dim - 1)
				gh_y = random.randint(0, dim - 1)
				tup = [gh_y, gh_x]
			gh_stack.append(tup)  # if tup not in stack
		gh_stack.sort()
		# - - - - - Good Health
		dc = 0 # death counter
		lc = 0 # life/born counter
		sa = 0 # still alive
		for y in range(dim):
			for x in range(dim):
				neighs = getNeighbors([x, y], dim, matrix)
				it = matrix[y][x]
				# - - - - - Good Health
				if it >= 1 and neighs >= 1 and len(gh_stack) > 0 and gh_stack[0] == [y, x]: # life
					matrix_copy[y][x] = 1
					sa += 1
				# - - - - - Good Health
				elif it >= 1 and neighs < 2:  # death
					matrix_copy[y][x] = -1
					dc += 1
				elif it >= 1 and neighs > 3:  # death
					matrix_copy[y][x] = -2
					dc += 1
				elif it <= 0 and neighs == 3:  # life
					matrix_copy[y][x] = 2
					lc += 1
				elif it >= 1 and (neighs == 2 or neighs == 3):  # life
					matrix_copy[y][x] = 1
					sa += 1
				elif it <= 0:  # reset to 0
					matrix_copy[y][x] = 0
				# - - - - - Disease
				if y == dis_y and x == dis_x:
					if matrix[dis_y][dis_x] >= 1:  # disease kills that cell
						if matrix[dis_y][dis_x] == 1:
							sa -= 1
						elif matrix[dis_y][dis_x] == 2:
							lc -= 1
						matrix_copy[dis_y][dis_x] = -3
						dc += 1
					else:
						matrix_copy[dis_y][dis_x] = -4
				# - - - - -
		matrix = matrix_copy  # done changing cur state = matrix_copy, so copy becomes next state
		printSideBySide(dim, matrix, i + 1)
		print("Born: " + str(lc) + "   Survived: " + str(sa) + "   Died: " + str(dc) +
			  "   Total Alive: " + str(lc + sa) + "   Net: " + str(lc-dc))
		time.sleep(timestep)  # sleep for 2 seconds before next iteration


# changes are made iteratively based on previous state
# (changes made during this window/itereation affect later changes in this window/iteration)
def iterate_waveChange(dim, matrix, iter, timestep):
	printSideBySide(dim, matrix, 0)
	time.sleep(timestep)  # sleep for 2 seconds before next iteration
	for i in range(iter):
		# - - - - - Disease
		dis_x = random.randint(0, dim - 1)
		dis_y = random.randint(0, dim - 1)
		# - - - - - Disease
		# - - - - - Good Health
		num_gh = random.randint(0, math.ceil(dim / 5) + 3)
		gh_stack = []
		for j in range(num_gh):
			gh_x = random.randint(0, dim - 1)
			gh_y = random.randint(0, dim - 1)
			tup = [gh_y, gh_x]
			while tup in gh_stack:
				gh_x = random.randint(0, dim - 1)
				gh_y = random.randint(0, dim - 1)
				tup = [gh_y, gh_x]
			gh_stack.append(tup)  # if tup not in stack
		gh_stack.sort()
		# - - - - - Good Health
		dc = 0 # death counter
		lc = 0 # life/born counter
		sa = 0 # still alive
		for y in range(dim):
			for x in range(dim):
				neighs = getNeighbors([x, y], dim, matrix)
				it = matrix[y][x]
				# - - - - - Good Health
				if it >= 1 and neighs >= 1 and len(gh_stack) > 0 and gh_stack[0] == [y, x]: # life
					matrix[y][x] = 1
					sa += 1
				# - - - - - Good Health
				elif it >= 1 and neighs < 2:  # death
					matrix[y][x] = -1
					dc += 1
				elif it >= 1 and neighs > 3:  # death
					matrix[y][x] = -2
					dc += 1
				elif it <= 0 and neighs == 3:  # life
					matrix[y][x] = 2
					lc += 1
				elif it >= 1 and (neighs == 2 or neighs == 3):  # life
					matrix[y][x] = 1
					sa += 1
				elif it <= 0:  # reset to 0
					matrix[y][x] = 0
				# - - - - - Disease
				if y == dis_y and x == dis_x:
					if matrix[dis_y][dis_x] >= 1:  # disease kills that cell
						if matrix[dis_y][dis_x] == 1:
							sa -= 1
						elif matrix[dis_y][dis_x] == 2:
							lc -= 1
						matrix[dis_y][dis_x] = -3
						dc += 1
					else:
						matrix[dis_y][dis_x] = -4
				# - - - - -
		printSideBySide(dim, matrix, i + 1)
		print("Born: " + str(lc) + "   Survived: " + str(sa) + "   Died: " + str(dc) +
			  "   Total Alive: " + str(lc + sa) + "   Net: " + str(lc-dc))
		time.sleep(timestep)  # sleep for 2 seconds before next iteration


# randomly choose dim^2 locations (could repeat or not)
# basically, each iterative step, this will choose a random location to update so per a given 'window iteration'
# dim*dim locations will be chosen just like the ther types of iterate methods but locations can repeat or they
# may never be updated at all
def iterate_randomChange(dim, matrix, iter, timestep):
	printSideBySide(dim, matrix, 0)
	time.sleep(timestep)  # sleep for 2 seconds before next iteration
	for i in range(iter):
		# - - - - - Disease     Kill a random cell in matrix per iteration/window
		dis_x = random.randint(0, dim - 1)
		dis_y = random.randint(0, dim - 1)
		# - - - - - Disease
		# - - - - - Good Health   Make some amount of cells (proportional to matrix size) stay alive if it has >=1 neighbor
		num_gh = random.randint(0, math.ceil(dim / 5) + 3)
		gh_stack = []
		for j in range(num_gh):
			gh_x = random.randint(0, dim - 1)
			gh_y = random.randint(0, dim - 1)
			tup = [gh_y, gh_x]
			while tup in gh_stack:
				gh_x = random.randint(0, dim - 1)
				gh_y = random.randint(0, dim - 1)
				tup = [gh_y, gh_x]
			gh_stack.append(tup)  # if tup not in stack
		gh_stack.sort()
		# - - - - - Good Health
		dc = 0  # death counter
		lc = 0  # life/born counter
		sa = 0  # still alive
		for z in range(dim*dim): #dim*dim random locations to update
			x = random.randint(0, dim - 1)
			y = random.randint(0, dim - 1)
			neighs = getNeighbors([x, y], dim, matrix)
			it = matrix[y][x]
			# - - - - - Good Health
			if it >= 1 and neighs >= 1 and len(gh_stack) > 0 and gh_stack[0] == [y, x]:  # life
				matrix[y][x] = 1
				sa += 1
			# - - - - - Good Health
			elif it >= 1 and neighs < 2:  # death
				matrix[y][x] = -1
				dc += 1
			elif it >= 1 and neighs > 3:  # death
				matrix[y][x] = -2
				dc += 1
			elif it <= 0 and neighs == 3:  # life
				matrix[y][x] = 2
				lc += 1
			elif it >= 1 and (neighs == 2 or neighs == 3):  # life
				matrix[y][x] = 1
				sa += 1
			elif it <= 0:  # reset to 0
				matrix[y][x] = 0
			# - - - - - Disease
			if y == dis_y and x == dis_x:
				if matrix[dis_y][dis_x] >= 1:  # disease kills that cell
					if matrix[dis_y][dis_x] == 1:
						sa -= 1
					elif matrix[dis_y][dis_x] == 2:
						lc -= 1
					matrix[dis_y][dis_x] = -3
					dc += 1
				else:
					matrix[dis_y][dis_x] = -4
		# - - - - -
		printSideBySide(dim, matrix, i + 1)
		print("Born: " + str(lc) + "   Survived: " + str(sa) + "   Died: " + str(dc) +
			  "   Total Alive: " + str(lc + sa) + "   Net: " + str(lc - dc))
		time.sleep(timestep)  # sleep for 2 seconds before next iteration


# the matrix 'wraps around' so a location of 0,0 on a 4 by 4 matrix will have neighbors:
# 1,0 , 1,1 , 0,1 , 3,0 , 0,3 , 3,3 , 3,1 , 1,3
def getNeighbors(pos, dim, matrix):
	x = pos[0]
	y = pos[1]
	counter = 0
	# if there is a 1 in any of the neighboring positions (accounting for wrapping around the matrix) inc counter
	if matrix[(y-1)%dim][(x-1)%dim] == 1: # upper left
		counter += 1
	if matrix[(y-1)%dim][x] == 1:         # above
		counter += 1
	if matrix[(y-1)%dim][(x+1)%dim] == 1: # upper right
		counter += 1
	if matrix[y][(x-1)%dim] == 1:         # left
		counter += 1
	if matrix[y][(x+1)%dim] == 1:         # right
		counter += 1
	if matrix[(y+1)%dim][(x-1)%dim] == 1: # lower left
		counter += 1
	if matrix[(y+1)%dim][x] == 1:         # below
		counter += 1
	if matrix[(y+1)%dim][(x+1)%dim] == 1: # lower right
		counter += 1
	return counter


def printMatrix(dim, matrix, iter):
	print("ITER: " + str(iter))
	for y in range(dim):
		for x in range(dim):
			if matrix[y][x] <= 0:
				print(" .", end="")
			else:
				print(" @", end="")
		print("")


def printDetailedMatrix(dim, matrix, iter):
	print("ITER: " + str(iter))
	for y in range(dim):
		for x in range(dim):
			if matrix[y][x] == 0:
				print(" .", end="")
			elif matrix[y][x] == 1:
				print(" @", end="")
			elif matrix[y][x] == 2:
				print(" *", end="")
			elif matrix[y][x] == -1:
				print(" x", end="")
			elif matrix[y][x] == -2:
				print(" X", end="")
			elif matrix[y][x] == -3:
				print(" !", end="")
			elif matrix[y][x] == -4:
				print(" -", end="")
		print("")

def printSideBySide(dim, matrix, iter):
	print("")
	print("ITER: " + str(iter))
	for y in range(dim):
		for x in range(dim):
			if matrix[y][x] == 0:
				print(" .", end="")
			elif matrix[y][x] == 1:
				print(" @", end="")
			elif matrix[y][x] == 2:
				print(" *", end="")
			elif matrix[y][x] == -1:
				print(" x", end="")
			elif matrix[y][x] == -2:
				print(" X", end="")
			elif matrix[y][x] == -3:
				print(" !", end="")
			elif matrix[y][x] == -4:
				print(" -", end="")
		print("     ", end="")
		for x in range(dim):
			if matrix[y][x] <= 0:
				print(" .", end="")
			else:
				print(" @", end="")
		print("")

#params:
# matrix dim (size),
# level (lower the level, the more live cells will start),
# iterations/number of life step windows,
# timestep in sec before next iteration/window is shown,
# iterType: 'I' : instantChange , 'W' : waveChange , 'R' : randomChange
gameOfLife(25, 3, 10, 5, 'W')
