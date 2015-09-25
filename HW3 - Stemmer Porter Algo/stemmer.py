import re

# Determine number of VC repetitions in a given word
def calculateM(word):
    # TODO
    return 0

def step1a(word, m):
	if re.search(r'sses$', word):
		word = re.sub(r'sses$', r'ss$', word)
	elif re.search(r'ies$', word):
		word = re.sub(r'ies$', r'i$', word)
	elif re.search(r'ss$', word):
		pass
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
    # This rule needs work...should match 'yay' but doesn't. -- doesn't match y as first letter
    # Is ^ being read as 'not' instead of 'start of string'? --
	elif re.search(r'([b-df-hj-np-tv-xz]|[aeiou]y|^y)[aeiouy][b-df-hj-np-tvz]$', word) and m == 1:
		word = re.sub(r'([^lsz])\1$', r'\1', word)	
	### I think work. For young, would y be considered vowel of consonent? if consonent then this should be correct
	return word

def step1c(word, m):
	if re.search(r'([aeiou]|[^aeiou]y).*y$', word):
		word = re.sub(r'([aeiou]|[^aeiou]y).*y$', r'i$', word)
	return word

def step2(word, m):
    if m > 0:
        if re.search(r'ational$', word):
            word = re.sub(r'ational$', r'ate$', word)
        elif re.search(r'tional$', word):
            word = re.sub(r'tional$', r'tion$', word)
        elif re.search(r'enci$', word):
            word = re.sub(r'enci$', r'ence$', word)
        elif re.search(r'anci$', word):
            word = re.sub(r'anci$', r'ance$', word)
        elif re.search(r'izer$', word):
            word = re.sub(r'izer$', r'ize$', word)
        elif re.search(r'abli$', word):
            word = re.sub(r'abli$', r'able$', word)
        elif re.search(r'alli$', word):
            word = re.sub(r'alli$', r'al$', word)
        elif re.search(r'entli$', word):
            word = re.sub(r'entli$', r'ent$', word)
        elif re.search(r'eli$', word):
            word = re.sub(r'eli$', r'e$', word)
        elif re.search(r'ousli$', word):
            word = re.sub(r'ousli$', r'ous$', word)
        elif re.search(r'ization$', word):
            word = re.sub(r'ization$', r'ize$', word)
        elif re.search(r'ation$', word):
            word = re.sub(r'ation$', r'ate$', word)
        elif re.search(r'ator$', word):
            word = re.sub(r'ator$', r'ate$', word)
        elif re.search(r'alism$', word):
            word = re.sub(r'alism$', r'al$', word)
        elif re.search(r'iveness$', word):
            word = re.sub(r'iveness$', r'ive$', word)
        elif re.search(r'fulness$', word):
            word = re.sub(r'fulness$', r'ful$', word)
        elif re.search(r'ousness$', word):
            word = re.sub(r'ousness$', r'ous$', word)
        elif re.search(r'aliti$', word):
            word = re.sub(r'aliti$', r'al$', word)
        elif re.search(r'iviti$', word):
            word = re.sub(r'iviti$', r'ive$', word)
        elif re.search(r'biliti$', word):
            word = re.sub(r'biliti$', r'ble$', word)
    return word

def step3(word, m):
    if m > 0:
        if re.search(r'(icate|iciti|ical)$', word):
            word = re.sub(r'(icate|iciti|ical)$', r'ic$', word)
        elif re.search(r'(ative|ful|ness)$', word):
            word = re.sub(r'(ative|ful|ness)$', r'$', word)
        elif re.search(r'alize$', word):
            word = re.sub(r'alize$', r'al$', word)
    return word

def step4(word, m):
    if m > 1:
        if re.search(r'(al|ance|ence|er|ic|able|ible|ant|ement)$', word):
            word = re.sub(r'(al|ance|ence|er|ic|able|ible|ant|ement)$', r'$', word)
        elif re.search(r'(ment|ent|ou|ism|ate|iti|ous|ive|ize)$', word):
            word = re.sub(r'(ment|ent|ou|ism|ate|iti|ous|ive|ize)$', r'$', word)
        elif re.search(r'[st]ion$', word):
            word = re.sub(r'[st]ion$', r'$', word)
    return word

def step5a(word, m):
    if re.search(r'e$', word) and m > 1:
        word = re.sub(r'e$', r'$', word)
    #### THIS RULE IS WRONG -- should be opposite of the rule in step1bhelper
    #elif re.search(r'[^(([b-df-hj-np-tv-xz]|[aeiou]y|^y)[aeiouy][b-df-hj-np-tvz])]$', word) and m == 1:
    #    word = re.sub(r'e$', r'$', word)
    return word

def step5b(word, m):
    if re.search(r'll$', word) and m > 1:
        word = re.sub(r'l$', r'$', word)
    
def main():
	userInput = input().split()
	word = userInput[0]
	m = int(userInput[1])
	word = word.lower()
	word = step1a(word, m)
	word = step1b(word, m)
	word = step1c(word, m)
	word = step2(word, m)
	word = step3(word, m)
	word = step4(word, m)
	word = step5a(word, m)
	word = step5b(word, m)
	print(word)

if __name__ == "__main__":
	main()
