from earley_parser import *
import random
from nltk import word_tokenize
import sys

with open("grammar500.dat", 'rb') as handle:
    grammar = pickle.loads(handle.read())
with open("parser_probs500.dat", 'rb') as handle:
    parser_probs = pickle.loads(handle.read())
with open("headword_bigram500.dat", 'rb') as handle:
    headword_bigram = pickle.loads(handle.read()) 

print(grammar)
def generate_sentence(phrase):
	min_length = random.randint(4,6) # Minimum number of words in sentence
	top_selected_words, is_complete = Earley_Parser().parse(grammar["ROOT"], phrase, parser_probs, headword_bigram) # returns sorted dictionary of possible words and their probabilities
	tokenized_phrase = word_tokenize(phrase)
	if (is_complete and len(tokenized_phrase) > min_length) or (len(top_selected_words) == 0) or (len(tokenized_phrase) > 12):
		return phrase, is_complete
	else:
		selected_word = top_selected_words[random.randint(0, len(top_selected_words)-1)]
		while selected_word[0] == tokenized_phrase[-1]:
			selected_word = top_selected_words[random.randint(0, len(top_selected_words)-1)]
		sys.stdout.write(selected_word[0] +  " ")
		sys.stdout.flush()
		phrase = phrase + " " + selected_word[0]
		return generate_sentence(phrase)

def main():
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


if __name__ == '__main__':
	main()


# --> return list of possible next words, whether it can stop
# see if we should stop or not
# if we should stop:
#	return the sentence
# else:
# 	choose one item from the list (weighted by probabilitiy)
# 	return the list
