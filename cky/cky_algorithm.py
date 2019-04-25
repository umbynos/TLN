import numpy as np
import sys

def cky_parse(words,grammar_dict):
	#init of the table 
	table = np.empty((len(words),len(words)),dtype = 'object')
	for a in range (len(words)):
		for b in range (len(words)):
			table[a,b] = []
	#cky-algorithm beginning
	for j in range(1, len(words)+1):
		table[j-1,j] = find_lex_rule(words[j], grammar_dict)
		for i in range(j-2, -1, -1): #third argument "-1" used as decrement var
			for k in range(i+1, j-1):
				b = table[i,k]
				c = table[k,j]
				rhs = B + " " + C
				if (rhs in grammar_dict):
					table[i,j].append(grammar_dict[rhs])
	return table

def find_lex_rule(word,grammar_dict):
	print(word)
	print(grammar_dict[word])
	return grammar_dict[word]

def create_dict(grammar_file):
	file = open(grammar_file,"r")
	grammar_dict = {}
	for line in file:
		grammar_dict[(line.split("->")[1]).strip('\n')] = (line.split("->")[0])
	return grammar_dict

def main():
	grammar = sys.argv[1]
	sentence = sys.argv[2]
	grammar_dict = create_dict(grammar)
	table = cky_parse(sentence.split(), grammar_dict)
	print(table)

if __name__== "__main__":
	main()