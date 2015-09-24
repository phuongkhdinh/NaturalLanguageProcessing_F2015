# topicmodel.py
# By Phuong Dinh and Julia Kroll
# CS 322
# September 15, 2015
# Reads a file and prints out the five words 
# that best summarize the content of the file.
# stopwords.txt based on "Words Ignored By Search Engines", 
# www.link-assistant.com/seo-stop-words.html

import sys, re, queue, operator

'''Takes in text and a list of stop words (meaningles words) and returns a dictionary
of the words and their frequency'''
def getWordCounts(text, stopWords):
   wordCounts = {}
   for line in text:
         for word in line.split():
            regex = re.compile('[^A-Za-z]')
            # Remove non-alpha characters
            word = regex.sub('', word) 
            # Make word lowercase
            word = word.lower() 
            # Filter out meaningless words
            if word not in stopWords and word != "": 
               if word not in wordCounts:
                  wordCounts[word] = 1
               else:
                  wordCounts[word] = wordCounts[word] + 1
   return wordCounts

def main():
   text = open(sys.argv[1])
   stopWords = open('stopwords.txt').readline().split()
   wordCounts = getWordCounts(text, stopWords)
   text.close()
   # Sort items in decreasing order of occurence
   sortedWordCounts = sorted(wordCounts.items(), key=operator.itemgetter(1), reverse=True)
   # Print five most frequent words
   for item in range(5):
      print(sortedWordCounts[item][0], wordCounts[sortedWordCounts[item][0]])

if __name__ == '__main__':
   main()