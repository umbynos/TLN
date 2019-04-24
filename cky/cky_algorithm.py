import numpy as np
import sys
table = np.zeros((len(words),len(words)))
#grammar verrà gestita globalmente

def cky_parse(words,grammar_dict):
	for j in range(1, len(words)+1):
		table[j-1,j] = find_lex_rule(words[j], grammar_dict)
		for i in range(j-2, -1, -1): #third argument "-1" used as decrement var
			for k in range(i+1, j-1):
				table[i,j] #add things and stuff
	return table

def find_lex_rule(word,grammar_dict):
	return grammar_dict[word]

def create_dict(grammar_file):
	file = open(grammar_file,"r")
	grammar_dict = {}
	for line in file:
		grammar_dict[(line.split("->")[1]).strip('\n')] = (line.split("->")[0])
	return grammar_dict
  		

def __init__(self):
	grammar = sys.argv[1]
	sentence = sys.argv[2]
	grammar_dict = create_dict(grammar)
	table = cky_parse(sentence, grammar_dict)
