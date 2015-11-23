from earley_parser import *
import random
from nltk import word_tokenize
import sys

with open("grammar.dat", 'rb') as handle:
    grammar = pickle.loads(handle.read())
with open("parser_probs.dat", 'rb') as handle:
    parser_probs = pickle.loads(handle.read())
with open("headword_bigram.dat", 'rb') as handle:
    headword_bigram = pickle.loads(handle.read()) 
#print(grammar)   
# for tree in build_trees(parse(grammar["ROOT"], "the man was in a fish", parser_probs, headword_bigram)):
#     tree.print_()

def generate_sentence(phrase):
	#print("Phrase so far:", phrase)
	min_length = random.randint(4,6) # Minimum number of words in sentence
	top_selected_words, is_complete = parse(grammar["ROOT"], phrase, parser_probs, headword_bigram) # returns sorted dictionary of possible words and their probabilities
	tokenized_phrase = word_tokenize(phrase)
	#print(is_complete, len(tokenized_phrase), is_complete and len(tokenized_phrase) > min_length)
	if (is_complete and len(tokenized_phrase) > min_length) or (len(top_selected_words) == 0) or (len(tokenized_phrase) > 12):
		#print(phrase, is_complete)
		return phrase, is_complete
	else:
		selected_word = top_selected_words[random.randint(0, len(top_selected_words)-1)]
		while selected_word[0] == tokenized_phrase[-1]:
			selected_word = top_selected_words[random.randint(0, len(top_selected_words)-1)]
		sys.stdout.write(selected_word[0] +  " ")
		sys.stdout.flush()
		#print(selected_word[0], end=" ")
		phrase = phrase + " " + selected_word[0]
		return generate_sentence(phrase)

def main():
#try:
	starting_phrase = " ".join(sys.argv[1:])
	if starting_phrase == "":
		print("User must enter some start word.")
		sys.exit()
	sys.stdout.write("Sentence building: " + starting_phrase + " ")
	sys.stdout.flush()
	phrase, is_complete = generate_sentence(starting_phrase)
	num_attempts = 0
	while not is_complete and num_attempts < 6:
		num_attempts += 1
		phrase, is_complete = generate_sentence(starting_phrase)
		sys.stdout.write("\nNot a legal sentence. Regenerate from beginning.")
		sys.stdout.write("Sentence building: " + starting_phrase + " ")
		sys.stdout.flush()
	if phrase != "":
		print("\nDone. Finished sentence:", phrase)
	else:
		print("Cannot generate sentence starting with '" + starting_phrase+"'.")
#except:
	#print("Please enter a starting phrase")

if __name__ == '__main__':
	main()


# --> return list of possible next words, whether it can stop
# see if we should stop or not
# if we should stop:
#	return the sentence
# else:
# 	choose one item from the list (weighted by probabilitiy)
# 	return the list
