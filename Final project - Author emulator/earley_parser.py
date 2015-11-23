# An early Parser - reference

import sys
import pickle
from math import exp, log


class Rule():
    def __init__(self, name, *productions):
        self.name = name
        self.productions = list(productions)
    def add(self, productions):
        self.productions.append(productions)


class Production():
    def __init__(self, *terms):
        self.terms = terms
        if type(self.terms[0]) is tuple:
            self.terms = self.terms[0]
    def gettype(self):
        return type(self.terms[0])
    def __len__(self):
        return len(self.terms)
    def __getitem__(self, index):
        return self.terms[index]
    def __iter__(self):
        return iter(self.terms)
    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(self.terms)

class State():
    def __init__(self, name, production, dot_index, start_column):
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]
    def __eq__(self, other):
        return (self.name, self.production, self.dot_index, self.start_column) == \
            (other.name, other.production, other.dot_index, other.start_column)
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.name, self.production))
    def completed(self):
        return self.dot_index >= len(self.production)
    def next_term(self):
        if self.completed():
            return None
        return self.production[self.dot_index]

class Column():
    def __init__(self, index, token):
        self.index = index
        self.token = token
        self.states = []
        self._unique = set()
    def __len__(self):
        return len(self.states)
    def __iter__(self):
        return iter(self.states)
    def __getitem__(self, index):
        return self.states[index]
    def enumfrom(self, index):
        for i in range(index, len(self.states)):
            yield i, self.states[i]
    def add(self, state):
        if state not in self._unique:
            self._unique.add(state)
            state.end_column = self
            self.states.append(state)
            return True
        return False
    def print_(self, completedOnly = False):
        print("[%s] %r" % (self.index, self.token))
        print("=" * 35)
        for s in self.states:
            if completedOnly and not s.completed():
                continue
            print(repr(s))
        print()

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def print_(self, level = 0):
        print("  " * level + str(self.value))
        for child in self.children:
            child.print_(level + 1)

def predict(col, rule):
    predictWords = set()
    for prod in rule.productions:
        col.add(State(rule.name, prod, 0, col))
        if prod.gettype() is str:
            predictWords.add(prod[0])
    return predictWords
def scan(col, state, token):
    if token != col.token:
        return
    col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))

def complete(col, state):
    if not state.completed():
        return
    for st in state.start_column:
        term = st.next_term()
        if not isinstance(term, Rule):
            continue
        if term.name == state.name:
            col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))

GAMMA = u"GAMMA"

def parse(rule, text, parserProbs, headwordBigram):
    table = [Column(i, tok) for i, tok in enumerate([None] + text.lower().split())]
    table[0].add(State(GAMMA, Production(rule), 0, table[0]))
    parserProbs[('GAMMA', ('ROOT',))] = 0.0
    ruleTransProbMatrix = {}
    predictWordProbMatrix = {}

    for i, col in enumerate(table):
        #predictedWords = set()

        for state in col:
            if state.completed():
                complete(col, state)
            else:
                term = state.next_term()
                if isinstance(term, Rule):
                    if state.name == "ROOT" and len(state.production)==1 and state.production[0].name == "FRAG":
                        continue
                    predictWords = predict(col, term)
                    # AMONG THESE WORDS, which one has the highest bigram (top 2)
                    #print(i)
                    if i==len(text.split())-1:
                        stateij = (state.name, tuple([obj.name for obj in state.production]))
                        ruleTransProb = parserProbs[stateij]
                        ruleTransProbMatrix[stateij] = ruleTransProb
                        #predictWordProbMatrix[]
                        for word in predictWords:
                            wordEmissionProb =  parserProbs[(term.name, word)]
                            #print(text.split()[i],word)
                            if (text.split()[i],word) in headwordBigram:
                                bigramTransProb = headwordBigram[(text.split()[i],word)]
                            else:
                                bigramTransProb = -15
                            #print(ruleTransProb,wordEmissionProb, bigramTransProb)
                            wordProb = ruleTransProb + wordEmissionProb + bigramTransProb

                            if word in predictWordProbMatrix:
                                predictWordProbMatrix[word] = max(wordProb, predictWordProbMatrix[word])
                            else:
                                predictWordProbMatrix[word] = wordProb


                elif i + 1 < len(table):
                    scan(table[i+1], state, term)
        
    ### Rank word by probs
    predictWordProbMatrix = sorted(predictWordProbMatrix.items(), key=lambda x: x[1], reverse=True)
    n = 5
    topPredictedWord = predictWordProbMatrix[:min(n, len(predictWordProbMatrix))]
    #print(predictWordProbMatrix)



    sentenceComplete = False
    for st in table[-1]:
        if st.name == GAMMA and st.completed():
            #return st
            sentenceComplete = True
            return topPredictedWord, sentenceComplete
    else:
        #print("No tree was built. Not legal sentence")
        return topPredictedWord, sentenceComplete
        #sys.exit(1)



def main():
    with open("grammar.dat", 'rb') as handle:
        grammar = pickle.loads(handle.read())
    with open("parser_probs.dat", 'rb') as handle:
        parser_probs = pickle.loads(handle.read())
    with open("headword_bigram.dat", 'rb') as handle:
        headword_bigram = pickle.loads(handle.read())    



if __name__ == '__main__':
    main()
