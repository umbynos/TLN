# Conceptual similarity with WordNet

# INPUT
# 2 termini
# Usare WordSim353 (tsv o csv): 2 termini con valore numerico per similarita [0,10]

# OUTPUT
# Punteggio numerico di similarita che indica la vicinanza semantica dei termini in input

# SCALA PUNTEGGI
# Compreso nell'intervallo [0,1]: 0 completamente dissimile; 1 identita

# Sfruttare la struttura ad albero di WordNet per calcolare la vicinanza semantica
# Documentazione: https://wordnet.princeton.edu/documentation/wnintro3wn

# SVOLGIMENTO
# Trovare la vicinanza semantica con 3 diverse misure:
#	- Wu & Palmer
#	- Shortest Path
#	- Leacock & Chodorow
# Per ciascuna misura di similarita calcolare:
#	- gli indici di correlazioine di Spearman
#	- gli indici di correlazioine di Pearson confrontando il risultato ottenuto con quello presente all'interno del file

# NOTA
# input: coppie di termini;
# formula: sensi
# Quindi per disambiguare si prendono i sensi con la massima similarita

import sys
from node_structure import Node
from itertools import islice
from nltk.corpus import wordnet as wn
import math
import numpy as np
import pandas as pd

def main():
	# Saving the file in an array structure. Each element is a node_structure
	words_file = sys.argv[1] # The file is given by argument
	file = open(words_file,"r")
	words_array = []
	for line in islice(file, 1, None): # don't read the first line, start from 1: first line contains an introduction
		fst_word = line.split("\t")[0]
		snd_word = line.split("\t")[1]
		similarity = line.split("\t")[2]
		node = Node(fst_word, snd_word, similarity)
		words_array.append(node) # TRASFORMARE IN MATRICE?
	file.close()
	# Depth of WordNet structure
	global depth_max
	depth_max = depthMax()
	# METTIAMO POI TUTTO IN UN CILCLO UNICO
	wu_and_palmer_sim_indexes = [] # List with Wu & Palmer Similarity for each entry of words_array
	shortest_path_sim_indexes = [] # List with Shortest Path Similarity for each entry of words_array
	leacock_chodorow_sim_indexes = [] # List with Leacock Chodorow Similarity for each entry of words_array
	for i in range(len(words_array)):
		word1 = words_array[i].get_fst_word()
		word2 = words_array[i].get_snd_word()
		print("words:",word1,word2)
		wu_and_palmer_sim_indexes.append(float(wu_and_palmer(word1,word2)))
		print("wu_and_palmer nostro:", wu_and_palmer_sim_indexes[i])
		shortest_path_sim_indexes.append(shortest_path(word1,word2))
		print("shortest_path:", shortest_path_sim_indexes[i])
		leacock_chodorow_sim_indexes.append(leacock_chodorow(word1,word2))
		print("leacock_chodorow nostro:",leacock_chodorow_sim_indexes[i])
		print()
	# Correlation indexes
	sim_indexes = []
	# for elem in words_array:
	#  	sim_indexes.append(float(elem.get_similarity()))
	# print("Pearson, WUP: ", pearson(sim_indexes, wu_and_palmer_sim_indexes))
	# print("Pearson, SP: ", pearson(sim_indexes, shortest_path_sim_indexes))
	# # print("Pearson, LC: ", pearson(sim_indexes, leacock_chodorow_sim_indexes))
	# print("Spearman, WUP: ", spearman(sim_indexes, wu_and_palmer_sim_indexes))
	# print("Spearman, SP: ", spearman(sim_indexes, shortest_path_sim_indexes))
	# # print("Spearman, LC: ", spearman(sim_indexes, leacock_chodorow_sim_indexes))

# wu_and_palmer takes two words and returns the Wu & Palmer Similarity considering the two senses that give the maximum similarity
def wu_and_palmer(word1, word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	cs = 0
	sense1 = None
	sense2 = None
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase #RITORNARE -1
		for s1 in synset1:
			for s2 in synset2:	
				# LCS: Lowest Common Subsumer. It is the lower common ancestor between sense1 and sense2, id est the lowest common hypernym
				lcs = lowest_common_subsumer(s1, s2)
				if lcs: # not all senses have a root in common
					new_cs = 2*(lcs.max_depth()+1) / ((s1.max_depth()+1) + (s2.max_depth()+1)) # CHIEDERE AGLI ALTRI PER IL +1
					# Get the longest path from the LCS to the root, with correction: add one because the calculations include both the start and end nodes
					# max_depth(): if there are more possibilities, it is taken the one with the longest minimum distance from the root
					# MAX_DEPTH DOBBIAMO IMPLEMENTARLO NOI???????? POSSIAMO SALVARLO QUANDO CALCOLIAMO LCS
					if(new_cs > cs):
						cs = new_cs
						sense1 = s1
						sense2 = s2
		if sense1 and sense2: # not all senses have a root in common
			print("wu_and_palmer WD: ", sense1.wup_similarity(sense2))
	#print("sensi wu_and_palmer", sense1,sense2)
	return cs # QUALCHE RISULTATO è UN FILO DIVERSO (+-0.3). SCEGLIERE MEGLIO L'IPERONIMO COMUNE?

# Get a list of lowest synset(s) that both synsets have as a hypernym. # NON UNA LISTA. UNO SOLO..TANTO CI BASTA
def lowest_common_subsumer(sense1, sense2):
	paths1 = hypernym_paths(sense1)
	paths2 = hypernym_paths(sense2)
	common_hypernym = None
	position = -1
	for path1 in paths1:
		for path2 in paths2:
			for i in range(len(path1)-1, -1, -1):
				for j in range(len(path2)-1, -1, -1):
					if path1[i]==path2[j] and (i>position or j>position):
						common_hypernym = path1[i]
						position = max(i, j)
	return common_hypernym

# hypernym_paths(sense) return paths list: a list of lists, each list gives the node sequence from a root to sense
def hypernym_paths(sense):
	paths = []
	hypernyms = sense.hypernyms()
	if len(hypernyms) == 0:
		paths = [[sense]]
	for hypernym in hypernyms:
		for ancestor_list in hypernym.hypernym_paths():
			ancestor_list.append(sense)
			paths.append(ancestor_list)
	return paths

# shortest_path() returns the shortest path length from word1 to word2 considering the two senses that give the maximum similarity
def shortest_path(word1,word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	# senso1 = None
	# senso2 = None
	sim = None
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synset1:
			for s2 in synset2:
				shortest_path_distance = lowest_common_subsumer_shortest_path(s1,s2)
				if shortest_path_distance:
					new_sim = 2*depth_max-shortest_path_distance
					if not sim or new_sim<sim: # not sim: first assignment, sim is None
						sim = new_sim
						# senso1 = s1
						# senso2 = s2
		# NON HO TROVATO IL CORRISPETTIVO IN WN
	# if senso1 and senso2:
	# 	print("sensi shortest_path",s1,s2)
	return sim

# CONTROLLATO, NON CONSIDERA GLI STESSI DELL'ALTRO. NON SAPREI COME UNIRLI. CAMBIARE NOME
def lowest_common_subsumer_shortest_path(sense1, sense2):
	paths1 = hypernym_paths(sense1)
	paths2 = hypernym_paths(sense2)
	best_len_path = None
	for path1 in paths1:
		for path2 in paths2:
			for i in range(len(path1)-1, -1, -1):
				for j in range(len(path2)-1, -1, -1):
					if path1[i]==path2[j]:
						# if a match is found, the number of step from the senses to their common hypernym is computed
						len_path = (len(path1)-1)-i + (len(path2)-1)-j
						if not best_len_path or len_path<best_len_path: # not best_len_path: first assignment, best_first_path is None
							best_len_path = len_path
	return best_len_path

# leacock_chodorow() returns the Leacock Chodorow Similarity considering the two senses that give the maximum similarity
def leacock_chodorow(word1, word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	sim = 0
	found = False # the similarity is computed only if the parameters have at least one sense in common with the same POS
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synset1:
			for s2 in synset2:
				length = s1.shortest_path_distance(s2, simulate_root=True)
				if(length == 0):
					new_sim = abs(math.log((length+1)/(2.0*depth_max+1))) # 
				else:
					new_sim =  abs(math.log((length+1)/(2.0*depth_max)))
				if(new_sim>sim and s1._pos==s2._pos):
					sim = new_sim
					sense1 = s1
					sense2 = s2
					found = True
	if(found):
		print("leakock_chodorow WD: ", sense1.lch_similarity(sense2, simulate_root=False))
		return sim
	else:
		print(found)
		return -1

# depthMax() returns the maximum depth of WordNet's structure
def depthMax(): # CONTROLLARNE LA CORRETTEZZA. USARE IL NOSTRO HYPERNYM_PATHS?????
	max_hyp_path = 0
	max_all = 0
	for synset in wn.all_synsets():
		for hyp_path in synset.hypernym_paths():
			if(len(hyp_path) > max_hyp_path):
				max_hyp_path = len(hyp_path)
		if(max_hyp_path > max_all):
			max_all = max_hyp_path
	return max_all

# spearman() returns the Spearman's correlation indexes
def spearman(similarities, indexes_sim):
	similarities.sort()
	indexes_sim.sort() # PROVARE A STAMPARE PER VEDERE COME ORDINA: ORDINA IN MODO CORRETTO
	return pearson(similarities, indexes_sim) # VALORI MOLTO PIU ALTI RISPETTO AGLI ALTRI!!

def pearson(fst, snd):
	# if no similiraity is found, the elem are removed
	print("len fst", len(fst))
	print("len snd", len(snd))
	for i in range(len(fst)):
		for j in range(len(snd)):
			print("fst, i",fst[i],i)
			print("snd, j",snd[j],j)
			if fst[i] == None or snd[j] == None:
				fst.pop(i)
				snd.pop(j)
	arr1 = np.asarray(fst)
	arr2 = np.asarray(snd)
	std1 = arr1.std()
	std2 = arr2.std()
	return ((arr1*arr2).mean()-arr1.mean()*arr2.mean())/(std1*std2)

if __name__== "__main__":
	main()