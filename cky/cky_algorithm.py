import numpy as np
import sys
import re
from BinaryTree import BinaryTree

def cky_parse(words,grammar_dict):
	#init of the table 
	table = np.empty((len(words),len(words)),dtype = 'object')
	for a in range (len(words)):
		for b in range (len(words)):
			table[a,b] = []
	#cky-algorithm beginning
	for j in range(1, len(words)+1):
		table[j-1,j-1].append(find_lex_rule(words[j-1], grammar_dict) + "->" + words[j-1])
		for i in range(j-2, -1, -1): #third argument "-1" used as decrement var
			for k in range(i+1, j): #j: because range does not include last elem (j-1)
				for z in range (len(table[i,k-1])):
					b = table[i,k-1][z].split("->")[0]
					b_coord = (i,k-1,z)
					for x in range (len(table[k,j-1])):
						c = table[k,j-1][x].split("->")[0]
						c_coord = (k,j-1,x)
						rhs = b + " " + c
						if (rhs in grammar_dict):
							table[i,j-1].append(grammar_dict[rhs] + "->" + b + str(b_coord) + " " + c + str(c_coord))
	return table

def find_lex_rule(word,grammar_dict):
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
	if table[0][len(sentence.split())-1][0].split("->")[0] == 'S':
		tree = translate_table(table)
	#print(table[0][len(sentence.split())-1][0].split("->")[0]) #debug

def translate_table(table):
	#grammar rule contains something like this: "S->NP(0, 0, 0) VP(1, 5, 0)"
	grammar_rule = table[0][len(table[0])-1][0]
	#insert rhs of actual grammar rule as root in a binary tree
	tree = BinaryTree(grammar_rule.split("->")[0])
	# contains the coordinates (in the table) of the first lhs of actual grammar rule 
	coord_left = re.findall('\((.*?)\)', grammar_rule)[0].split(", ")
	left_grammar_rule = table[int(coord_left[0]),int(coord_left[1])][int(coord_left[2])]
	tree.insert_left(left_grammar_rule.split("->")[0])

	coord_right = re.findall('\((.*?)\)', grammar_rule)[1].split(", ")
	right_grammar_rule = table[int(coord_right[0]),int(coord_right[1])][int(coord_right[2])].split("->")[0]
	tree.insert_right(right_grammar_rule)
	tree.dfs()
		
	#return tree

if __name__== "__main__":
	main()

