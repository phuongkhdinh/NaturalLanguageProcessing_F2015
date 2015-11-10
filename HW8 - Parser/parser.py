import sys

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
		if tuple(right_hand_side) in grammar_dict:
			grammar_dict[tuple(right_hand_side)] = [left_hand_side]
		else:
			grammar_dict[tuple(right_hand_side)].append(left_hand_side)
		if left_hand_side in lhs_rhs_dict:
			lhs_rhs_dict[left_hand_side] = [tuple(right_hand_side)]
		else:
			lhs_rhs_dict[left_hand_side].append(tuple(right_hand_side))

	# If a rule is a unit production, duplicate rules to conform to CNF
	for lhs in lhs_rhs_dict:
		for rhs in lhs_rhs_dict[lhs]:
			if len(rhs) == 1: # Unit production
				for possible_repeated_lhs in lhs_rhs_dict:
					if possible_repeated_lhs == rhs:
						lhs_rhs_dict[]
			

	return grammar_dict

def main():
	grammar_filename = sys.argv[1]
	grammar_dict = get_grammar(grammar_filename)
	print(grammar_dict)

if __name__ == "__main__":
	main()

