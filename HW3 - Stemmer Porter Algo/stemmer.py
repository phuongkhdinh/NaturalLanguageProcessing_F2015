import re

def step1a(word, m):
	if re.search(r'sses$', word):
		word = re.sub(r'sses$', r'ss$', word)
	elif re.search(r'ies$', word):
		word = re.sub(r'ies$', r'i$', word)
	elif re.search(r'ss$', word):
		break
	elif re.search(r's$', word):
		word = re.sub(r's$', r'$', word)	
	return word

def step1b(word, m):
	if re.search(r'eed$', word) and m > 0:
		word = re.sub(r'eed$', r'ee$', word)
	elif re.search(r'([aeiou]|[^aeiou]y).*ed$', word):
		word = re.sub(r'ed$', r'$', word)
		word = step1bhelper(word,m)
	elif re.search(r'([aeiou]|[^aeiou]y).*ing$', word):
		word = re.sub(r'ing$', r'$', word)
		word = step1bhelper(word,m)
	return word

def step1bhelper(word,m):
	if re.search(r'at$', word):
		word = re.sub(r'at$', r'ate$', word)
	elif re.search(r'bl$', word):
		word = re.sub(r'bl$', r'ble$', word)
	elif re.search(r'iz$', word):
		word = re.sub(r'iz$', r'ize$', word)
	elif re.search(r'([^lsz])\1$', word):
		word = re.sub(r'([^lsz])\1$', r'\1', word)	
	elif re.search(r'([^aeiouy]|[aeiou]y)([aeiou]|[^aeiou]y)(^([aeiouwxy]|[^aeiou]y))', word) and m = 1:
		word = re.sub(r'([^lsz])\1$', r'\1', word)	
	### STILL NOT WORKING. NEED TO LOOK AT
	return word

def step1c(word, m):
	if re.search(r'([aeiou]|[^aeiou]y).*y$', word):
		word = re.sub(r'([aeiou]|[^aeiou]y).*y$', r'i$', word)
	return word

def step2(word, m):
	if re.search(r'ational$', word) and m > 0:
		word = re.sub(r'ational$', r'ate$', word)
	elif re.search(r'tional$', word) and m > 0:
		word = re.sub(r'tional$', r'tion$', word)
	elif re.search(r'enci$', word) and m > 0:
		word = re.sub(r'enci$', r'ence$', word)
	elif re.search(r'anci$', word) and m > 0:
		word = re.sub(r'anci$', r'ance$', word)
	elif re.search(r'izer$', word) and m > 0:
		word = re.sub(r'izer$', r'ize$', word)
	elif re.search(r'abli$', word) and m > 0:
		word = re.sub(r'abli$', r'able$', word)
	elif re.search(r'alli$', word) and m > 0:
		word = re.sub(r'alli$', r'al$', word)
	elif re.search(r'entli$', word) and m > 0:
		word = re.sub(r'entli$', r'ent$', word)
	elif re.search(r'eli$', word) and m > 0:
		word = re.sub(r'eli$', r'e$', word)
	elif re.search(r'ousli$', word) and m > 0:
		word = re.sub(r'ousli$', r'ous$', word)
	elif re.search(r'ization$', word) and m > 0:
		word = re.sub(r'ization$', r'ize$', word)
	elif re.search(r'ation$', word) and m > 0:
		word = re.sub(r'ation$', r'ate$', word)
	elif re.search(r'ator$', word) and m > 0:
		word = re.sub(r'ator$', r'ate$', word)
	elif re.search(r'alism$', word) and m > 0:
		word = re.sub(r'alism$', r'al$', word)
	elif re.search(r'iveness$', word) and m > 0:
		word = re.sub(r'iveness$', r'ive$', word)
	elif re.search(r'fulness$', word) and m > 0:
		word = re.sub(r'fulness$', r'ful$', word)
	elif re.search(r'ousness$', word) and m > 0:
		word = re.sub(r'ousness$', r'ous$', word)
	elif re.search(r'aliti$', word) and m > 0:
		word = re.sub(r'aliti$', r'al$', word)
	elif re.search(r'iviti$', word) and m > 0:
		word = re.sub(r'iviti$', r'ive$', word)
	elif re.search(r'biliti$', word) and m > 0:
		word = re.sub(r'biliti$', r'ble$', word)
	return word

def main():
	# word is input
	word = word.lower()
	word = step1a(word, m)
	word = step1b(word,m)
	word = step1c(word,m)
	word = step2(word,m)


if __name__ == "__main__":
	main()