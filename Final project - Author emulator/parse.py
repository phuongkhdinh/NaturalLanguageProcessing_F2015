import os
from nltk.parse import stanford
from nltk.tree import ParentedTree
from nltk.tree import Tree
os.environ['STANFORD_PARSER'] = './stanford-parser-full-2015-04-20/'
os.environ['STANFORD_MODELS'] = './stanford-parser-full-2015-04-20/'
import nltk.data
import time
import sys
from earley_parser import *

parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
rules = {} #(NP(prod1, prod2, prod3), VB(prod4, prod5))

def tokenize_sentences():
    """Tokenize corpus into sentences"""
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 
    f = open("hemingway/full_text/winner_take_nothing.txt")
    data = f.read()
    sentences = tokenizer.tokenize(data)
    return sentences

def parse_sentences(filename):
    """Parse each sentence into a tree"""
    f = open(filename, 'r')
    #t = open('trees.txt', 'w')
    #start = time.time()
    for sentence in f.readlines()[:1]:
        trees = parser.raw_parse(sentence)
        for tree in trees:
            print(tree)
            extract_rules(tree)

            # tree = ParentedTree.convert(tree)
            # for i in range(5):
            #     print(tree)
            #     tree = tree[0]
            #     if type(tree) == ParentedTree:
            #         print("right:", tree.right_sibling())

            #while tree[0] != None:
            # tree = tree[0][0][0]
            
            # print(tree.label())
            # print(tree.right_sibling())
            # pt = ParentedTree.convert(tree)
            # print(pt[0].parent().label())
            # print(pt.leaves())
            # for leaf in pt.leaves():
            #     print(pt.parent().label())
            # t.write(str(tree))
            # t.write("*")
        # for dep_graphs in parser.raw_parse(sentence):
        #   print(list(dep_graphs))
        #   print("\n")
    #end = time.time()
    #print("Time:", end-start)

def extract_string_rules(tree):
    """Preliminary version of rule extraction, using strings"""
    left = tree.label()
    right = []
    for i in range(len(tree)):
        if type(tree[i]) == Tree:
            right.append(tree[i].label())
            extract_rules(tree[i])
        elif type(tree[i]) == str:
            right.append(tree[i])
        else:
            print("Error: unexpected type")
            sys.exit(1)
    print(left, "->", right)
    right = tuple(right)
    new_rule = (left, right)
    rules.add(new_rule)

def extract_rules(tree):
    rule_name = tree.label()
    rule = None
    #rule = Rule(rule_name)
    #rules.add(
    production_objects = []
    if rule_name in rules:
        # Add new production to existing rule
        rule = rules[rule_name]
    else:
        # Create new rule object
        rule = Rule(rule_name)
        rules[rule_name] = rule
    for i in range(len(tree)): 
        # for every child in tree
        if type(tree[i]) == str:
            #print(rules[rule_name].productions)
            production_objects.append(tree[i])
            rule.add(Production(tree[i]))
            return
            #print(rules[rule_name].productions)
        # for every nonterminal in tree
        else: 
            extract_rules(tree[i])
            name = tree[i].label()
            if name in rules:
                production_objects.append(rules[name])
            else:
                child_rule = Rule(name)
                rules[name] = child_rule
                production_objects.append(child_rule)
    #print(rules[rule_name].productions)
        rule.add(Production(tuple(production_objects)))
    #print(rules[rule_name].productions)


    #         print("not adding anything")          
    #         prod_objects = []
    #         for item in production_items:
    #             if item in rules:
    #                 prod_objects.append(rules[item])
    #             else:
    #                 prod_objects.append(Rule(item))
    #         print("rule: ", rule)
    #         print("ProductioN:", tuple(prod_objects))
    #         rules[rule].add(Production(tuple(prod_objects)))
    #         extract_rules(tree[i])
    # print("ryle",rules)

# def make_parented_trees():
#     ## for each tree, pt = ParentedTree.convert(tree)


# GUI
# for line in sentences:
#     for sentence in line:
#         sentence.draw()

def print_sentences(sentences):
    for sentence in sentences:
        print(sentence)

def main():
    #sentences = tokenize_sentences()
    #print_sentences(sentences)
    #parse_sentences('./hemingway/sentences/sea.txt')
    parse_sentences('test.txt')
    print("done parsing")
    #print(rules["NP"].productions)
    print("PRINTING")
    for prod in rules["NP"].productions:
        for rule in prod:
            print(rule[0])
        print()
    #print(rules)
    #get_trees()
    # for tree in build_trees(parse(rules["ROOT"], "I can like cats and dogs")):
    #     tree.print_()


if __name__ == '__main__':
    main()