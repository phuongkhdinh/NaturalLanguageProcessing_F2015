README.txt

Author Emulator
CS322-Natural Language Processing
By Julia Kroll and Phuong Dinh

This program generates original sentences in the style of an author. We hoped to preserve a high level of originality by using a bigram model to generate new sentences, but incorporate a parser into the algorithm in order to produce sentences that were grammatical as well as novel.

- To train a new corpus, run:
python3 training.py [corpus.txt] 
(corpus.txt is optional)
If a corpus is not given, the program will use our default hemingway.txt. The Language Model will be output into 3 files: headword_bigram_250_USER.dat, parser_probs_250_USER.dat, grammar_250_USER.dat.

- To predict/generate a new sentence, run:
python3 predictor.py [grammar.dat parser_probs.dat headword_bigram.dat] 
(grammar.dat parser_probs.dat headword_bigram.dat are optional LM arguments)
If not given, the program will use our default 250 sentences demo LM for Hemingway.
