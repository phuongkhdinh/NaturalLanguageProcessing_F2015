# spellchecker.py
# By Julia Kroll and Phuong Dinh
# 30th Sep 2015


import re
import sys
#from sets import Set

def minEditDistance(target, source):
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
    if (sourceLetter == targetLetter):
        return 0
    return 2

def importDictionary():
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

def getFiveSuggestions(misspelledWord, dictionary):
    lowestEditDistance = [(9999, None)] * 5
    for i in range(-1,2):
        try:
            for altWord in dictionary[len(misspelledWord) + i]:
                lowestEditDistance.sort()
                editDistance = minEditDistance(altWord, misspelledWord)
                if editDistance < lowestEditDistance[4][0]:
                    lowestEditDistance[4] = (editDistance, altWord)
        except IndexError:
            pass
    return lowestEditDistance

def main():

    dictionary = importDictionary()

    # Read file
    inputFile = open(sys.argv[1],"r")

    outputFile = open('corrected_'+sys.argv[1], 'w')
    
    abbr = ['co.', 'dr.', 'jan.', 'feb.', 'mar.', 'apr.', 'jun.', 'jul.', 'aug.', 'sep.', 'sept.', 'oct.', \
    'nov.', 'dec.', 'mrs.', 'ms.', 'mr.' 'jr.', 'sr.', 'inc.']
    
    # Tokenization
    for line in inputFile:
        # Original, adding spaces around punctuation
        # tokenizedLine = re.sub(r'([?!()";/|`])', r' \1 ', line, flags=re.I) 
        # tokenizedLine = re.sub(r'([^0-9]),', r'\1 , ', tokenizedLine, flags=re.I)
        # tokenizedLine = re.sub(r',([^0-9])', r' , \1', tokenizedLine, flags=re.I)
        # tokenizedLine = re.sub(r"^'", r"' ", tokenizedLine, flags=re.I)
        # tokenizedLine = re.sub(r"([^A-Za-z0-9])'", r"\1 ' ", tokenizedLine, flags=re.I)
        # #tokenizedLine = re.sub(r"('|:|-|'s|'d|'m|'ll|'re|'ve|n't)$", r' \1', tokenizedLine, flags=re.I)
        # #tokenizedLine = re.sub(r"('|:|-|'s|'d|'m|'ll|'re|'ve|n't)([^A-Za-z0-9])", r' \1 \2', tokenizedLine, flags=re.I)
        # tokenizedLine = re.sub(r"('|:|-)$", r' \1', tokenizedLine, flags=re.I)
        # tokenizedLine = re.sub(r"('|:|-)([^A-Za-z0-9])", r' \1 \2', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r'([?!()";/|`])', r'', line, flags=re.I) 
        tokenizedLine = re.sub(r'([^0-9]),', r'\1', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r',([^0-9])', r'\1', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r"^'", r"", tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r"([^A-Za-z0-9])'", r"\1", tokenizedLine, flags=re.I)
        #tokenizedLine = re.sub(r"('|:|-|'s|'d|'m|'ll|'re|'ve|n't)$", r' \1', tokenizedLine, flags=re.I)
        #tokenizedLine = re.sub(r"('|:|-|'s|'d|'m|'ll|'re|'ve|n't)([^A-Za-z0-9])", r' \1 \2', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r"('|:|-)$", r'', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r"('|:|-)([^A-Za-z0-9])", r' \2', tokenizedLine, flags=re.I)
        for word in tokenizedLine.split():
            word = word.lower().strip()
            if re.search(r'[A-Za-z0-9]\.', word) and word not in abbr and \
             not re.search(r'^([A-Za-z]\.([A-Za-z]\.)+|[A-Z][bcdfghj-nptvxz]+\.)$', word):
                word = re.sub(r'\.$', r'', word)
            #word = re.sub(r"'ve", r'have', word)
            #word = re.sub(r"'m", r'am', word)
            #print(word, end=" ")
            if len(word) < 32: #
                if not re.match(r'^[0-9.,]*$', word):
                    if not word in dictionary[len(word)]:
                        print('Mis-spelled word: ', word)
                        print('Context: ', line)
                        print('Suggestion')
                        # call function to get 5 suggestions
                        suggestionsArr = getFiveSuggestions(word, dictionary)
                        for i in range(5):
                            print(str(i+1) + ': '+suggestionsArr[i][1])
                        userSelection = input("Please choose a correction by entering number 1 to 5. Enter anything else to ignore. \nEnter: ")
                        if userSelection in ["1","2","3","4","5"]:
                            #Do changes to the file.
                            line = re.sub(word, suggestionsArr[int(userSelection)-1][1], line, flags=re.I)
                        print("-----------------------------------")
            else:
                print('Mis-spelled word: ', word)
                print('Context: ', line)
                print("No suggestions")
                print("-----------------------------------")

            
        # Write new edited line to file
        outputFile.write(line)

    # Close all files
    inputFile.close()
    outputFile.close()

if __name__ == "__main__":
    main()