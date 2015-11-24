"""
clean_corpus.py
Cleans a text file, removing various punctuation and chapter headings,
and tokenizes text into lines of sentences.
Output file is named '[input]_CLEAN_SENTENCES.txt'
"""

import sys
import re
import nltk.data

def clean_corpus(self):

	# Files
	corpus = open(sys.argv[1], 'r')
	clean_block_text = sys.argv[1][:-4] + "_CLEAN_BLOCK_TEXT.txt"
	clean_sentences = sys.argv[1][:-4] + "_CLEAN_SENTENCES.txt"
	f_block = open(clean_block_text, 'w')
	f_sentences = open(clean_sentences, 'w')

	# Clean each line in the corpus, construct a single-line clean file
	for line in corpus.readlines():
		if not re.match(r'Chapter ([0-9]+|[IVXL]+)', line, flags=re.IGNORECASE):
			line = line.strip("\n").lower() + " "
			f_block.write(re.sub(r'["\';:,_]', "", line))

	f_block.close()
	f_block = open(clean_block_text, 'r')

	# Tokenize the one giant line into one line per sentence
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 
	data = f_block.read()
	sentences = tokenizer.tokenize(data)
	for sentence in sentences:
		f_sentences.write(sentence)

	f_block.close()
	f_sentences.close()

	return clean_sentences
