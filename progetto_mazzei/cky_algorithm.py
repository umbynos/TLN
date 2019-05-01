import numpy as np

def cky_parse(words,grammar_dict):
	table = init_matrix(len(words))
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

def init_matrix(dim):
	table = np.empty((dim, dim) ,dtype = 'object')
	for a in range (dim):
		for b in range (dim):
			table[a,b] = []
	return table