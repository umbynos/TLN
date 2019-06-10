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
#	- Leakcock & Chodorow
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
	for line in islice(file, 1, None): # don't read the first line, start from 1: it contains an introduction
		fst_word = line.split("\t")[0]
		snd_word = line.split("\t")[1]
		similarity = line.split("\t")[2]
		node = Node(fst_word, snd_word, similarity)
		words_array.append(node) # TRASFORMARE IN MATRICE?
	file.close()
	global depth_max
	depth_max = depthMax()
	# Creating array with Wu & Palmer Similarity for each entry of words_array
	wu_and_palmer_sim_indexes = []
	for i in range(len(words_array)):
		word1 = words_array[i].get_fst_word()
		word2 = words_array[i].get_snd_word()
		wu_and_palmer_sim_indexes.append(float(wu_and_palmer(word1,word2)))
		print("i,wu_and_palmer_sim_indexes:", i,wu_and_palmer_sim_indexes[i])
	# Creating array with Short Path Similarity for each entry of words_array
	shortest_path_sim_indexes = []
	for i in range(len(words_array)):
		word1 = words_array[i].get_fst_word()
		word2 = words_array[i].get_snd_word()
		shortest_path_sim_indexes.append(shortest_path(word1,word2))
		print("i,shortest_path_sim_indexes:", i,shortest_path_sim_indexes[i])
	# Creating array with Short Path Similarity for each entry of words_array
	leakcock_chodorow_sim_indexes = []
	for i in range(len(words_array)):
		word1 = words_array[i].get_fst_word()
		word2 = words_array[i].get_snd_word()
		leakcock_chodorow_sim_indexes.append(leakcock_chodorow(word1,word2))
		print("i,leakcock_chodorow_sim_indexes:", i,leakcock_chodorow_sim_indexes[i])
	# Correlation indexes
	sim_indexes = []
	for elem in words_array:
		sim_indexes.append(float(elem.get_similarity()))
	print("Pearson, WUP: ", pearson(sim_indexes, wu_and_palmer_sim_indexes))
	print("Pearson, SP: ", pearson(sim_indexes, shortest_path_sim_indexes))
	print("Pearson, LC: ", pearson(sim_indexes, leakcock_chodorow_sim_indexes))
	print("Spearman, WUP: ", spearman(sim_indexes, wu_and_palmer_sim_indexes))
	print("Spearman, SP: ", spearman(sim_indexes, shortest_path_sim_indexes))
	print("Spearman, LC: ", spearman(sim_indexes, leakcock_chodorow_sim_indexes))

# QUESTI 3 METODI CI PIACCIONO COSI O PREFERIAMO CREARNE UNO SOLO A CUI SI PASSANO LE DUE PAROLE ED UN PARAMETRO CHE INDENTIFICA UNO DEI TRE METODI?
# wu_and_palmer takes two words and returns the Wu & Palmer Similarity considering the two senses that give the maximum similarity
def wu_and_palmer(word1, word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	cs = 0
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase #RITORNARE -1
		for s1 in synset1:
			for s2 in synset2:	
				# LCS: Lowest Common Subsumer. It is the lower common ancestor between sense1 and sense2, id est the lowest common hypernym
				lcs = s1.lowest_common_hypernyms(s2, simulate_root=True, use_min_depth=True) # VA BENE O DOBBIAMO CALCOLARCELO NOI??? PRIMA DI FARLO MANDEREI UNA MAIL
				# simulate_root=True: fake root that connect the taxonomies that do not share a single root
				# use_min_depth=True: USATO PERCHE USATO NELLA LIBRERIA DI WN. SENZA NON TUTTI SONO UGUALI. LO TENIAMO? SPIEGAZIONE:
				# Note that to preserve behavior from NLTK2 we set use_min_depth=True
		        # It is possible that more accurate results could be obtained by
		        # removing this setting and it should be tested later on
				new_cs = 2*(lcs[0].max_depth()+1) / ((s1.max_depth()+1) + (s2.max_depth()+1)) # CHIEDERE AGLI ALTRI PER IL +1
				# Get the longest path from the LCS to the root, with correction: add one because the calculations include both the start and end nodes
				# max_depth(): if there are more possibilities, it is taken the one with the longest minimum distance from the root
				if(new_cs > cs):
					cs = new_cs
					sense1 = s1
					sense2 = s2
		print("wu_and_palmer WD: ", sense1.wup_similarity(sense2, simulate_root=True))
	return cs

# shortest_path() returns the shortest path length from word1 to word2 considering the two senses that give the maximum similarity
def shortest_path(word1,word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	sim = 0
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synset1:
			for s2 in synset2:
				new_sim = 2*depth_max-s1.shortest_path_distance(s2, simulate_root=True) # DOBBIAMO IMPLEMENTARLO NOI??
				if(new_sim > sim):
					sim = new_sim
		# NON HO TROVATO IL CORRISPETTIVO IN WN
	return sim

# leakock_chodorow() returns the Leakcock Chodorow Similarity considering the two senses that give the maximum similarity
def leakcock_chodorow(word1, word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	sim = 0
	found = False # the similarity is computed only if the parameters have at least one sense in common with the same POS
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synset1:
			need_root = s1._needs_root()
			for s2 in synset2:
				length = s1.shortest_path_distance(s2, simulate_root=True)
				if(length == 0):
					new_sim = abs(math.log((length+1)/(2*depth_max+1))) # 
				else:
					new_sim =  abs(math.log(length/2*depth_max))
				if(new_sim>sim and s1._pos==s2._pos):
					sim = new_sim
					sense1 = s1
					sense2 = s2
					found = True
	if(found):
		print("leakock_chodorow WD: ", sense1.lch_similarity(sense2))
		return sim
	else:
		print(found)
		return -1

# depthMax() returns the maximum depth of WordNet's structure
def depthMax(): # CONTROLLARNE LA CORRETTEZZA
	max_hyp_path = 0
	max_all = 0
	for synset in wn.all_synsets():
		for hyp_path in synset.hypernym_paths():
			if(len(hyp_path) > max_hyp_path):
				max_hyp_path = len(hyp_path)
		if(max_hyp_path > max_all):
			max_all = max_hyp_path
	return max_all
	# max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets()) ERA COSI!! ALLUCINANTE!!

# spearman() returns the Spearman's correlation indexes
def spearman(similarities, indexes_sim):
	similarities.sort()
	indexes_sim.sort()
	return pearson(similarities, indexes_sim) # VALORI MOLTO PIU ALTI RISPETTO AGLI ALTRI!!

def pearson(fst, snd):
	arr1 = np.asarray(fst)
	arr2 = np.asarray(snd)
	std_dev_sim = np.std(fst)
	std_dev_wup = np.std(snd)
	std1 = arr1.std()
	std2 = arr2.std()
	return ((arr1*arr2).mean()-arr1.mean()*arr2.mean())/(std1*std2)

if __name__== "__main__":
	main()