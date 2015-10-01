# spellchecker.py
# By Julia Kroll and Phuong Dinh
# 30th Sep 2015
# This program accepts a file as input, suggesting any correction to misspelled words
# Increased Efficiency in Word Choice: 
#           - Only calculate edit-distance for alternate words of length +- 1 to the original words
#           - Only calculate edit-distance for alternate words which have at least one matching letter within the 
#            first 3 letters of the original words (This does not affect the accuracy of suggestion but widely increase speed)
# Alterations to Levenshtein Distance: 
#           - Reduce substitution cost for commonly substituted letter from 2 to lower cost such as ae/ea (0.5), ai/ia/oe... (1)
#       This is because certain letters are statistically more commonly misspelled than others. (statistics from https://web.stanford.edu/class/cs124/lec/med.pdf )
#           - Threshold of maximum edit distance is 7 (e.g 3 letter swap and 1 ins/del)
# Others: When considering the correctness of the words, we also try to strip plural(sses, s) and "ed", "ing" suffixes
# Tokenizer and min Edit distance are adapted from Textbook (with a few changes)


import re
import sys

def getAbbrList():
    return ['co.', 'dr.', 'jan.', 'feb.', 'mar.', 'apr.', 'jun.', 'jul.', 'aug.', 'sep.', 'sept.', 'oct.', \
    'nov.', 'dec.', 'mrs.', 'ms.', 'mr.' 'jr.', 'sr.', 'inc.']

def sanitizeWord(word, abbr):
    # This function sanitise space and dots in words
    word = word.lower().strip()
    # Strip away '.'
    if re.search(r'[A-Za-z0-9]\.', word) and word.lower() not in abbr and \
     not re.search(r'^([A-Za-z]\.([A-Za-z]\.)+|[A-Z][bcdfghj-nptvxz]+\.)$', word):
        word = re.sub(r'\.$', r'', word)
    return word

def isValidWord(word, dictionary, abbr):
    # This function examine if a word is valid, take into consideration abbr and suffixes (sses, s, ed)
    return word in dictionary[len(word)] or word in abbr \
             or re.sub(r'sses$',r'ss', word, flags=re.I) in dictionary[len(word)-2]\
             or re.sub(r's$',r'', word, flags=re.I) in dictionary[len(word)-1] \
             or re.sub(r'([aeiouy].*)ed$',r'\1', word, flags=re.I) in dictionary[len(word)-2]\
             or re.sub(r'([aeiouy].*)ing$',r'\1', word, flags=re.I) in dictionary[len(word)-3]

def matchInFirstThreeLetters(target, source):
    # This function return bool whether the target and source word share at least 1 common character within the first 3 chars
	if target[0] == (source[0] or source[1] or source[2]):
		return True
	elif target[1] == (source[0] or source[1] or source[2]):
		return True
	elif target[2] == (source[0] or source[1] or source[2]):
		return True
	return False

def minEditDistance(target, source):
    # Implement the min edit distance algorithm (with a few twist) 
    # THIS IS THE MAIN TASK 
    n = len(target)
    m = len(source)

    distance = [[0 for x in range(m+1)] for x in range(n+1)]
    distance[0][0] = 0
    for i in range(1, n+1):
        distance[i][0] = distance[i-1][0] + insCost(target[i-1])
    for j in range(1, m+1):
        distance[0][j] = distance[0][j-1] + delCost(source[j-1])
    for i in range(1, n+1):
        for j in range(1, m+1):
            distance[i][j] = min(distance[i-1][j] + insCost(target[i-1]), \
                                 distance[i-1][j-1] + subCost(source[j-1], target[i-1]), \
                                 distance[i][j-1] + delCost(source[j-1]))
    return distance[n][m]

def insCost(targetLetter):
    return 1

def delCost(sourceLetter):
    return 1

def subCost(sourceLetter, targetLetter):
    # Sub cost varies depending on the frequency of certain mispelling
    # Source of statistics: https://web.stanford.edu/class/cs124/lec/med.pdf 

	if (sourceLetter == targetLetter):
		return 0
	# Reduce substitution cost for common letter substitutions in spelling mistakes
	elif sourceLetter + targetLetter == ("ae" or "ea"):
		return 0.5
	elif sourceLetter + targetLetter == ("ai" or "ia" or "mn" or "nm" or \
										 "ie" or "ei" or "oe" or "eo"):
		return 1
	return 2

def importDictionary():
    # import dictionary, return array of all words by length and alphabet
    wordList = open("/usr/share/dict/words","r")
    wordsArr = [None]*32
    wordsArr[0] = set([""])
    for word in wordList:
        word = word.strip()
        if not wordsArr[len(word)]:
            wordsArr[len(word)] = set([word])
        else:
            wordsArr[len(word)].add(word)

    #wordList.close()
    return wordsArr

def printIntroduction():
    #Introduction printing
    print('This program will suggest corrections for your spelling errors. We will suggest up to 5 corrections.')
    print('Choose a correction by typing a number from 1 to 5, or if you would like to keep the original word, press Enter.')
    print('Once you have gone through the whole file, we will save your corrected version as corrected_filename.txt.')
    input('Press Enter to start')
    print('------------------')
    print()

def printSuggestions(word, line, dictionary):
    # This function receive words which are considered mispelled, get 5 suggestions 
    # Receive user input and return the corrected line

    suggestionsArr = getFiveSuggestions(word, dictionary)
    if suggestionsArr: # if at least 1 suggestion exists
        print('Mis-spelled word: ', word, "\n")
        print('Context: ', line)
        print('Suggestions')
        for i in range(len(suggestionsArr)):
            print(str(i+1) + ': '+suggestionsArr[i][1])
        userSelection = input("Select your correction: ")
        while userSelection not in ["1","2","3","4","5", ""]:
            userSelection = input("Please enter 1 to 5 to choose your selection, or Enter to keep the original word.\nSelect your correction: ")
        if userSelection in ["1","2","3","4","5"]:
            #Do changes to the file.
            line = re.sub(word, suggestionsArr[int(userSelection)-1][1], line, flags=re.I)
        print("-----------------------------------\n")
    else:
        printNoSuggestion(word, line)
    return line

def printNoSuggestion(word, line):
    # This function will tell the user that we did not find any reasonable correction suggestions
    print('Mis-spelled word: ', word, "\n")
    print('Context: ', line)
    print("Sorry, we found no reasonable suggestions for this word")
    print("-----------------------------------\n")

def getFiveSuggestions(misspelledWord, dictionary):
    # This function find the 5 closest words to the mispelled words, measuring by edit distance
    lowestEditDistance = [(9999, None)] * 5
    for i in range(-1,2):
        try:
            for altWord in dictionary[len(misspelledWord) + i]:
				# Only check edit distance if target & source share >=1 of first three letters
                if (len(altWord) < 3 or len(misspelledWord) < 3) or matchInFirstThreeLetters(altWord, misspelledWord):
                    lowestEditDistance.sort()
                    editDistance = minEditDistance(altWord, misspelledWord)
                    if editDistance < lowestEditDistance[4][0] and editDistance < 8:
                        lowestEditDistance[4] = (editDistance, altWord)
                    else:
                        pass
        except IndexError:
            pass
    while (9999, None) in lowestEditDistance:
        lowestEditDistance.remove((9999, None))
    return lowestEditDistance

def getTokenizedLine(line):
    # This function do some of the tokenizer (some other are done in sanitizeWord function)
    tokenizedLine = re.sub(r'([?!()";|`#:%^*_+=~{}<>\[\]])', r'', line, flags=re.I) 
    tokenizedLine = re.sub(r'([^0-9]),', r'\1', tokenizedLine, flags=re.I)
    tokenizedLine = re.sub(r',([^0-9])', r'\1', tokenizedLine, flags=re.I)
    tokenizedLine = re.sub(r"^'", r"", tokenizedLine, flags=re.I)
    tokenizedLine = re.sub(r"([^A-Za-z0-9])'", r"\1", tokenizedLine, flags=re.I)
    tokenizedLine = re.sub(r"('|:|-)$", r'', tokenizedLine, flags=re.I)
    tokenizedLine = re.sub(r"('|:|-)([^A-Za-z0-9])", r' \2', tokenizedLine, flags=re.I)
    return tokenizedLine

def main():

    dictionary = importDictionary() # Get system dictionary

    printIntroduction()

    # Read file
    inputFile = open(sys.argv[1],"r")
    outputFile = open('corrected_'+sys.argv[1], 'w')
    
    abbr = getAbbrList()
    
    for line in inputFile:
        # Most of tokenizer is done here:
        tokenizedLine = getTokenizedLine(line)

        for word in tokenizedLine.split():
            word = sanitizeWord(word, abbr) # Remove space and dot

            if len(word) < 25: # if words of reasonable length
                if not re.match(r'^[0-9.,]*$', word): # Ignore number
                    if isValidWord(word, dictionary, abbr):
                        pass
                    else: # Words which are identified as "misspelled"
                        line = printSuggestions(word, line, dictionary)
            
            else: # Words which are too long -> no reasonable suggestions
                printNoSuggestion(word, line)

        # Write new edited line to file
        outputFile.write(line)

    # Close all files
    inputFile.close()
    outputFile.close()

    # Ending words
    print("Corrections complete. Please check for your corrected file in the folder. Thank you!\n")

if __name__ == "__main__":
    main()