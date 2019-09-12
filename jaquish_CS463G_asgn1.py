"""
CS 463G Project 1
By Jack Jaquish
Started: 8/27/2019
Finished: 9/8/2019
"""
import copy
import itertools
import random

class cell():
	#These represent a single cell on a sudokube
	#which contain an orientation and a value
	orientation = '^'
	value = 0
	
	#defining how a cell is displayed when it is passed to print
	def __str__(self):
		return(str(self.value) + self.orientation)
	
	
class face():
	#These represent a single face on a sudokube
	#which contain 9 cell objects
	
	def __init__(self, starting_config, orientation):
		#given a starting config, and starting orientation
		#sets all the cells appropriately
		
		#initializes a 3 x 3 list of cell objects for the face
		self.cells = [[cell() for i in range(3)] for j in range(3)]
		self.starting_config = starting_config
		self.starting_orientation = orientation
		self.reset(self.starting_config, self.starting_orientation)
		
	def reset(self, starting_config, orientation):
		for index, row in enumerate(starting_config):
			for jindex, val in enumerate(row):
				self.cells[index][jindex].value = val
				self.cells[index][jindex].orientation = orientation

	def is_solved(self):
		
		#control variables for checking for solved state of a face
		solved_or = True
		solved_num = False
		
		#This is our reference for the correct orientation
		true_or = self.cells[1][1].orientation

		#this block checks all orientations and collects the face values
		#for our set check against 1-9
		checkset = set([i + 1 for i in range(9)])
		myset = set()
		for row in self.cells:
			for cell in row:
				#here we check the orientation
				if cell.orientation != true_or:
					solved_or = False

				#here we add it to our set to check the number
				myset.add(cell.value)
		if myset == checkset:
			solved_num = True
			
		return (solved_num == solved_or == True)
			
	def rotate(self, direction):
		tmp = self.cells
		if direction == 'C':
			tmp0 = self.cells[0]
			tmp1 = self.cells[1]
			tmp2 = self.cells[2]
			self.cells[0] = [tmp2[0], tmp1[0], tmp0[0]]
			self.cells[1] = [tmp2[1], tmp1[1], tmp0[1]]
			self.cells[2] = [tmp2[2], tmp1[2], tmp0[2]]

		elif direction == 'CC':
			tmp0 = self.cells[0]
			tmp1 = self.cells[1]
			tmp2 = self.cells[2]
			self.cells[0] = [tmp0[2], tmp1[2], tmp2[2]]
			self.cells[1] = [tmp0[1], tmp1[1], tmp2[1]]
			self.cells[2] = [tmp0[0], tmp1[0], tmp2[0]]
		else:
			print("Invalid rotation. ")
			return

		#fixes the orientation
		for row in self.cells:
			for cell in row:
				cell.orientation = orient(direction, cell.orientation, 'G')
	
	#display methods used for the GUI
	def display_top(self, tabs=0, spaces=0, my_end=''):
		print("\t" * tabs, " " * spaces, '[', self.cells[0][0], self.cells[0][1], self.cells[0][2], ']', sep='', end=my_end)
	def display_mid(self, tabs=0, spaces=0, my_end=''):
		print("\t" * tabs, " " * spaces, '[', self.cells[1][0], self.cells[1][1], self.cells[1][2], ']', sep='', end=my_end)
	def display_bot(self, tabs=0, spaces=0, my_end=''):
		print("\t" * tabs, " " * spaces, '[', self.cells[2][0], self.cells[2][1], self.cells[2][2], ']', sep='', end=my_end)

				
class sudokube():
	#represents the entire sudokube, which contains
	#six face objects

	def __init__(self):
			#initializes the faces to their starting configurations
		self.front = face([[1,5,2],[4,6,3],[7,8,9]], '^')
		self.left = face([[3,8,7],[2,1,9],[5,6,4]], '^')
		self.back = face([[4,3,6],[7,5,1],[9,2,8]], '^')
		self.right = face([[8,6,3],[2,1,9],[4,5,7]], '>')
		self.top = face([[9,7,1],[2,4,8],[5,3,6]], '^')
		self.bottom = face([[5,9,6],[3,7,8],[2,4,1]], 'v')
		
	def move(self, face, direction):
		#Here is a single move, where a face and direction are specified
		#i ran out of time to do this in a clever way, so it is just an extremely
		#long method where I do everything by hand. :shrug:
		if face == "F":
			if direction == 'C': #THIS CASE IS DONE
				self.front.rotate(direction)
				for i in range(3):
					self.top.cells[2][i].orientation = orient(direction, self.top.cells[2][i].orientation, 'G')
					self.right.cells[i][0].orientation = orient(direction, self.right.cells[i][0].orientation, 'G')
					self.bottom.cells[0][i].orientation = orient(direction, self.bottom.cells[0][i].orientation, 'G')
					self.left.cells[i][2].orientation = orient(direction, self.left.cells[i][2].orientation, 'G')
				#move
				tmp = copy.deepcopy(self.top.cells)
				for i in range(3):
					self.top.cells[2][i] = self.left.cells[2-i][2]
				for i in range(3):
					self.left.cells[2-i][2] = self.bottom.cells[0][2-i]
				for i in range(3):
					self.bottom.cells[0][2-i] = self.right.cells[i][0]
				for i in range(3):
					self.right.cells[i][0] = tmp[2][i]	
					
			elif direction == 'CC': #THIS CASE IS DONE
				self.front.rotate(direction)
				for i in range(3):
					self.top.cells[2][i].orientation = orient(direction, self.top.cells[2][i].orientation, 'G')
					self.right.cells[i][0].orientation = orient(direction, self.right.cells[i][0].orientation, 'G')
					self.bottom.cells[0][i].orientation = orient(direction, self.bottom.cells[0][i].orientation, 'G')
					self.left.cells[i][2].orientation = orient(direction, self.left.cells[i][2].orientation, 'G')
				#move
				tmp = copy.deepcopy(self.top.cells)
				for i in range(3):
					self.top.cells[2][i] = self.right.cells[i][0]
				for i in range(3):
					self.right.cells[i][0] = self.bottom.cells[0][2-i]
				for i in range(3):
					self.bottom.cells[0][i] = self.left.cells[i][2]
				for i in range(3):
					self.left.cells[2-i][2] = tmp[2][i]	
			else:
				print("Invalid direction specified, no move made. ")

		elif face == "L":
			if direction == 'C': #THIS CASE IS DONE
				self.left.rotate(direction)
				for i in range(3):
					self.back.cells[i][2].orientation = rev_orient(self.back.cells[i][2].orientation)
					self.bottom.cells[i][0].orientation = rev_orient(self.bottom.cells[i][0].orientation)
				#move
				tmp = copy.deepcopy(self.top.cells)
				for i in range(3):
					self.top.cells[i][0] = self.back.cells[2-i][2]
				for i in range(3):
					self.back.cells[i][2] = self.bottom.cells[2-i][0]
				for i in range(3):
					self.bottom.cells[i][0] = self.front.cells[i][0]
				for i in range(3):
					self.front.cells[i][0] = tmp[i][0]	
			
			elif direction == 'CC': #THIS CASE IS DONE
				self.left.rotate(direction)
				for i in range(3):
					self.back.cells[i][2].orientation = rev_orient(self.back.cells[i][2].orientation)
					self.top.cells[i][0].orientation = rev_orient(self.top.cells[i][0].orientation)
				#move
				tmp = copy.deepcopy(self.top.cells)
				for i in range(3):
					self.top.cells[i][0] = self.front.cells[i][0]
				for i in range(3):
					self.front.cells[i][0] = self.bottom.cells[i][0]
				for i in range(3):
					self.bottom.cells[i][0] = self.back.cells[2-i][2]
				for i in range(3):
					self.back.cells[i][2] = tmp[2-i][0]
			else:
				print("Invalid direction specified, no move made. ")
				
		elif face == "B":
			if direction == 'C':
				self.back.rotate(direction)
				for i in range(3):
					self.top.cells[0][i].orientation = orient('CC', self.top.cells[0][i].orientation, 'G')
					self.right.cells[i][2].orientation = orient('CC', self.right.cells[i][2].orientation, 'G')
					self.bottom.cells[2][i].orientation = orient('CC', self.bottom.cells[2][i].orientation, 'G')
					self.left.cells[i][0].orientation = orient('CC', self.left.cells[i][0].orientation, 'G')
				#move
				tmp = copy.deepcopy(self.top.cells)
				for i in range(3):
					self.top.cells[0][i] = self.right.cells[i][2]
				for i in range(3):
					self.right.cells[i][2] = self.bottom.cells[2][2-i]
				for i in range(3):
					self.bottom.cells[2][i] = self.left.cells[i][0]
				for i in range(3):
					self.left.cells[2-i][0] = tmp[0][i]	
			elif direction == 'CC': #THIS CASE IS DONE
				self.back.rotate(direction)
				for i in range(3):
					self.top.cells[0][i].orientation = orient('C', self.top.cells[0][i].orientation, 'G')
					self.right.cells[i][2].orientation = orient('C', self.right.cells[i][2].orientation, 'G')
					self.bottom.cells[2][i].orientation = orient('C', self.bottom.cells[2][i].orientation, 'G')
					self.left.cells[i][0].orientation = orient('C', self.left.cells[i][0].orientation, 'G')
				#move
				tmp = copy.deepcopy(self.top.cells)
				for i in range(3):
					self.top.cells[0][i] = self.left.cells[2-i][0]
				for i in range(3):
					self.left.cells[2-i][0] = self.bottom.cells[2][2-i]
				for i in range(3):
					self.bottom.cells[2][2-i] = self.right.cells[i][2]
				for i in range(3):
					self.right.cells[i][2] = tmp[0][i]	
			else:
				print("Invalid direction specified, no move made. ")
				
		elif face == "R":
			if direction == 'C': #THIS CASE IS CONDE
				#rotate the face
				self.right.rotate(direction)
				for i in range(3):
					self.back.cells[i][0].orientation = rev_orient(self.back.cells[i][0].orientation)
					self.top.cells[i][2].orientation = rev_orient(self.top.cells[i][2].orientation)
				#move
				tmp = copy.deepcopy(self.top.cells)
				for i in range(3):
					self.top.cells[i][2] = self.front.cells[i][2]
				for i in range(3):
					self.front.cells[i][2] = self.bottom.cells[i][2]
				for i in range(3):
					self.bottom.cells[i][2] = self.back.cells[2-i][0]
				for i in range(3):
					self.back.cells[i][0] = tmp[2-i][2]
					
			elif direction == 'CC': #THIS CASE IS DONE
				self.right.rotate(direction)
				#reverse orientations of things that will need it
				for i in range(3):
					self.back.cells[i][0].orientation = rev_orient(self.back.cells[i][0].orientation)
					self.bottom.cells[i][2].orientation = rev_orient(self.bottom.cells[i][2].orientation)
				#move
				tmp = copy.deepcopy(self.top.cells)
				for i in range(3):
					self.top.cells[i][2] = self.back.cells[2-i][0]
				for i in range(3):
					self.back.cells[i][0] = self.bottom.cells[2-i][2]
				for i in range(3):
					self.bottom.cells[i][2] = self.front.cells[i][2]
				for i in range(3):
					self.front.cells[i][2] = tmp[i][2]
			else:
				print("Invalid direction specified, no move made. ")
				
		elif face == "U":
			if direction == 'C':
				self.top.rotate(direction)
				#move
				tmp = copy.deepcopy(self.front.cells)
				for i in range(3):
					self.front.cells[0][i] = self.right.cells[0][i]
				for i in range(3):
					self.right.cells[0][i] = self.back.cells[0][i]
				for i in range(3):
					self.back.cells[0][i] = self.left.cells[0][i]
				for i in range(3):
					self.left.cells[0][i] = tmp[0][i]
			elif direction == 'CC':
				self.top.rotate(direction)
				tmp = copy.deepcopy(self.front.cells)
				for i in range(3):
					self.front.cells[0][i] = self.left.cells[0][i]
				for i in range(3):
					self.left.cells[0][i] = self.back.cells[0][i]
				for i in range(3):
					self.back.cells[0][i] = self.right.cells[0][i]
				for i in range(3):
					self.right.cells[0][i] = tmp[0][i]
			else:
				print("Invalid direction specified, no move made. ")
				
		elif face == "D":
			if direction == 'C':
				self.bottom.rotate(direction)
				tmp = copy.deepcopy(self.front.cells)
				for i in range(3):
					self.front.cells[2][i] = self.left.cells[2][i]
				for i in range(3):
					self.left.cells[2][i] = self.back.cells[2][i]
				for i in range(3):
					self.back.cells[2][i] = self.right.cells[2][i]
				for i in range(3):
					self.right.cells[2][i] = tmp[2][i]
			elif direction == 'CC':
				self.bottom.rotate(direction)
				tmp = copy.deepcopy(self.front.cells)
				for i in range(3):
					self.front.cells[2][i] = self.right.cells[2][i]
				for i in range(3):
					self.right.cells[2][i] = self.back.cells[2][i]
				for i in range(3):
					self.back.cells[2][i] = self.left.cells[2][i]
				for i in range(3):
					self.left.cells[2][i] = tmp[2][i]
			else:
				print("Invalid direction specified, no move made. ")
				
		else:
			print("Invalid face specified, no move made. ")		
		
	def randomize(self, k):
		#display the base state
		self.display()
		#base list of possible faces and turn directions
		faces = ['F', 'L', 'B', 'R', 'U', 'D']
		moves = ['C', 'CC']
		
		#we now have an ordered list of all possible moves
		all_moves = list(itertools.product(faces,moves))
		my_prev_move = None
		for i in range(k):
			my_move = random.choice(all_moves)
			if my_prev_move != None:
				if my_move[1] == 'C':
					while my_move[0] == my_prev_move[0] and my_prev_move[1] == 'CC':
						my_move = random.choice(all_moves)
				else:
					while my_move[0] == my_prev_move[0] and my_prev_move[1] == 'C':
						my_move = random.choice(all_moves)
			my_prev_move = my_move
			self.move(my_move[0], my_move[1])
			print(my_move)
			self.display()
		
	
	def display(self):
		#First 3 rows
		self.top.display_top(tabs=1, my_end='\n')
		self.top.display_mid(tabs=1, my_end='\n')
		self.top.display_bot(tabs=1, my_end='\n')
	
		#Next 3 rows
		self.left.display_top()
		self.front.display_top()
		self.right.display_top()
		self.back.display_top(my_end='\n')
		
		self.left.display_mid()
		self.front.display_mid()
		self.right.display_mid()
		self.back.display_mid(my_end='\n')
		
		self.left.display_bot()
		self.front.display_bot()
		self.right.display_bot()
		self.back.display_bot(my_end='\n')
		
		#Last 3 rows
		self.bottom.display_top(tabs=1, my_end='\n')
		self.bottom.display_mid(tabs=1, my_end='\n')
		self.bottom.display_bot(tabs=1, my_end='\n')
		
	def is_solved(self):
		#checks the solved state of each face on the cube.
		#if they're all solved, returns True, else returns False
		return (self.front.is_solved() == self.left.is_solved() == self.back.is_solved()
				   == self.right.is_solved() == self.top.is_solved() == self.bottom.is_solved()
				   == True)
	
	
def orient(direction, cur_orientation, perspective):

	#This handles changing the orientation in a simple manner
	#so I don't have to think about it, and I can include as many
	#cases as I need.
	
	#clockwise case
	c_ors = ['^', '>', 'v', '<']
	
	#counterclockwise case
	cc_ors = ['^', '<', 'v', '>']
	
	if direction == 'C' and perspective == 'G':
		progression = c_ors
	elif direction == 'CC' and perspective == 'G':
		progression = cc_ors
		
	for i in range(len(progression)):
		if cur_orientation == progression[i]:
			if i != 3:
				return progression[i+1]
			else:
				return progression[0]

def rev_orient(cur_orientation):
	#Using the dictionary feature, the point of this is simply
	#to return the opposite direction. Useful for the left
	#and right face rotations.
	mydict = {
	'^': 'v',
	'v': '^',
	'<': '>',
	'>': '<'
	}
	return mydict[cur_orientation]


def main():

	choice = input("Enter 'Q' to quit, 'P' to play, and 'K' to play randomly..")
	
	if choice == 'Q':
		return
	elif choice == 'P':
		sk = sudokube()
		sk.display()
		
		while True:
			face = input("Enter the face you wish to move (L, R, U, D, F, B) (or type Quit to quit): ")
			if face == 'Quit':
				return
			direction = input("Enter the direction (C, CC) you want to move the face {}: ".format(face))
			sk.move(face, direction)
			sk.display()
	elif choice == 'K':
		while True:
			k = input('Enter a valid integer (or type Quit to quit):')
			if k == 'Quit':
				return
			else:
				
				try:
					x = int(k)
					sk = sudokube()
					sk.randomize(x)
				except ValueError as e:
					print(e)

if __name__ == '__main__':
	main()

