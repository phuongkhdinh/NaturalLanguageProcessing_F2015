# stemmer.py
# By Julia Kroll and Phuong Dinh
# 26th Sep 2015
# This program implements the Potter Stemmer algorithm, which aims to remove suffixes from words
# Rules are referenced to "An algorithm for suffix stripping" by M.F.Porter (1980)

import re

def step1a(word):
	if re.search(r'sses$', word):
		word = re.sub(r'sses$', r'ss', word)
	elif re.search(r'ies$', word):
		word = re.sub(r'ies$', r'i', word)
	elif re.search(r'ss$', word):
		pass
	elif re.search(r's$', word):
		word = re.sub(r's$', r'', word)	
	return word

def step1b(word):
	if re.search(r'eed$', word):
		m = calculateM(re.sub(r'eed$', r'', word))
		if m > 0:
			word = re.sub(r'eed$', r'ee', word)
	elif re.search(r'([aeiou]|[b-df-hj-np-tv-xz]y).*ed$', word):
		word = re.sub(r'ed$', r'', word)
		word = step1bhelper(word)	
	elif re.search(r'([aeiou]|[b-df-hj-np-tv-xz]y).*ing$', word):
		word = re.sub(r'ing$', r'', word)
		word = step1bhelper(word)	
	return word

def step1bhelper(word):
	# If the 2nd or 3rd rule in step 1b is successful, proceed to this
	if re.search(r'at$', word):
		word = re.sub(r'at$', r'ate', word)
	elif re.search(r'bl$', word):
		word = re.sub(r'bl$', r'ble', word)
	elif re.search(r'iz$', word):
		word = re.sub(r'iz$', r'ize', word)
	elif re.search(r'([^lsz])\1$', word):
		# *d and not (*l, *s or *z)
		word = re.sub(r'([^lsz])\1$', r'\1', word)	
	elif re.search(r'([b-df-hj-np-tv-xz]|[aeiou]y|^y)[aeiouy][b-df-hj-np-tvz]$', word): 
		# *o rule: *cvc where the 2nd v is not w, x, y 
		m = calculateM(word)
		if m == 1:
			word = re.sub(r'$', r'e', word)	
	return word

def step1c(word):
	if re.search(r'([aeiou]|[b-df-hj-np-tv-xz]y).*y$', word):
		# (*v*) Y -> I
		word = re.sub(r'y$', r'i', word)
	return word

def step2(word):
	m = calculateM(re.sub(r'(ational|tional|enci|anci|izer|abli|alli|entli|eli|ousli\
		|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti)$', r'', word))
	if m > 0:
		if re.search(r'ational$', word):
			word = re.sub(r'ational$', r'ate', word)
		elif re.search(r'tional$', word):
			word = re.sub(r'tional$', r'tion', word)
		elif re.search(r'enci$', word):
			word = re.sub(r'enci$', r'ence', word)
		elif re.search(r'anci$', word):
			word = re.sub(r'anci$', r'ance', word)
		elif re.search(r'izer$', word):
			word = re.sub(r'izer$', r'ize', word)
		elif re.search(r'abli$', word):
			word = re.sub(r'abli$', r'able', word)
		elif re.search(r'alli$', word):
			word = re.sub(r'alli$', r'al', word)
		elif re.search(r'entli$', word):
			word = re.sub(r'entli$', r'ent', word)
		elif re.search(r'eli$', word):
			word = re.sub(r'eli$', r'e', word)
		elif re.search(r'ousli$', word):
			word = re.sub(r'ousli$', r'ous', word)
		elif re.search(r'ization$', word):
			word = re.sub(r'ization$', r'ize', word)
		elif re.search(r'ation$', word):
			word = re.sub(r'ation$', r'ate', word)
		elif re.search(r'ator$', word):
			word = re.sub(r'ator$', r'ate', word)
		elif re.search(r'alism$', word):
			word = re.sub(r'alism$', r'al', word)
		elif re.search(r'iveness$', word):
			word = re.sub(r'iveness$', r'ive', word)
		elif re.search(r'fulness$', word):
			word = re.sub(r'fulness$', r'ful', word)
		elif re.search(r'ousness$', word):
			word = re.sub(r'ousness$', r'ous', word)
		elif re.search(r'aliti$', word):
			word = re.sub(r'aliti$', r'al', word)
		elif re.search(r'iviti$', word):
			word = re.sub(r'iviti$', r'ive', word)
		elif re.search(r'biliti$', word):
			word = re.sub(r'biliti$', r'ble', word)
	return word

def step3(word):
	m = calculateM(re.sub(r'(icate|iciti|ical|ative|ful|ness|alize)$', r'',word))
	if m > 0:
		if re.search(r'(icate|iciti|ical)$', word):
			word = re.sub(r'(icate|iciti|ical)$', r'ic', word)
		elif re.search(r'(ative|ful|ness)$', word):
			word = re.sub(r'(ative|ful|ness)$', r'', word)
		elif re.search(r'alize$', word):
			word = re.sub(r'alize$', r'al', word)
	return word

def step4(word):
	m = calculateM(re.sub(r'(al|ance|ence|er|ic|able|ible|ant|ement|ment|\
		ent|ou|ism|ate|iti|ous|ive|ize)$', r'',word))
	if m > 1:
		if re.search(r'(al|ance|ence|er|ic|able|ible|ant|ement|ment|\
			ent|ou|ism|ate|iti|ous|ive|ize)$', word):
			word = re.sub(r'(al|ance|ence|er|ic|able|ible|ant|ement|ment|\
			ent|ou|ism|ate|iti|ous|ive|ize)$', r'', word)
		elif re.search(r'[st]ion$', word):
			word = re.sub(r'ion$', r'', word)
	return word

def step5a(word):
	m = calculateM(word)
	# (m > 1) E
	if m > 1 and re.search(r'e$', word):
			word = re.sub(r'e$', r'', word)

	# m=1 and not *o
	elif (not re.search(r'([b-df-hj-np-tv-xz]|[aeiou]y|^y)[aeiouy][b-df-hj-np-tvz].$', word)) \
	 and re.search(r'e$', word):
		if m == 1:
			word = re.sub(r'e$', r'', word)	
	return word

def step5b(word):
	if re.search(r'll$', word):
		m = calculateM(word)
		if m > 1:
			word = re.sub(r'l$', r'', word)
	return word

def calculateM(word):
# Determine number of VC repetitions in a given word
	word = resolveY(word)
	return len(re.findall(r'.*?([aeiou]+[b-df-hj-np-tv-xz]+).*?', word))

def resolveY(word):
# Changes each occurrence of 'y' to 'z' if it serves as a consonant and 'a' if it serves as a vowel

	# First resolve all y's as consonants or vowels
	while re.search(r'y', word):
		# y starts word --> y is consonant
		if re.search(r'^y', word):
			word = re.sub(r'^y', r'z', word)
		# y follows vowel --> y is consonant
		elif re.search(r'[aeiou]y', word):
			print(word)
			word = re.sub(r'([aeiou])y', r'\1z', word)
		# y follows consonant --> y is vowel
		elif re.search(r'[b-df-hj-np-tv-z]y', word):
			word = re.sub(r'([b-df-hj-np-tv-z])y', r'\1a', word)
		else:
			print('ERROR no y matches')
	return word
	
def main():
	print("This program strips the suffixes of words\nTo use the program, enter a word, without punctuation \nTo quit, enter quit()\n---------------")
	word = input("Please enter a word: ") 
	while word != "quit()":
		word = word.lower()
		word = step1a(word)	
		word = step1b(word)	
		word = step1c(word)
		word = step2(word)	
		word = step3(word)
		word = step4(word)	
		word = step5a(word)	
		word = step5b(word)	
		print("Stem: "+word)
		word = input("Please enter another word: ")

if __name__ == "__main__":
	main()
