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
		words_array.append(node)
	file.close()
	global depth_max
	depth_max = depthMax()
	#s1, s2 = words_to_best_senses(words_array[5].get_fst_word(),words_array[5].get_snd_word())
	#print("Wu & Palmer:", wu_and_palmer(s1, s2))
	#print("Shortest path:", shortest_path(s1, s2)) # CONFRONTARE CON QUELLO DELLA LIBRERIA
	#print("Leakcock Chodorow:", leakcock_chodorow(s1, s2)) # CONFRONTARE CON QUELLO DELLA LIBRERIA
	##############################################
	# DA SINGOLO AD ARRAY #
	##############################################
	# Setting the best senses for each entry of words_array
#	print("LENGTH:", len(words_array))
#	for i in range(len(words_array)):
#		elem = words_array[i]
#		s1, s2 = words_to_best_senses(elem.get_fst_word(),elem.get_snd_word())
#		print("i,s1,s2", i,s1,s2)
#		elem.set_fst_word_sense(s1)
#		elem.set_snd_word_sense(s2)
	# Creating array with Wu & Palmer Similarity for each entry of words_array
	wu_and_palmer_array = []
	for i in range(len(words_array)):
		word1 = words_array[i].get_fst_word()
		word2 = words_array[i].get_snd_word()
		wu_and_palmer_array.append(wu_and_palmer(word1,word2))
		print("i,wu_and_palmer_array:", i,wu_and_palmer_array[i])
	# Creating array with Short Path Similarity for each entry of words_array
	shortest_path_array = []
	for i in range(len(words_array)):
		word1 = words_array[i].get_fst_word()
		word2 = words_array[i].get_snd_word()
		shortest_path_array.append(shortest_path(word1,word2))
		print("i,shortest_path_array:", i,shortest_path_array[i])
	# Creating array with Short Path Similarity for each entry of words_array
	leakcock_chodorow_array = []
	for i in range(len(words_array)):
		word1 = words_array[i].get_fst_word()
		word2 = words_array[i].get_snd_word()
		leakcock_chodorow_array.append(leakcock_chodorow(word1,word2))
		print("i,leakcock_chodorow_array:", i,leakcock_chodorow_array[i])

#def spearman(): # NOTA DA FARE SU TUTTO IL FILE, NON SULLE SINGOLE RIGHE

# QUESTI 3 METODI CI PIACCIONO COSI O PREFERIAMO CREARNE UNO SOLO A CUI SI PASSANO LE DUE PAROLE ED UN PARAMETRO CHE INDENTIFICA UNO DEI TRE METODI?
# wu_and_palmer takes two words and returns the Wu & Palmer Similarity considering the two senses that give the maximum similarity
def wu_and_palmer(word1, word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	cs = 0
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synset1:
			for s2 in synset2:	
				# LCS: Lowest Common Subsumer. It is the lower common ancestor between sense1 and sense2, id est the lowest common hypernym
				lcs = s1.lowest_common_hypernyms(s2, simulate_root=True, use_min_depth=True) # VA BENE O DOBBIAMO CALCOLARCELO NOI??? PRIMA DI FARLO MANDEREI UNA MAIL
				# simulate_root=True: fake root that connect the taxonomies that do not share a single root
				# use_min_depth=True: USATO PERCHE USATO NELLA LIBRERIA DI WN. SENZA NON TUTTI SONO UGUALI. LO TENIAMO? SPIEGAZIONE:
				# Note that to preserve behavior from NLTK2 we set use_min_depth=True
		        # It is possible that more accurate results could be obtained by
		        # removing this setting and it should be tested later on
				new_cs = 2*(lcs[0].max_depth()+1) / ((s1.max_depth()+1) + (s2.max_depth()+1))
				# Get the longest path from the LCS to the root, with correction: add one because the calculations include both the start and end nodes
				if(new_cs > cs):
					cs = new_cs
					sense1 = s1
					sense2 = s2
		print("wu_and_palmer WD: ", sense1.wup_similarity(sense2, simulate_root=True))
	return cs
	# VALORI RESTITUITI NON UGUALI: ALCUNI MOLTO DIVERSI, ALTRI POCO

# shortest_path() returns the shortest path length from word1 to word2 considering the two senses that give the maximum similarity
def shortest_path(word1,word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	sim = 0
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synset1:
			for s2 in synset2:
				new_sim = 2*depth_max-s1.shortest_path_distance(s2, simulate_root=True)
				if(new_sim > sim):
					sim = new_sim
					#sense1 = s1
					#sense2 = s2
		#print("shortest_path WD: ", sense1.path_similarity(sense2))
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
			for s2 in synset2:
				length = s1.shortest_path_distance(s2, simulate_root=True)
				if(length == 0):
					new_sim = abs(math.log((length+1)/(2*depth_max+1)))
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
	

# It takes two words and it returns the senses with the highest Wu & Palmer similarity
#def words_to_best_senses(fst_word, snd_word):
#	fst_word_synset = wn.synsets(fst_word)
#	snd_word_synset = wn.synsets(snd_word)
#	fst_word_sense = ""
#	snd_word_sense = ""
#	found = False
#	wup_sim = 0 # LASCIAMO COSì E USIAMO WUP O PASSIAMO PER ARGOMENTO LA FORMULA CHE VOGLIAMO USARE???
#	for s1 in fst_word_synset:
#		for s2 in snd_word_synset:
#			if (s1.wup_similarity(s2) != None and s1.wup_similarity(s2) > wup_sim): # None check: some similarities are missing
#				wup_sim = s1.wup_similarity(s2)
#				fst_word_sense = s1
#				snd_word_sense = s2
#				found = True
#	if(not found):
#		return 0,0
#	return fst_word_sense, snd_word_sense

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

if __name__== "__main__":
	main()