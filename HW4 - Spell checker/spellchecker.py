# spellchecker.py
# By Julia Kroll and Phuong Dinh
# 30th Sep 2015


import re
import sys
from sets import Set

def minEditDistance(target, source):
    n = len(target)
    m = len(source)
    distance[0][0] = 0
    for i in range(1, n+1):
        distance[i][0] = distance[i-1][0] + insCost(target[i])
    for j in range(1, m+1):
        distance[0][j] = distance[0][j-1] + delCost(source[j])
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
    wordList = open(---filename).read()
    wordsArr = []
    for word in wordList:
        try:
            wordsArr[len(word)].add(word)
        except IndexError:
            wordsArr[len(word)] = Set([word])
    wordList.close()
    return wordsArr

def getFiveSuggestions(misspelledWord):
    lowestEditDistance = [(9999, None)] * 5
    try:
        for i in range(-1,2):
            for word in dictionary[len(word) + i]:
                lowestEditDistance.sort()
                editDistance = minEditDistance(word, misspelledWord)
                if editDistance < lowestEditDistance[4][1]:
                    lowestEditDistance[4] = (editDistance, word)



def main():

    dictionary = importDictionary()

    # Read file
    inputFile = open(sys.argv[1],"r")
    
    abbr = ['co.', 'dr.', 'jan.', 'feb.', 'mar.', 'apr.', 'jun.', 'jul.', 'aug.', 'sep.', 'sept.', 'oct.', \
    'nov.', 'dec.', 'mrs.', 'ms.', 'mr.' 'jr.', 'sr.', 'inc.']
    
    # Tokenization
    for line in inputFile:
        tokenizedLine = re.sub(r'([?!()";/|`])', r' \1 ', line, flags=re.I) 
        tokenizedLine = re.sub(r'([^0-9]),', r'\1 , ', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r',([^0-9])', r' , \1', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r"^'", r"' ", tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r"([^A-Za-z0-9])'", r"\1 ' ", tokenizedLine, flags=re.I)
        #tokenizedLine = re.sub(r"('|:|-|'s|'d|'m|'ll|'re|'ve|n't)$", r' \1', tokenizedLine, flags=re.I)
        #tokenizedLine = re.sub(r"('|:|-|'s|'d|'m|'ll|'re|'ve|n't)([^A-Za-z0-9])", r' \1 \2', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r"('|:|-)$", r' \1', tokenizedLine, flags=re.I)
        tokenizedLine = re.sub(r"('|:|-)([^A-Za-z0-9])", r' \1 \2', tokenizedLine, flags=re.I)
        for word in tokenizedLine.split():
            if re.search(r'[A-Za-z0-9]\.', word) and word not in abbr and \
             not re.search(r'^([A-Za-z]\.([A-Za-z]\.)+|[A-Z][bcdfghj-nptvxz]+\.)$', word):
                word = re.sub(r'\.$', r' .', word)
            #word = re.sub(r"'ve", r'have', word)
            #word = re.sub(r"'m", r'am', word)
            print(word, end=" ")
            if len(word) in dictionary:
                if not word in dictionary[len(word)]:
                    print('misspelled: ', word)
                    # call function to get 5 suggestions
                    suggestionsArr = getFiveSuggestions(misspelledWord)
            else:
                print(word + ": No suggestions")
        print()

    




    # Close all files
    inputFile.close()

if __name__ == "__main__":
    main()