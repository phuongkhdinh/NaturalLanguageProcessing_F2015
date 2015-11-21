from earley_parser import *

with open("grammar.dat", 'rb') as handle:
    grammar = pickle.loads(handle.read())
with open("parser_probs.dat", 'rb') as handle:
    parser_probs = pickle.loads(handle.read())
with open("headword_bigram.dat", 'rb') as handle:
    headword_bigram = pickle.loads(handle.read()) 
#print(grammar)   
for tree in build_trees(parse(grammar["ROOT"], "he was an old man")):
    tree.print_()