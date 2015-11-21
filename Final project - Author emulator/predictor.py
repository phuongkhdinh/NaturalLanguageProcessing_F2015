from earley_parser import *

with open("grammar.dat", 'rb') as handle:
    grammar = pickle.loads(handle.read())
with open("parser_probs.dat", 'rb') as handle:
    parser_probs = pickle.loads(handle.read())
with open("headword_bigram.dat", 'rb') as handle:
    headword_bigram = pickle.loads(handle.read()) 
#print(grammar)   
# for tree in build_trees(parse(grammar["ROOT"], "he was always a boy")):
#     tree.print_()

def generate_sentence(phrase):
	n = 5 # Number of words to consider
	min_length = 5 # Minimum number of words in sentence
	all_possible_words = parse(grammar["ROOT"], phrase]) # returns sorted dictionary of possible words and their probabilities
	top_n = all_possible_words[:n]
	selected_word = top_n[random.randint(0, n)]
	phrase += selected_word
	if len(tokenize_sentence(phrase)) > min_length and selected_word == ".":
		return sentence
	else:
		generate_sentence(phrase)


# --> return list of possible next words, whether it can stop
# see if we should stop or not
# if we should stop:
#	return the sentence
# else:
# 	choose one item from the list (weighted by probabilitiy)
# 	return the list
