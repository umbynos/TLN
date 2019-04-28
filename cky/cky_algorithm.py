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

#create_dict will create a dictionary, it uses rhs as key and lhs as value 
def create_dict(grammar_file):
	file = open(grammar_file,"r")
	grammar_dict = {}
	for line in file:
		lhs = line.split("->")[0]
		rhs = line.split("->")[1]
		grammar_dict[rhs.strip('\n')] = lhs
	return grammar_dict

def main():
	grammar_file = sys.argv[1]
	sentence = sys.argv[2]
	grammar_dict = create_dict(grammar_file)
	table = cky_parse(sentence.split(), grammar_dict)
	print(table)
	lhs_start = table[0][len(sentence.split())-1][0].split("->")[0]
	if lhs_start == 'S': #check if the sentence is syntactically correct
		#contains something like this: "S->NP(0, 0, 0) VP(1, 5, 0)"
		starting_grammar_rule = table[0][len(table[0])-1][0]
		tree = table_to_tree(table, starting_grammar_rule)
		print()
		tree.print_leaves()
		print()

def table_to_tree(table, grammar_rule):
	lhs = grammar_rule.split("->")[0]
	rhs = grammar_rule.split("->")[1]
	#insert lhs of actual grammar rule as root in a binary tree
	tree = BinaryTree(lhs)
	if re.search('\((.*?)\)', rhs): #check if the rhs contains the coordinates -> then it's not a terminal
		#contains the coordinates (in the table) of the first lhs of actual grammar rule
		coord_left = re.findall('\((.*?)\)', grammar_rule)[0].split(", ")
		left_grammar_rule = table[int(coord_left[0]),int(coord_left[1])][int(coord_left[2])]
		tree.insert_left(table_to_tree(table, left_grammar_rule)) #recursive call
		#contains the coordinates (in the table) of the second lhs of actual grammar rule
		coord_right = re.findall('\((.*?)\)', grammar_rule)[1].split(", ")
		right_grammar_rule = table[int(coord_right[0]),int(coord_right[1])][int(coord_right[2])]
		tree.insert_right(table_to_tree(table, right_grammar_rule)) #recursive call
	else:
		#insertion of the word into the tree in case there is a word
		tree.insert_leaf(rhs)
	return tree

if __name__== "__main__":
	main()