import os
from nltk.parse import stanford
os.environ['STANFORD_PARSER'] = './stanford-parser-full-2015-04-20/'
os.environ['STANFORD_MODELS'] = './stanford-parser-full-2015-04-20/'

corpus = open()

parser = stanford.StanfordParser()
#sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
##sentences = parser.raw_parse_sents(["Hello, My name is Melroy.", "What is your name?"])
#print(sentences)
##print([parse for parse in parser.raw_parse_sents(["Hello, My name is Melroy.", "What is your name?"])])
#print([list(parse) for parse in parser.raw_parse_sents(("The quick brown fox jumps over the lazy dog.", "I am tired."))])
#print(sum([list(dep_graphs) for dep_graphs in parser.raw_parse_sents(("I can spam", "Time flies like an arrow"))], []))
#print([list(dep_graphs) for dep_graphs in parser.raw_parse_sents(("I can spam", "Fruit flies like a banana"))], [])

for dep_graphs in parser.raw_parse_sents(("I can spam", "Fruit flies like bananas")):
	print(list(dep_graphs))
	print("\n")

# GUI
# for line in sentences:
#     for sentence in line:
#         sentence.draw()