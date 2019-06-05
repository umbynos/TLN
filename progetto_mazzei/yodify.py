import sys
import re
from tree import Tree
import cky_algorithm as cky

#create_dict will create a dictionary, it uses rhs as key and lhs as value 
def create_dict(grammar_file):
	file = open(grammar_file,"r")
	grammar_dict = {}
	for line in file:
		lhs = line.split("->")[0]
		rhs = line.split("->")[1]
		grammar_dict[rhs.strip('\n')] = lhs
	file.close()
	return grammar_dict

def main():
	grammar_file = sys.argv[1]
	sentence = sys.argv[2]
	grammar_dict = create_dict(grammar_file)
	table = cky.cky_parse(sentence.split(), grammar_dict)
	print(table)
	#contains something like this: "S->NP(0, 0, 0) VP(1, 5, 0)"
	starting_grammar_rule = table[0][len(table[0])-1][0]
	#take the lsh of the first rule in the table to verify that is 'S'
	if starting_grammar_rule.split("->")[0] == 'S': #check if the sentence is syntactically correct
		tree = table_to_tree(table, starting_grammar_rule)
		print()
		tree.print_leaves()
		print()
		yodify(tree)
		tree.print_leaves()
		print()

def table_to_tree(table, grammar_rule):
	lhs = grammar_rule.split("->")[0]
	rhs = grammar_rule.split("->")[1]
	#insert lhs of actual grammar rule as root in a binary tree
	tree = Tree(lhs)
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

def yodify(tree):
	subject = tree.search_left('NP') #the subject is located in the left side of the three
	x = tree.take_right_child() #the right side of the tree contains everything else
	v = x.search_left('V') #the ver is in the leftest side of X
	tree.insert_left(x) 
	yoda = Tree('YODA') #create a artificial node with value 'YODA'
	yoda.insert_left(subject)
	yoda.insert_right(v)
	tree.insert_right(yoda) #place YODA subtree in the original tree in the right side

if __name__== "__main__":
	main()