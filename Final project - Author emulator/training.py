'''
    training.py
    Written for CS322 - Natural Language Processing
    By Phuong Dinh and Julia Kroll
'''

import os
from nltk.parse import stanford
from nltk.tree import ParentedTree, Tree
from nltk import word_tokenize
os.environ['STANFORD_PARSER'] = './stanford-parser-full-2015-04-20/'
os.environ['STANFORD_MODELS'] = './stanford-parser-full-2015-04-20/'
import nltk.data
import time
import sys
from earley_parser import *
from collections import Counter
from math import log
import pickle
from clean_corpus import clean_corpus

class LanguageModel:

    def __init__(self):
        self.parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        self.grammar = {} 
        self.probabilistic_parser_counts = Counter()
        self.nonterminal_counts = Counter()
        self.terminal_counts = Counter()
        self.headword_bigram_counts = Counter() #headword_bigram_counts[(word1(preceding), word2)] = 17
        self.probabilistic_parser_probs = {}
        self.headword_bigram_probs = {}


    def tokenize_sentence(self, sentence):
        """Parses a string sentence into a list of tokens"""
        tokenized_sentence = word_tokenize(sentence)
        return tokenized_sentence

    def parse_sentences(self, filename, num_sentences):
        """Parses each one-line sentence into a syntax tree"""
        # Open the file and parse a given number of sentences
        f = open(filename, 'r')
        if num_sentences == 'all':
            num_sentences = -1
        count = 0
        for sentence in f.readlines()[:num_sentences]:
            if count%10==0:
                print("Number of sentences trained: ",count)
            # Get possible parse trees
            trees = self.parser.raw_parse(sentence.lower())
            for tree in trees:
                self.nonterminal_counts['ROOT'] += 1
                tokenized_sentence = self.tokenize_sentence(sentence)
                # Only extract rules from sentences with greater than 8 tokens,
                # to avoid adding rules that generate short, ungrammatical sentences
                if len(tokenized_sentence) > 8:
                    self.extract_rules(tree)
                # Convert the tree into a ParentedTree, 
                # which is an NLTK tree that keeps pointers to each node's parent
                ptree = ParentedTree.convert(tree)
                # Calculate the bigram counts for this sentence
                self.get_bigram(ptree, tokenized_sentence)
            count+=1

    def extract_rules(self, tree):
        """Given the parse tree of a sentence,
           extract all of the grammar rules it contains
           in order to build a PCFG."""
        rule_name = tree.label()
        rule = None
        production_objects = []
        if rule_name in self.grammar:
            # Add new production to existing rule
            rule = self.grammar[rule_name]
        else:
            # Create new rule object
            rule = Rule(rule_name)
            self.grammar[rule_name] = rule
        if type(tree[0]) == str:
            production_objects.append(tree[0])
            if (rule_name, tree[0]) not in self.probabilistic_parser_counts:
                rule.add(Production(tree[0]))
            self.probabilistic_parser_counts[(rule_name, tree[0])] += 1
            self.terminal_counts[tree[0]] += 1
            return
        else:
            for i in range(len(tree)): 
                # for every nonterminal child in tree
                self.extract_rules(tree[i])
                name = tree[i].label()
                self.nonterminal_counts[tree[i].label()] += 1
                if name in self.grammar:
                    production_objects.append(self.grammar[name])
                else:
                    child_rule = Rule(name)
                    self.grammar[name] = child_rule
                    production_objects.append(child_rule)

            if (rule_name, tuple([obj.name for obj in production_objects])) not in self.probabilistic_parser_counts:
                for obj in production_objects:
                    # Ignore rules with FRAG (sentence fragment) tags
                    if obj.name == "FRAG":
                        return
                rule.add(Production(tuple(production_objects)))
            self.probabilistic_parser_counts[(rule_name, tuple([obj.name for obj in production_objects]))] += 1

    def get_left_siblings(self, node):
        """Takes in a ParentedTree node and returns a list of all its left sibling nodes"""
        left_siblings = []
        while node.left_sibling() is not None:
            left_siblings.append(node.left_sibling())
            node = node.left_sibling()
        return left_siblings

    def get_bigram(self, tree, sentence):
        """Given a node and a string sentence,
           get the node's headword and add the
           headword and current word to bigram counts"""
        # For each child
        for i in range(len(tree)):
            # If the child is not a terminal:
            if type(tree[i]) != str:
                if len(tree[i]) > 0:
                    self.get_bigram(tree[i], sentence)
            # Else the child is a terminal:
            else:
                self.get_headword(tree, tree[i], sentence)
            
    def get_headword(self, node, label, sentence):
        """Get the headword given a node, original terminal's label,
           and the sentence the terminal appears in."""
        tag = node.label()
        # Traverse up the tree until a node with a left sibling is found
        while node.parent().label() != 'ROOT' and not node.left_sibling():
            node = node.parent()
        candidate_nodes = self.get_left_siblings(node)
        parent_node = node.parent()
        if candidate_nodes != []:
            self.traverse(candidate_nodes,parent_node, label, sentence)

    def get_children(self, node):
        """Returns a list of all children of a given node"""
        all_children = []
        for child in node:
            all_children.append(child)
        return all_children

    def traverse(self, candidate_nodes,parent_node, label, sentence):
        """Traverse the tree in search of the best possible headword 
           given the original candidate node and its label"""

        if len(candidate_nodes) == 1 and type(candidate_nodes[0]) is str:
            previous_word = candidate_nodes[0]
            self.headword_bigram_counts[(previous_word, label)] += 1
            updated_node = True
            return

        updated_node = False
        if parent_node.label() != 'ROOT': 
            if parent_node.label() == "NP":
                for candidate in candidate_nodes:         
                    if candidate.label() in ["NN", "NNS", "NNP", "NNPS", "PRP"]:
                        node = candidate
                        updated_node = True
                        break
            elif parent_node.label() == "VP":
                for candidate in candidate_nodes: 
                    if candidate.label() in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
                        node = candidate
                        updated_node = True
                        break
            elif parent_node.label() ==  "VBZ" or parent_node.label() == "VBD":
                for candidate in candidate_nodes:  
                    if candidate.label()[0] in ["W", "N"]:
                        node = candidate
                        updated_node = True
                        break
            elif parent_node.label() ==  "IN" or  parent_node.label()[0] == "W" or parent_node.label() == "S":
                if sentence.index(label)-1 > -1:     
                    previous_word = sentence[sentence.index(label)-1]   
                    self.headword_bigram_counts[(previous_word, label)] += 1
                return

            if not updated_node:
                # No better headword has been found, so just choose the rightmost left sibling
                node = candidate_nodes[-1]

            candidate_nodes = self.get_children(node)
            if candidate_nodes!=[]:
                self.traverse(candidate_nodes, node, label, sentence)

    def train_corpus(self):
        """Build PCFG and bigram headword models"""
        for item in self.probabilistic_parser_counts: #probabilitistic_parser[(LHS, RHS as tuple)] = 0.55
            if item[0] in self.nonterminal_counts and item in self.probabilistic_parser_counts:
                self.probabilistic_parser_probs[item] = log(self.probabilistic_parser_counts[item]) - log(self.nonterminal_counts[item[0]])
        for bigram in self.headword_bigram_counts: #headword_bigram[(word1, word2)] = 0.55
            if bigram[0] in self.terminal_counts and bigram in self.headword_bigram_counts:
                self.headword_bigram_probs[bigram] = log(self.headword_bigram_counts[bigram]) - log(self.terminal_counts[bigram[0]])

def main():

    # Take the corpus filename as user input
    try:
        if len(sys.argv) == 2:
            corpus = sys.argv[1]
        elif len(sys.argv) == 1:
            corpus = 'hemingway.txt' # Our default corpus if the user does not enter corpus
        else:
            print("ERROR: The program accept either 0 or 1 arguments. \npython3 training.py [corpus.txt]")
            sys.exit()
        lm = LanguageModel()
        cleaned_corpus = clean_corpus(corpus)
        lm.parse_sentences(cleaned_corpus, 250) # Trains 250 sentence as default
        lm.train_corpus(cleaned_corpus)
    except:
        print("ERROR: Cannot parse user input file.")
        sys.exit(1)


    # Pickle the three completed models for use in predictor.py
    with open("headword_bigram_250_USER.dat", "wb") as outFile:
        pickle.dump(lm.headword_bigram_probs, outFile)
    with open("parser_probs_250_USER.dat", "wb") as outFile:
        pickle.dump(lm.probabilistic_parser_probs, outFile)
    with open("grammar_250_USER.dat", "wb") as outFile:
        pickle.dump(lm.grammar, outFile)

    print("grammar_250_USER.dat, parser_probs_250_USER.dat and headword_bigram_250_USER.dat are created successfully.")

if __name__ == '__main__':
    main()