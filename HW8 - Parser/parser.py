import sys

# TODO If word isn't in grammar, catch so dictionary access doesn't cause error

class Node():
	def __init__(self, terminal, tree):
		self.terminal = terminal
		self.pointer = tree

def main():
	grammarRaw = sys.argv[1] # Filename
	sentence = sys.argv[2]
	grammar = get_grammar(grammarRaw)
	tokens = sentence.split()
	N = len(tokens) #N is number of words in sentence
	# fill with 0
	table = [[[] for i in range(N + 1)] for j in range(N+1)]
	table = fillTable(table, tokens, grammar)
	for finalParse in table[0][N]:
		if finalParse.terminal == "S":
			print("S")

#def printTree()
def fillTable(table, tokens, grammar):
	N = len(tokens)
	print(grammar)
	for i in range(N):
		table[i][i+1] = []
		productions = grammar[(tokens[i], )]
		for production in productions:
			table[i][i+1].append(Node(production, None)) #List of all possible terminals matching with token 
	for i in range(1, N+1):
		for j in range(N+1-i): #This is to go diagonally
			for k in range(j+1, i):
				BList = table[j][k] # Get back a list of Nodes
				CList = table[k][i]
				for B in BList:
					for C in CList: # Note: B and C are node object containing the terminal and its pointer
						if (B.terminal, C.terminal) in grammar:
							productions = grammar[(B.terminal, C.terminal)]
							for production in productions:
								table[j][i].append(Node(production, [B, C]))

	return table 

def get_grammar(grammar_filename):
	"""Takes in a filename and returns a dictionary of rules in the format
	   tuple of right hand side: string of left hand side"""
	grammar_file = open(grammar_filename, 'r')
	grammar_dict = {}
	lhs_rhs_dict = {}
	for rule in grammar_file:

		# Get left-hand side and right-hand side of the rule
		divide_rule = rule.strip("\n").split("->")
		left_hand_side = divide_rule[0].strip()
		right_hand_side = divide_rule[1].strip().split(" ")

		# Add rule to dictionary
		if tuple(right_hand_side) not in grammar_dict:
			grammar_dict[tuple(right_hand_side)] = [left_hand_side]
		else:
			grammar_dict[tuple(right_hand_side)].append(left_hand_side)
		if left_hand_side not in lhs_rhs_dict:
			lhs_rhs_dict[left_hand_side] = [tuple(right_hand_side)]
		else:
			lhs_rhs_dict[left_hand_side].append(tuple(right_hand_side))

	# If a rule is a unit production, duplicate rules to conform to CNF
	grammar_removal_list = []
	grammar_deletion_list = []
	for lhs in lhs_rhs_dict:
		for rhs in lhs_rhs_dict[lhs]:
			if len(rhs) == 1 and rhs[0] != rhs[0].lower(): 
				# Unit production
				print("unit production rule:", lhs, "->", rhs)

				# First, for X -> Y, copy all rules X -> AB to Y -> AB
				for possible_repeated_lhs in lhs_rhs_dict:
					if possible_repeated_lhs == rhs:
						for repeated_rule in lhs_rhs_dict[possible_repeated_lhs]:
							lhs_rhs_dict[lhs].append(repeated_rule)
							grammar_dict[repeated_rule].append(lhs)

				# Prepare to remove the unit production rules after the loops
				grammar_removal_list.append((rhs, lhs))
				if len(grammar_dict[rhs]) == 1: # Will be 0 after removal
					print("Will delete rhs", rhs)
					grammar_deletion_list.append(rhs)

	for item in grammar_removal_list:
		grammar_dict[item[0]].remove(item[1])
	for item in grammar_deletion_list:
		grammar_dict.pop(item)


	#print("LHS dict:\n", lhs_rhs_dict)
	#print("Grammar dict:\n", grammar_dict)
	return grammar_dict

# def main():
# 	grammar_filename = sys.argv[1]
# 	grammar_dict = get_grammar(grammar_filename)
# 	#print(grammar_dict)

if __name__ == "__main__":
	main()

