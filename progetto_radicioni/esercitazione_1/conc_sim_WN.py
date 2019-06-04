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
	s1, s2 = words_to_best_senses(words_array[0].get_fst_word(),words_array[0].get_snd_word())
	print(s1, s2)

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


#def wu_and_palmer(sense1, sense2):
	# print(w1.wup_similarity(w2)) quella di wordnet

if __name__== "__main__":
	main()