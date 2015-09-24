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
	elif re.search(r'(^([aeiou]|[^aeiou]y))([aeiou]|[^aeiou]y)(^([aeiouwxy]|[^aeiou]y))', word) and m = 1:
		word = re.sub(r'([^lsz])\1$', r'\1', word)	
	return word

def main():
	# word is input
	word = word.lower()
	word = step1a(word)


if __name__ == "__main__":
	main()