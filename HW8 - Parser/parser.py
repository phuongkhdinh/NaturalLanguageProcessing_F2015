"""
parser.py
By Phuong Dinh and Julia Kroll
Implements the CKY algorithm
Takes in a grammar file and a sentence, 
and prints all grammatical parses of the sentence.
"""

import sys

class Node():
	"""Helper class to track backpointers to reconstruct parse trees"""
	def __init__(self, terminal, tree):
		self.terminal = terminal
		self.pointer = tree

def get_grammar(grammar_filename):
	"""Takes in a filename and returns a dictionary of rules in the format
	   tuple of right hand side: string of left hand side"""
	grammar_file = open(grammar_filename, 'r')
	grammar_dict = {}
	lhs_rhs_dict = {}

	for rule in grammar_file:

		# Get left-hand side and right-hand side of the rule
		divide_rule = rule.strip("\n").split("->") # NP -> DT NN
		left_hand_side = divide_rule[0].strip()
		right_hand_side = divide_rule[1].strip()
		rhs_elements = right_hand_side.split("|") # john | cat | bunny

		for rhs_element in rhs_elements:
			# Add rule to dictionary
			rhs_element = rhs_element.strip().split(" ")
			if tuple(rhs_element) not in grammar_dict:
				grammar_dict[tuple(rhs_element)] = [left_hand_side]
			else:
				grammar_dict[tuple(rhs_element)].append(left_hand_side)
			if left_hand_side not in lhs_rhs_dict:
				lhs_rhs_dict[left_hand_side] = [tuple(rhs_element)]
			else:
				lhs_rhs_dict[left_hand_side].append(tuple(rhs_element))

	# If a rule is a unit production, duplicate rules to conform to CNF
	grammar_removal_list = []
	grammar_deletion_list = []
	for lhs in lhs_rhs_dict:
		for rhs in lhs_rhs_dict[lhs]:
			if len(rhs) == 1 and rhs[0] != rhs[0].lower(): 
				# Unit production

				# First, for X -> Y, copy all rules X -> AB to Y -> AB
				for possible_repeated_lhs in lhs_rhs_dict:
					if possible_repeated_lhs == rhs[0]:
						for repeated_rule in lhs_rhs_dict[possible_repeated_lhs]:
							lhs_rhs_dict[lhs].append(repeated_rule)
							grammar_dict[repeated_rule].append(lhs)

				# Prepare to remove the unit production rules after the loops
				grammar_removal_list.append((rhs, lhs))
				if len(grammar_dict[rhs]) == 1: # Will be 0 after removal
					grammar_deletion_list.append(rhs)

	# Remove unneeded items left over from getting rid of unit productions
	for item in grammar_removal_list:
		grammar_dict[item[0]].remove(item[1])
	for item in grammar_deletion_list:
		grammar_dict.pop(item)

	# Return final dictionary of rules
	return grammar_dict

def fillTable(table, tokens, grammar):
	"""CKY algorithm"""
	N = len(tokens)
	for i in range(N):
		table[i][i+1] = []
		if (tokens[i], ) in grammar:
			productions = grammar[(tokens[i], )]
			for production in productions:
				table[i][i+1].append(Node(production, tokens[i])) #List of all possible terminals matching with token
		else:
			 sys.stdout.write("ERROR: The word "+tokens[i]+" is not in the given grammar.\n")
			 sys.exit(0)
	for i in range(1, N+1):
		for j in range(i-2,-1,-1): #This is to go diagonally
			print(j,i)
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

def printTree(node, recursionDepth):
	"""Prints the tree structure of a parsed sentence"""
	sys.stdout.write("("+ node.terminal +" ")
	if type(node.pointer) is not str:
		printTree(node.pointer[0],recursionDepth+len(node.terminal)+2)
		printTree(node.pointer[1],recursionDepth+len(node.terminal)+2)
	else:
		sys.stdout.write(node.pointer)
	sys.stdout.write(")")
	sys.stdout.write("\n"+''.join([' ' for s in range(recursionDepth)]))

def main():
	grammarRaw = sys.argv[1] # Filename
	sentence = sys.argv[2]
	grammar = get_grammar(grammarRaw)
	tokens = sentence.split()
	N = len(tokens) #N is number of words in sentence
	# fill with empty lists
	table = [[[] for i in range(N + 1)] for j in range(N+1)]
	table = fillTable(table, tokens, grammar)
	validSentence = False
	print("num final parses:", len(table[0][N]))
	for finalParse in table[0][N]:
		if finalParse.terminal == "S":
			printTree(finalParse, 0)
			validSentence = True
		else:
			print("Another parse is", finalParse.terminal)
	if not validSentence:
		sys.stdout.write("ERROR: There is no grammatical parsing for the given sentence.\n")

if __name__ == "__main__":
	main()

