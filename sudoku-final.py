from fractions import Fraction
import copy
import ctypes
import time
num_list = list(range(1,10))
def gen_empty_matrix(row, column):
	final_matrix = []
	for i in range(0,row):
		final_matrix.append([])
		for j in range(0,column):
			final_matrix[i].append(0)
	return final_matrix
def get_possible_nums_horizontal(i,j,input_matrix):
	newmatrix = copy.deepcopy(input_matrix[i])
	del newmatrix[j]
	final_matrix = []
	for i in newmatrix:
		if i != 0:
			final_matrix.append(i)
	return set(num_list).difference(set(final_matrix))
	
def get_possible_nums_vertical(i,j,input_matrix):
	newmatrix = []
	for r in input_matrix:
		newmatrix.append(r[j])
	new_matrix = copy.deepcopy(newmatrix)
	del newmatrix[i]
	final_matrix = []
	for i in newmatrix:
		if i != 0:
			final_matrix.append(i)
	return set(num_list).difference(set(final_matrix))
	
def get_possible_nums_square(i,j,input_matrix):
	newmatrix2 = []
	final_nums = []
	if i >= 0 and i <= 2:
		newmatrix = copy.deepcopy(input_matrix[0:3])
	elif i >= 3 and i <= 5:
		newmatrix = copy.deepcopy(input_matrix[3:6])
	elif i >= 6 and i <= 8:
		newmatrix = copy.deepcopy(input_matrix[6:9])
	if j >= 0 and j <= 2:
		for row in newmatrix:
			newmatrix2.append(row[0:3])
	if j >= 3 and j <= 5:
		for row in newmatrix:
			newmatrix2.append(row[3:6])
	if j >= 6 and j <= 8:
		for row in newmatrix:
			newmatrix2.append(row[6:9])
	ni = i % 3
	nj = j % 3
	for i in range(0,3):
		for j in range(0,3):
			if ((i != ni) or (j != nj)) and newmatrix2[i][j] != 0:
				final_nums.append(newmatrix2[i][j])
	return set(num_list).difference(set(final_nums))
	
def get_possible_nums_joined(i,j,input_matrix):
	set1 = get_possible_nums_horizontal(i,j,input_matrix)
	set2 = get_possible_nums_vertical(i,j,input_matrix)
	set3 = get_possible_nums_square(i,j,input_matrix)
	return set1.intersection(set2).intersection(set3)

def fraction_to_string(number):
	num, den = Fraction(number).numerator, Fraction(number).denominator
	if den == 1:
		return str(num)
	if den != 1:
		return str(num) + "/" + str(den)
		
def is_solved_matrix(input_sd):
	input_sudoku = copy.deepcopy(input_sd)
	for i in range(0,9):
		for j in range(0,9):
			if input_sudoku[i][j] == 0:
				return "N"
	for i in range(0,9):
		for j in range(0,9):
			pn = get_possible_nums_joined(i,j,input_sudoku)
			try:
				v = list(pn)[0]
				if v != input_sudoku[i][j]:
					return "E"
			except IndexError:
				return "E"
	return "Y"

def add_with_carry_matrix(mtoadd, mmax):
	imatrix = copy.deepcopy(mtoadd)
	carry = 0
	for i in range(0,9):
		for j in range(0,9):
			if imatrix[i][j] < mmax[i][j]:
				imatrix[i][j] = imatrix[i][j] + 1
				return imatrix
			elif imatrix[i][j] == mmax[i][j]:
				imatrix[i][j] = 0
	return "F"
	
def get_pe_nums(input_sd):
	return int(str(input_sd[0][0]) + str(input_sd[0][1]) + str(input_sd[0][2]))
			
file = open("sudoku.txt", "r")
dict = {}
cur_key = ""
for line in file:
	if line[0:5] == "Grid ":
		cur_key = line[5:7]
		dict[cur_key] = []
	else:
		l = []
		for c in line[0:9]:
			l.append(int(c))
		dict[cur_key].append(l)
		
#print(dict["01"][0][2])

class sudoku(object):
	def __init__(self, init_sudoku):
		self.current_state = init_sudoku
	def print_state(self):
		input_matrix = self.current_state
		matrix_rows = len(input_matrix)
		matrix_columns = len(input_matrix[0])
		max_len = 0
		final_matrix = gen_empty_matrix(matrix_rows,matrix_columns)
		final_matrix_2 = gen_empty_matrix(matrix_rows,matrix_columns)
		for i in range(0,matrix_rows):
			for j in range(0,matrix_columns):
				try:
					string = str(input_matrix[i][j])
				except ValueError:
					string = str(input_matrix[i][j])
				orlen = len(string)
				if orlen > max_len:
					max_len = orlen
				final_matrix[i][j] = string
		for i in range(0,matrix_rows):
			for j in range(0,matrix_columns):
				string2 = final_matrix[i][j]
				while len(string2) < max_len+1:
					string2 = " " + string2
				final_matrix_2[i][j] = string2
		for row in final_matrix_2:
			outrow = "".join(row)
			print(outrow)
		return None
	def get_possible_numbers(self):
		input_sudoku = self.current_state
		new_matrix = gen_empty_matrix(9,9)
		for i in range(0,9):
			for j in range(0,9):
				if input_sudoku[i][j] == 0:
					new_matrix[i][j] = get_possible_nums_joined(i,j,input_sudoku)
				else:
					new_matrix[i][j] = "S"
		self.possible_numbers = new_matrix
	def get_possible_numbers_sorted(self):
		input_sudoku = self.current_state
		new_matrix = gen_empty_matrix(9,9)
		new_matrix_2 = gen_empty_matrix(9,9)
		for i in range(0,9):
			for j in range(0,9):
				if input_sudoku[i][j] == 0:
					tl = sorted(list(get_possible_nums_joined(i,j,input_sudoku)))
					new_matrix[i][j] = tl
					new_matrix_2[i][j] = len(tl) - 1
				else:
					tl = []
					tl.append(input_sudoku[i][j])
					new_matrix[i][j] = tl
		self.possible_numbers_sorted = new_matrix
		self.possible_numbers_sorted_amount = new_matrix_2
	def try_dumb_reduction(self):
		input_sudoku = self.current_state
		input_possible = self.possible_numbers
		new_sudoku = copy.deepcopy(self.current_state)
		found_total = 0
		for i in range(0,9):
			for j in range(0,9):
				if input_sudoku[i][j] == 0 and len(input_possible[i][j]) == 1:
					new_sudoku[i][j] = list(input_possible[i][j])[0]
					found_total += 1
		self.current_state = new_sudoku
		return found_total
	def try_dumb_only_possible_reduction_hor(self):
		input_sudoku = self.current_state
		input_possible = self.possible_numbers
		new_sudoku = copy.deepcopy(self.current_state)
		found_total = 0
		for i in range(0,9):
			for j in range(0,9):
				newer_list = []
				if input_sudoku[i][j] == 0 and len(input_possible[i][j]) > 1:
					new_list = copy.deepcopy(input_possible[i])
					del new_list[j]
					for item in new_list:
						if item != "S":
							newer_list.append(item)
					#print(newer_list)
					set = input_possible[i][j]
					for item in newer_list:
						set = set.difference(item)
						if len(set) == 0:
							break
					if len(set) == 1:
						new_sudoku[i][j] = list(set)[0]
						found_total += 1
					#new_sudoku[i][j] = list(input_possible[i][j])[0]
					#found_total += 1
		self.current_state = new_sudoku
		return found_total

	def try_dumb_only_possible_reduction_ver(self):
		input_sudoku = self.current_state
		input_possible = self.possible_numbers
		new_sudoku = copy.deepcopy(self.current_state)
		found_total = 0
		for i in range(0,9):
			for j in range(0,9):
				newer_list = []
				if input_sudoku[i][j] == 0 and len(input_possible[i][j]) > 1:
					new_list = []
					for r in input_possible:
						new_list.append(r[j])
					new_list2 = copy.deepcopy(new_list)
					del new_list2[i]
					for item in new_list2:
						if item != "S":
							newer_list.append(item)
					#print(newer_list)
					set = input_possible[i][j]
					for item in newer_list:
						set = set.difference(item)
						if len(set) == 0:
							break
					if len(set) == 1:
						new_sudoku[i][j] = list(set)[0]
						found_total += 1
					#new_sudoku[i][j] = list(input_possible[i][j])[0]
					#found_total += 1
		self.current_state = new_sudoku
		return found_total
		
	def try_dumb_only_possible_reduction_sqr(self):
		input_sudoku = self.current_state
		input_possible = self.possible_numbers
		new_sudoku = copy.deepcopy(self.current_state)
		found_total = 0
		for i in range(0,9):
			for j in range(0,9):
				if input_sudoku[i][j] == 0 and len(input_possible[i][j]) > 1:
					newmatrix2 = []
					final_nums = []
					if i >= 0 and i <= 2:
						newmatrix = copy.deepcopy(input_possible[0:3])
					elif i >= 3 and i <= 5:
						newmatrix = copy.deepcopy(input_possible[3:6])
					elif i >= 6 and i <= 8:
						newmatrix = copy.deepcopy(input_possible[6:9])
					if j >= 0 and j <= 2:
						for row in newmatrix:
							newmatrix2.append(row[0:3])
					if j >= 3 and j <= 5:
						for row in newmatrix:
							newmatrix2.append(row[3:6])
					if j >= 6 and j <= 8:
						for row in newmatrix:
							newmatrix2.append(row[6:9])
					ni = i % 3
					nj = j % 3
					for bi in range(0,3):
						for bj in range(0,3):
							if ((bi != ni) or (bj != nj)) and newmatrix2[bi][bj] != "S":
								final_nums.append(newmatrix2[bi][bj])
					newer_list = copy.deepcopy(final_nums)
					set = input_possible[i][j]
					for item in newer_list:
						set = set.difference(item)
						if len(set) == 0:
							break
					if len(set) == 1:
						new_sudoku[i][j] = list(set)[0]
						found_total += 1
					#new_sudoku[i][j] = list(input_possible[i][j])[0]
					#found_total += 1
		self.current_state = new_sudoku
		return found_total
	def is_solved(self):
		input_sudoku = self.current_state
		self.get_possible_numbers_sorted()
		input_possible = self.possible_numbers_sorted
		input_possible_amount = self.possible_numbers_sorted_amount
		for i in range(0,9):
			for j in range(0,9):
				if input_possible_amount[i][j] < 0:
					return "E"
		for i in range(0,9):
			for j in range(0,9):
				if input_sudoku[i][j] == 0:
					return "N"
		for i in range(0,9):
			for j in range(0,9):
				pn = get_possible_nums_joined(i,j,input_sudoku)
				try:
					v = list(pn)[0]
					if v != input_sudoku[i][j]:
						return "E"
				except IndexError:
					return "E"
		return "Y"
	def try_dumb_reductions_all(self):
		input_sudoku = self.current_state
		found = found_2 = found_3 = found_4 = 1
		sng = hor = ver = sqr = 0
		while found > 0 or found_2 > 0 or found_3 > 0 or found_4 > 0:
			#sudoku_1.print_state()
			self.get_possible_numbers()
			found = self.try_dumb_reduction()
			sng += found
			#print("Found by dumb: ",found)
			#sudoku_1.print_state()
			self.get_possible_numbers()
			found_2 = self.try_dumb_only_possible_reduction_hor()
			hor += found_2
			#print("Found by dumb HOR: ",found_2)
			#sudoku_1.print_state()
			self.get_possible_numbers()
			found_3 = self.try_dumb_only_possible_reduction_ver()
			ver += found_3
			#print("Found by dumb VER: ",found_3)
			#sudoku_1.print_state()
			self.get_possible_numbers()
			found_4 = self.try_dumb_only_possible_reduction_sqr()
			sqr += found_4
		#print("SNG: ", sng, " HOR: ", hor, " VER: ", ver, " SQR: ", sqr)
		cond = self.is_solved()
		if cond == "Y":
			return "Y"
		elif cond == "E":
			return "E"
		elif cond == "N":
			return "N"
	def init_brute_force(self):
		input_sudoku = self.current_state
		self.current_solved = False
		self.get_possible_numbers_sorted()
		input_possible = self.possible_numbers_sorted
		input_possible_amount = self.possible_numbers_sorted_amount
		init_mat = gen_empty_matrix(9,9)
		npamat = gen_empty_matrix(9,9)
		new_mat = gen_empty_matrix(9,9)
		psol = 1
		#for i in range(0,9):
		#	for j in range(0,9):
		#		psol *= (input_possible_amount[i][j] + 1)
		#print("Trying "+str(psol)+" solutions!")
		#print(input_possible_amount)
		#PICKING NEXT EMPTY NUMBER!
		is_done = False
		is_solved = False
		is_bad = False
		while is_done == False:
			for i in range(0,9):
				for j in range(0,9):
					if input_sudoku[i][j] == 0 and is_done == False:
						ci = i
						cj = j
						is_done = True
			if is_done == False:
				solcon = self.is_solved()
				if solcon == "Y":
					is_solved = True
					is_done = True
				if solcon == "E":
					is_done = True
					is_bad = True
		if is_solved == True:
			self.current_solved = True
			return self.current_state
		flag = False
		for i in range(0,9):
			for j in range(0,9):
				if flag == False:
					npamat[i][j] = input_possible_amount[i][j]
				else:
					npamat[i][j] = 0
				if i == ci and j == cj:
					flag = True
				
		while is_solved == False and is_bad == False:
			csol = init_mat[ci][cj]
			#print(ci,cj,csol)
			nsd = copy.deepcopy(input_sudoku)
			#print("bfinit")
			#self.print_state()
			#print()
			nsd[ci][cj] = input_possible[ci][cj][csol]
			new_s = sudoku(nsd)
			#condit = new_s.is_solved()
			condit = new_s.try_dumb_reductions_all()
			#print("afterbf")
			#new_s.print_state()
			#print(condit)
			if condit == "Y":
				is_solved = True
				self.current_solved = True
				#print("Found")
				self.current_state = new_s.current_state
				return "Y"
			elif condit == "N":
				new_s.init_brute_force()
				if new_s.current_solved == True:
					#print("Found")
					self.current_solved = True
					self.current_state = new_s.current_state
					return "Y"
			#elif condit == "E":
			#	return None
			init_mat = add_with_carry_matrix(init_mat,npamat)
			if init_mat == "F":
				return None
			#print(init_mat)
		# while is_done == False:
			# #time1 = time.time()
			# for i in range(0,9):
				# for j in range(0,9):
					# csol = init_mat[i][j]
					# new_mat[i][j] = input_possible[i][j][csol]
			# if is_solved_matrix(new_mat) == "Y":
				# is_done = True
				# self.current_state = new_mat
				# return "Done"
			# init_mat = add_with_carry_matrix(init_mat,input_possible_amount)
			# if init_mat == "F":
				# is_done = True
				# return "Failed"
			# #print(time.time() - time1)
			
	
solved = 0
failed = 0
error = 0
sum = 0
for k in sorted(list(dict.keys())):
	sd = sudoku(dict[k])
	print("---INPUT BELOW---")
	sd.print_state()
	print("Starting:")
	c = sd.try_dumb_reductions_all()
	if c == "Y":
		sd.print_state()
		print("Solved!")
		sum += get_pe_nums(sd.current_state)
		solved += 1
	elif c == "N":
		sd.print_state()
		print("Failed")
		print("Starting BF")
		sd.init_brute_force()
		if sd.current_solved == True:
			sd.print_state()
			print("Found by BF!")
			sum += get_pe_nums(sd.current_state)
			solved += 1
		else:
			print("Couldn't find by BF!")
			failed += 1
	elif c == "E":
		sd.print_state()
		print("Error!")
		error += 1
	# sudoku_1 = sudoku(dict[k])
	# sudoku_1.print_state()
	# found = 1
	# found_2 = 1
	# found_3 = 1
	# found_4 = 1
	# sng = hor = ver = sqr = 0
	# while found > 0 or found_2 > 0 or found_3 > 0 or found_4 > 0:
		# #sudoku_1.print_state()
		# sudoku_1.get_possible_numbers()
		# found = sudoku_1.try_dumb_reduction()
		# sng += found
		# #print("Found by dumb: ",found)
		# #sudoku_1.print_state()
		# sudoku_1.get_possible_numbers()
		# found_2 = sudoku_1.try_dumb_only_possible_reduction_hor()
		# hor += found_2
		# #print("Found by dumb HOR: ",found_2)
		# #sudoku_1.print_state()
		# sudoku_1.get_possible_numbers()
		# found_3 = sudoku_1.try_dumb_only_possible_reduction_ver()
		# ver += found_3
		# #print("Found by dumb VER: ",found_3)
		# #sudoku_1.print_state()
		# sudoku_1.get_possible_numbers()
		# found_4 = sudoku_1.try_dumb_only_possible_reduction_sqr()
		# sqr += found_4
	# print("SNG: ", sng, " HOR: ", hor, " VER: ", ver, " SQR: ", sqr)
	# print("Final state is:")
	# sudoku_1.print_state()
	# cond = sudoku_1.is_solved()
	# if cond == "Y":
		# solved += 1
		# print("Solved!")
	# elif cond == "N":
		# failed += 1
		# print("Failed by logic")
		# print(sudoku_1.init_brute_force())
		# sudoku_1.print_state()
		# #print(sudoku_1.possible_numbers)
	# elif cond == "E":
		# error += 1
		# print("Solved, but WRONG!")
		
print(solved, " Solved,", failed, " Failed,", error, " Errors.")
print("Sum for Project Euler is: ", sum)
time.sleep(3)
#print(get_possible_nums_horizontal(0,0,dict["01"]))
#print(get_possible_nums_vertical(0,0,dict["01"]))
#print(get_possible_nums_square(0,0,dict["01"]))
#print(get_possible_nums_joined(0,1,dict["01"]))
