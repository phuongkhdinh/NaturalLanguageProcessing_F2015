import sys
class Node():
	self.terminal = None
	self.pointer = None
	def __init__(self, terminal, tree):
		self.terminal = terminal
		self.pointer = tree



def main(sentence, grammarRaw):
	
	grammar = getGrammar(grammarRaw)
	tokens = sentence.split()
	N = len(tokens) #N is number of words in sentence
	# fill with 0
	table = [[0 for i in range(N + 1)] for j in range(N+1)]
	table = fillTable(table, tokens, grammar)
	print(table[0,N])


def fillTable(table, tokens, grammar):
	N = len(tokens)
	for i in range(N):
		table[i][i+1] = []
		productions = grammar[(tokens[i])]
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
							productions = grammar[(B, C)]
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
	lhs_deletion_list = []
	grammar_deletion_list = []
	for lhs in lhs_rhs_dict:
		for rhs in lhs_rhs_dict[lhs]:
			if len(rhs) == 1 and rhs[0] != rhs[0].lower(): # Unit production
				for possible_repeated_lhs in lhs_rhs_dict:
					if possible_repeated_lhs == rhs:
						for repeated_rule in lhs_rhs_dict[possible_repeated_lhs]:
							lhs_rhs_dict[lhs].append(repeated_rule)
							grammar_dict[repeated_rule].append(lhs)
				grammar_dict[rhs].remove(lhs)
				if grammar_dict[rhs] == []:
					grammar_deletion_list.append(rhs)
				lhs_rhs_dict[lhs].remove(rhs)
				if lhs_rhs_dict[lhs] == []:
					lhs_deletion_list.append(lhs)
	for item in lhs_deletion_list:
		lhs_rhs_dict.pop(item)
	for item in grammar_deletion_list:
		grammar_dict.pop(item)


	print("LHS dict:\n", lhs_rhs_dict)
	print("Grammar dict:\n", grammar_dict)
	return grammar_dict

def main():
	grammar_filename = sys.argv[1]
	grammar_dict = get_grammar(grammar_filename)
	#print(grammar_dict)

if __name__ == "__main__":
	main()

