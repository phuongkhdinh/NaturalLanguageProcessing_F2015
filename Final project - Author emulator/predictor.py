'''
    predictor.py
    Written for CS322 - Natural Language Processing
    By Julia Kroll and Phuong Dinh
    This file read (optional) Language Model input / or use our default Hemingway LM
    Take in a starting phrase
    Generate a Hemingway-styled sentence.
'''

from earley_parser import *
import random
from nltk import word_tokenize
import sys



def generate_sentence(phrase, grammar, parser_probs, headword_bigram):
    '''
    This function recursively generate sentence till it's grammatically correct
    '''
    min_length = random.randint(5,7) # Minimum number of words in sentence
    top_selected_words, is_complete = Earley_Parser().parse(grammar["ROOT"], phrase, parser_probs, headword_bigram) # returns sorted dictionary of possible words and their probabilities
    tokenized_phrase = word_tokenize(phrase)

    if (is_complete and len(tokenized_phrase) > min_length) or (len(top_selected_words) == 0) or (len(tokenized_phrase) > 12) or (tokenized_phrase[-1] == '.'):
        return phrase, is_complete
    else:
        selected_word = top_selected_words[random.randint(0, len(top_selected_words)-1)]
        while selected_word[0] == tokenized_phrase[-1]:
            selected_word = top_selected_words[random.randint(0, len(top_selected_words)-1)]
        sys.stdout.write(selected_word[0] +  " ")
        sys.stdout.flush()
        phrase = phrase + " " + selected_word[0]
        return generate_sentence(phrase, grammar, parser_probs, headword_bigram)

def readInput():
    '''
    Read user input (if any)
    '''
    if len(sys.argv) == 4:
        grammar_file = sys.argv[1]
        parser_probs_file = sys.argv[2]
        headword_bigram_file = sys.argv[3]

    elif len(sys.argv) == 1: # Use our default files
        grammar_file = "grammar_250sibs.dat"
        parser_probs_file = "parser_probs_250sibs.dat"
        headword_bigram_file = "headword_bigram_250sibs.dat"
    else:
        print("ERROR: The program accept either 0 or 3 argument. \npython3 predictor.py [grammar.txt PCFG.txt bigram.txt]")
        sys.exit()
    #try:

    with open(grammar_file, 'rb') as handle:
        grammar = pickle.loads(handle.read())
    with open(parser_probs_file, 'rb') as handle:
        parser_probs = pickle.loads(handle.read())
    with open(headword_bigram_file, 'rb') as handle:
        headword_bigram = pickle.loads(handle.read()) 
    #except:
    #    print("ERROR: Cannot open input files.")
    #    sys.exit()  

    return grammar, parser_probs, headword_bigram

def main():

    grammar, parser_probs, headword_bigram = readInput()

    starting_phrase = input("Please enter starting word(s): ")
    if starting_phrase == "":
        sys.stdout.write("User must enter some start word.\n")
        sys.stdout.flush()
        sys.exit()
    sys.stdout.write("Sentence building: " + starting_phrase + " ")
    sys.stdout.flush()
    phrase, is_complete = generate_sentence(starting_phrase, grammar, parser_probs, headword_bigram)
    num_attempts = 0
    while not is_complete and num_attempts < 6:
        num_attempts += 1
        sys.stdout.write("\nNot a legal sentence. Regenerate from beginning.\n")
        sys.stdout.write("Sentence building: " + starting_phrase + " ")
        sys.stdout.flush()
        phrase, is_complete = generate_sentence(starting_phrase, grammar, parser_probs, headword_bigram)

    if is_complete:
        sys.stdout.write("\nDone. Finished sentence: "+ phrase+"\n")
    else:
        sys.stdout.write("\nCannot generate sentence starting with '" + starting_phrase+"' using the LM.\n")
    sys.stdout.flush()

if __name__ == '__main__':
    main()
