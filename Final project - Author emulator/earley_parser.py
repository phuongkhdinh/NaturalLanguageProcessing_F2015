'''
    Earley_Parser.py
    Written for CS322 - Natural Language Processing Final project
    By Julia Kroll and Phuong Dinh
    An Early Parser with some twist to work for prediction purpose
    Output the top 5 word guess to complete sentence
    Some code are referenced from Charty project (http://www.cavar.me/damir/charty/python/)
'''
import sys
import pickle
from math import exp, log


class Rule():
    '''
        Rule object, e.g NP -> DT NN
    '''
    def __init__(self, name, *productions):
        self.name = name
        self.productions = list(productions)
    def __str__(self):
        return self.name
    def add(self, productions):
        self.productions.append(productions)


class Production():
    '''
        Production object (the RHS), e.g DT NN
    '''
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
    def __repr__(self):
        return " ".join(str(t) for t in self.terms)
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
    '''
        Represent each row of a chart
    '''
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
    '''
        Column of Earley parser chart
    '''
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

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

class Earley_Parser():
    '''
        The Earley Parser
        With a twist, output the predicted word at the last column, 
        on top of analyzing whether the sentence is grammatically correct
    '''
    def __init__(self):
        self.GAMMA = "GAMMA"

    def predict(self, col, rule):
        predictWords = set()
        for prod in rule.productions:
            col.add(State(rule.name, prod, 0, col))
            if prod.gettype() is str:
                predictWords.add(prod[0])
        return predictWords
    def scan(self, col, state, token):
        if token != col.token:
            return
        col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))

    def complete(self, col, state):
        if not state.completed():
            return
        for st in state.start_column:
            term = st.next_term()
            if not isinstance(term, Rule):
                continue
            if term.name == state.name:
                col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))

    def parse(self, rule, text, parserProbs, headwordBigram):
        table = [Column(i, tok) for i, tok in enumerate([None] + text.lower().split())]
        table[0].add(State(self.GAMMA, Production(rule), 0, table[0]))
        # Initiate the chart with Gamma -> Root
        parserProbs[('GAMMA', ('ROOT',))] = 0.0
        ruleTransProbMatrix = {}
        predictWordProbMatrix = {}

        for i, col in enumerate(table):

            for state in col:
                #Complete rule
                if state.completed():
                    self.complete(col, state)
                else:
                    term = state.next_term()
                    if isinstance(term, Rule):

                        # Take out broken sentence rules
                        if state.name == "ROOT" and len(state.production)==1 and \
                            (state.production[0].name == "FRAG" or state.production[0].name == "SBARQ"):
                            continue

                        # Run predict rules    
                        predictWords = self.predict(col, term)

                        ### Find the probability of the words appearing next
                        ### Using ruleTransProb, wordEmissionProb, and bigramTransProb
                        ### Since all value are log, the * become +
                        if i==len(text.split())-1:
                            stateij = (state.name, tuple([obj.name for obj in state.production]))
                            ruleTransProb = parserProbs[stateij]
                            ruleTransProbMatrix[stateij] = ruleTransProb
                            #predictWordProbMatrix[]
                            for word in predictWords:
                                wordEmissionProb =  parserProbs[(term.name, word)]
                                if (text.split()[i],word) in headwordBigram:
                                    bigramTransProb = headwordBigram[(text.split()[i],word)]
                                else:
                                    bigramTransProb = -17 #Discount if the word never appear
                                wordProb = ruleTransProb + wordEmissionProb + bigramTransProb

                                if word in predictWordProbMatrix:
                                    predictWordProbMatrix[word] = max(wordProb, predictWordProbMatrix[word])
                                else:
                                    predictWordProbMatrix[word] = wordProb

                    # Scan rule
                    elif i + 1 < len(table):
                        self.scan(table[i+1], state, term)
            
        ### Rank word by probs
        predictWordProbMatrix = sorted(predictWordProbMatrix.items(), key=lambda x: x[1], reverse=True)
        n = 4
        topPredictedWord = predictWordProbMatrix[:min(n, len(predictWordProbMatrix))]



        sentenceComplete = False
        for state in table[-1]: #The sentence is parsable (complete using our grammar)
            if state.name == self.GAMMA and state.completed():
                sentenceComplete = True
                return topPredictedWord, sentenceComplete
        else:
            return topPredictedWord, sentenceComplete


