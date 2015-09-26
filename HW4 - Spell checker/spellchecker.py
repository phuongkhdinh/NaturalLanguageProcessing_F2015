# spellchecker.py
# By Julia Kroll and Phuong Dinh
# 30th Sep 2015


import re
import sys



def main():
    #read file
    inputFile = open(sys.argv[1],"r")
    for line in inputFile:
        print(line)
        tokenizedLine = re.sub(r'([?!()";/|`])', r' \1 ', line);
        for word in tokenizedLine.split():
            print(word)
    #tokenizer

    # Close all files
    inputFile.close()
if __name__ == "__main__":
    main()
