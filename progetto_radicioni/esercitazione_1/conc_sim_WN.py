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
	for line in islice(file, 1, None): # don't read the first line: it contains an introduction
		fst_word = line.split("\t")[0]
		snd_word = line.split("\t")[1]
		similarity = line.split("\t")[2]
		node = Node(fst_word, snd_word, similarity)
		words_array.append(node)
	file.close()
	s1, s2 = words_to_best_senses(words_array[5].get_fst_word(),words_array[5].get_snd_word())
	print("Wu & Palmer:", wu_and_palmer(s1, s2))
	print("Shortest path:", shortest_path(s1, s2)) # CONFRONTARE CON QUELLO DELLA LIBRERIA
	print("Leakcock Chodorow:", leakcock_chodorow(s1, s2)) # CONFRONTARE CON QUELLO DELLA LIBRERIA
	##############################################
	# DA SINGOLO AD ARRAY #
	##############################################
	# come salviamo sense?
	# altri campi in node_structure? Forse è meglio, tanto li riempi subito e tutti
	# metterli al posto di word? cercando una parola che vada bene per entrambi. MAH, poi non sai cos'hai
	# creare 2 strutture differenti? Pare eccessivo: devi ricopiare il valore dato all'inizio
	# NOTA: node_structure come nome non va bene: sono inseriti in un array, non sono collegati fra di loro!!!!!!!!!!!!!

# It takes two words and it returns the senses with the highest Wu & Palmer similarity
def words_to_best_senses(fst_word, snd_word):
	fst_word_synset = wn.synsets(fst_word)
	snd_word_synset = wn.synsets(snd_word)
	fst_word_sense = ""
	snd_word_sense = ""
	wup_sim = 0 # LASCIAMO COSì E USIAMO WUP O PASSIAMO PER ARGOMENTO LA FORMULA CHE VOGLIAMO USARE???
	for s1 in fst_word_synset:
		for s2 in snd_word_synset:
			if (s1.wup_similarity(s2) != None and s1.wup_similarity(s2) > wup_sim): # None check: some similarities are missing
				wup_sim = s1.wup_similarity(s2)
				fst_word_sense = s1
				snd_word_sense = s2
	return s1, s2

#def spearman(): # NOTA DA FARE SU TUTTO IL FILE, NON SULLE SINGOLE RIGHE

def wu_and_palmer(sense1, sense2):
	# LCS: Lowest Common Subsumer. It is the lower common ancestor between sense1 and sense2, id est the lowest common hypernym
	lcs = sense1.lowest_common_hypernyms(sense2, simulate_root=True) # VA BENE O DOBBIAMO CALCOLARCELO NOI??? PRIMA DI FARLO MANDEREI UNA MAIL
	# simulate_root=True: some taxonomies do not share a single root which disallows this metric from working for synsets that are not connected
	# This flag (False by default) creates a fake root that connects all the taxonomies
	cs = 2*lcs[0].min_depth()/(sense1.min_depth()+sense2.min_depth())
	# min_depth() returns the length of the shortest hypernym path from this synset to the root
	print("Valore di WN per wup:", sense1.wup_similarity(sense2))
	return cs
	# VALORI RESTITUITI NON UGUALI: ALCUNI MOLTO DIVERSI, ALTRI POCO

# shortest_path() returns the shortest path length from sense1 to sense2 (the parmeters)
def shortest_path(sense1,sense2):
	return 2*depthMax()-sense1.shortest_path_distance(sense2, simulate_root=True)

# leakock_chodorow() returns the Leakcock Chodorow Similarity
def leakcock_chodorow(sense1, sense2):
	len = sense1.shortest_path_distance(sense2, simulate_root=True)
	if(len == 0):
		return -math.log((len+1)/(2*depthMax()+1))
	else:
		return -math.log(len/2*depthMax())

# depthMax() returns the maximum depth of WordNet's structure
def depthMax():
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