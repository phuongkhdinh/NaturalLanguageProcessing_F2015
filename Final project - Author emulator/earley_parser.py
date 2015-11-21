# An early Parser - reference

import sys
import pickle
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
    def __repr__(self):
        return " ".join(str(t) for t in self.terms)
    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(self.terms)

class Rule():
    def __init__(self, name, *productions):
        self.name = name
        self.productions = list(productions)
    def __str__(self):
        return self.name
    def __repr__(self):
        return "%s -> %s" % (self.name, " | ".join(repr(p) for p in self.productions))
    def add(self, productions):
        self.productions.append(productions)

class State():
    def __init__(self, name, production, dot_index, start_column):
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]
    def __repr__(self):
        terms = [str(p) for p in self.production]
        terms.insert(self.dot_index, u"$")
        return "%-5s -> %-16s [%s-%s]" % (self.name, " ".join(terms), self.start_column, self.end_column)
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
    def __str__(self):
        return str(self.index)
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
            predictWords.add(prod.__getitem__(0))
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

GAMMA_RULE = u"GAMMA"

def parse(rule, text):
    table = [Column(i, tok) for i, tok in enumerate([None] + text.lower().split())]
    table[0].add(State(GAMMA_RULE, Production(rule), 0, table[0]))
    for i, col in enumerate(table):
        predictedWords = set()
        for state in col:
            if state.completed():
                complete(col, state)
            else:
                term = state.next_term()
                if isinstance(term, Rule):
                    predictWord = predict(col, term)
                    # AMONG THESE WORDS, which one has the highest bigram (top 2)
                    predictedWords |= predictWord

                elif i + 1 < len(table):
                    scan(table[i+1], state, term)
        
    print(predictedWords)

    # WILL WE END THE SENTENCE HERE?



    for st in table[-1]:
        if st.name == GAMMA_RULE and st.completed():
            return st
    else:
        print("No tree was built. Not legal sentence")
        sys.exit(1)

def build_trees(state):
    return build_trees_helper([], state, len(state.rules) - 1, state.end_column)

def build_trees_helper(children, state, rule_index, end_column):
    if rule_index < 0:
        return [Node(state, children)]
    elif rule_index == 0:
        start_column = state.start_column
    else:
        start_column = None
    
    rule = state.rules[rule_index]
    outputs = []
    for st in end_column:
        if st is state:
            break
        if st is state or not st.completed() or st.name != rule.name:
            continue
        if start_column is not None and st.start_column != start_column:
            continue
        for sub_tree in build_trees(st):
            for node in build_trees_helper([sub_tree] + children, state, rule_index - 1, st.start_column):
                outputs.append(node)
    return outputs

def main():
    with open("grammar.dat", 'rb') as handle:
        grammar = pickle.loads(handle.read())
    with open("parser_probs.dat", 'rb') as handle:
        parser_probs = pickle.loads(handle.read())
    with open("headword_bigram.dat", 'rb') as handle:
        headword_bigram = pickle.loads(handle.read())    

    for tree in build_trees(parse(grammar["ROOT"], "he was an old man")):
        tree.print_()

    print(parser_probs)
    print(headword_bigram)


if __name__ == '__main__':
    main()
# Prep = Rule("Prep")
# NP = Rule("NP")
# PP = Rule("PP")
# PP.add(Production(Prep, NP))
# AND = Rule("AND")
# AND.add(Production("and"))

# NP.add(Production(tuple([NP, PP])), Production(tuple([NP, AND, NP])))
# Noun = Rule("Noun")
# Noun.add(Production("i"),Production("cats"),Production("dogs"),Production("can"))
# Aux = Rule("Aux")
# Aux.add(Production("can"),Production("may"),Production("will"))
# Verb = Rule("Verb")
# Verb.add(Production("like"),Production("can"),Production("fool"),Production("catch"))
# VP = Rule("VP")

# VP.add(Production(VP, PP), Production(VP, NP, PP), Production(VP, NP),Production(Aux, VP, NP))




# Prep.add(Production("in"),Production("like"),Production("with"))
# Det = Rule("Det", Production("the"),Production("an"),Production("a"))


# NP.add(Production(Det, Noun), Production(Noun))
# VP.add(Production(Verb))

# S = Rule("S", Production(NP, VP))
# ROOT = Rule("ROOT", Production(S))


# print("ORBT")
# for prod in NP.productions:
#     for rule in prod:
#             print(rule)
# print("OND")
# for tree in build_trees(parse(ROOT, "i can like cats")):
#     tree.print_()
