# Conceptual similarity with WordNet

# INPUT
# 2 termini
# Usare WordSim353 (tsv o csv): 2 termini con valore numerico per similarità [0,10]

# OUTPUT
# Punteggio numerico di similarità che indica la vicinanza semantica dei termini in input

# SCALA PUNTEGGI
# Compreso nell'intervallo [0,1]: 0 completamente dissimile; 1 identità

# Sfruttare la struttura ad albero di WordNet

# SVOLGIMENTO
# Trovare la vicinanza semantica con 3 diverse misure:
#	- Wu & Palmer
#	- Shortest Path
#	- Leakcock & Chodorow
# Per ciascuna misura di similarità calcolare:
#	- gli indici di correlazioine di Spearman
#	- gli indici di correlazioine di Pearson confrontando il risultato ottenuto con quello presente all'interno del file

# NOTA
# input: coppie di termini;
# formula: sensi
# Quindi per disambiguare si prendono i sensi con la massima similarità



###################################
# Saving WordSim353 in a matrix structure
###################################

def main():
	words_file = sys.argv[1]
	file = open(words_file,"r")
	words_similarity = {}
	for line in file:
		fst_word = line.split(",")[0]
		snd_word = line.split(",")[1]
		
	file.close()
	return grammar_dict
















