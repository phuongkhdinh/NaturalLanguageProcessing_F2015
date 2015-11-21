import os
from nltk.parse import stanford
from nltk.tree import ParentedTree, Tree
#from nltk.tree import Tree
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

    def tokenize_sentences(self):
        """Tokenize corpus into sentences"""
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 
        f = open("hemingway/full_text/winner_take_nothing.txt")
        data = f.read()
        sentences = tokenizer.tokenize(data)
        return sentences

    def tokenize_sentence(self, sentence):
        tokenized_sentence = word_tokenize(sentence)
        return tokenized_sentence

    def parse_sentences(self, filename, num_sentences):
        """Parse each sentence into a tree"""
        f = open(filename, 'r')
        if num_sentences == 'all':
            num_sentences = -1
        count = 0
        for sentence in f.readlines()[240:num_sentences]:
            if count%10==0:
                print(count)
            trees = self.parser.raw_parse(sentence.lower())
            for tree in trees:
                #print(tree)
                self.nonterminal_counts['ROOT'] = 1
                tokenized_sentence = self.tokenize_sentence(sentence)
                if len(tokenized_sentence) > 8:
                    self.extract_rules(tree)
                ptree = ParentedTree.convert(tree)
                self.get_bigram(ptree, tokenized_sentence)
            count+=1

    def extract_rules(self, tree):
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

            rule.add(Production(tuple(production_objects)))
            self.probabilistic_parser_counts[(rule_name, tuple([obj.name for obj in production_objects]))] += 1


    def get_bigram(self, tree, sentence):
        # For each child
        for i in range(len(tree)):
            #print("tree len", len(tree))
            if len(tree[i]) > 0 and type(tree[i]) != str:
                self.get_bigram(tree[i], sentence)
            # For each terminal
            else:
                #print("ptree: ", tree)
                self.get_headword(tree, tree[i], sentence)


    # Node must be parented tree
    def get_headword(self, node, label, sentence):
        if type(node) == str:
            #print("wow", node)
            try: #Sometimes, there are discrepancy btw ntlk tokenizer and stanford tokenizer
                if sentence.index(label)-1 > -1:     
                #Do bigram
                    previous_word = sentence[sentence.index(label)-1]# Choose previous word
                    #print("Done", previous_word, label)            
                    self.headword_bigram_counts[(previous_word, label)] += 1  
                updated_node = True
            except:
                pass
            finally:
                return
        tag = node.label()
        # print(node, tag)
        while node.parent().label() != 'ROOT' and not node.left_sibling():
        #     #print(node)
            node = node.parent()
        #print(node.label())
        #node = node.parent()
        #print("a",node.label())
        updated_node = False
        if node.parent().label() != 'ROOT': 
            #print(node.label(), "label",label)

            if node.parent().label() == "NP":
                for sibling in node.left_sibling():         
                    #print("NP: ",node.label())
                    if type(sibling) is str:
                        node = sibling
                        updated_node = True
                        break
                    elif sibling.label() in ["NN", "NNS", "NNP", "NNPS", "PRP"]:
                        node = sibling
                        updated_node = True
                        break
            elif node.parent().label() == "VP":
                #print(node.parent())
                for sibling in node.left_sibling(): 
                    #print("sib",node.label(),sibling)
                    if type(sibling) is str:
                        node = sibling
                        updated_node = True
                        break
                    elif sibling.label() in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
                        node = sibling
                        updated_node = True
                        break
        #         #Choose Verb
            elif node.parent().label() ==  "VBZ" or node.parent().label() == "VBD":
                #Choose W__ or N__
                for sibling in node.left_sibling():  
                    if type(sibling) is str:
                        node = sibling
                        updated_node = True
                        break
                    elif sibling.label()[0] in ["W", "N"]:
                        node = sibling
                        updated_node = True
                        break
            elif node.parent().label() ==  "IN" or  node.parent().label()[0] == "W" or node.parent().label() == "S":
                if sentence.index(label)-1 > -1:     
                #Do bigram
                    previous_word = sentence[sentence.index(label)-1]# Choose previous word
                    #print("Done", previous_word, label)            
                    self.headword_bigram_counts[(previous_word, label)] += 1
                return

            if not updated_node:
                #print("false. Choose next", node)
                # Choose the rightmost tree

                node = node.left_sibling()
            self.get_headword(node, label, sentence)
    # def get_headword(self, node, label, sentence):
    #     if type(node) == str:
    #         #print("wow", node)
    #         previous_word = node
    #         self.headword_bigram_counts[(previous_word, label)] += 1
    #         print("wow", previous_word, label)     
    #         updated_node = True
    #         return
    #     tag = node.label()
    #     # print(node, tag)
    #     while node.parent().label() != 'ROOT' and not node.left_sibling():
    #     #     #print(node)
    #         node = node.parent()
    #     #print(node.label())
    #     #node = node.parent()
    #     #print("a",node.label())
    #     updated_node = False
    #     if node.parent().label() != 'ROOT': 
    #         #print(node.label(), "label",label)

    #         if node.parent().label() == "NP":
    #             for sibling in node.left_sibling():         
    #                 #print("NP: ",node.label())
    #                 if type(sibling) is str:
    #                     node = sibling
    #                     updated_node = True
    #                     break
    #                 elif sibling.label() in ["NN", "NNS", "NNP", "NNPS", "PRP"]:
    #                     node = sibling
    #                     updated_node = True
    #                     break
    #         elif node.parent().label() == "VP":
    #             #print(node.parent())
    #             for sibling in node.left_sibling(): 
    #                 #print("sib",node.label(),sibling)
    #                 if type(sibling) is str:
    #                     node = sibling
    #                     updated_node = True
    #                     break
    #                 elif sibling.label() in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
    #                     node = sibling
    #                     updated_node = True
    #                     break
    #     #         #Choose Verb
    #         elif node.parent().label() ==  "VBZ" or node.parent().label() == "VBD":
    #             #Choose W__ or N__
    #             for sibling in node.left_sibling():  
    #                 if type(sibling) is str:
    #                     node = sibling
    #                     updated_node = True
    #                     break
    #                 elif sibling.label()[0] in ["W", "N"]:
    #                     node = sibling
    #                     updated_node = True
    #                     break
    #         elif node.parent().label() ==  "IN" or  node.parent().label()[0] == "W" or node.parent().label() == "S":
    #             if sentence.index(label)-1 > -1:     
    #             #Do bigram
    #                 previous_word = sentence[sentence.index(label)-1]# Choose previous word
    #                 print("Done", previous_word, label)            
    #                 self.headword_bigram_counts[(previous_word, label)] += 1
    #             return

    #         if not updated_node:
    #             print("false. Choose next", node)
    #             # Choose the rightmost tree

    #             node = node.left_sibling()
    #         self.get_headword(node, label, sentence)


    def print_sentences(self, sentences):
        for sentence in sentences:
            print(sentence)

    def train_corpus(self):
        for item in self.probabilistic_parser_counts: #probabilitistic_parser[(LHS, RHS as tuple)] = 0.55
            #print(item[0])
            if item[0] in self.nonterminal_counts and item in self.probabilistic_parser_counts:
                self.probabilistic_parser_probs[item] = log(self.probabilistic_parser_counts[item]) - log(self.nonterminal_counts[item[0]])
        for bigram in self.headword_bigram_counts: #headword_bigram[(word1, word2)] = 0.55
            if bigram[0] in self.terminal_counts and bigram in self.headword_bigram_counts:
                self.headword_bigram_probs[bigram] = log(self.headword_bigram_counts[bigram]) - log(self.terminal_counts[bigram[0]])

def main():
    #sentences = tokenize_sentences()
    #print_sentences(sentences)
    lm = LanguageModel()
    lm.parse_sentences('./hemingway/sentences/sea.txt', 500)
    lm.train_corpus()
    # print("count:", lm.probabilistic_parser_probs[("NN", "skiff")])
    # print("CC", lm.nonterminal_counts["CC"])
    # print("f", lm.terminal_counts["fish"])
    #parse_sentences('test.txt')
    #print(rules["NP"].productions)
    # for prod in rules["NP"].productions:
    #     for rule in prod:
    #         print(rule)
    #     print()
    #print(rules)
    #get_trees()


    #pickle
    #pickle the headword bigramsssdfsdf
    with open("headword_bigram.dat", "wb") as outFile:
        pickle.dump(lm.headword_bigram_probs, outFile)
    #pickle the probabilistic parser probs (in log)
    with open("parser_probs.dat", "wb") as outFile:
        pickle.dump(lm.probabilistic_parser_probs, outFile)

    #pickle the grammar
    with open("grammar.dat", "wb") as outFile:
        pickle.dump(lm.grammar, outFile)
    # for tree in build_trees(parse(lm.grammar["ROOT"], "he was an old man")):
    #     tree.print_()
    


if __name__ == '__main__':
    main()