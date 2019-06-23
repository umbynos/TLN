# Corpora and Sense Identification
# Task: Semantic Word Similarity

#########################
# SVOLGIMENTO
#########################

# ANNOTAZIONE
# Annotare a mano con un punteggio da 0 a 4 (decimali compresi) la samilarità tra 100 coppie di termini (words.txt):
# - 4: molto simimli -> sinonimi
# - 3: simili -> le parole condiviono molto, ma non si riferiscono allo stesso concetto (es leone e zebra)
# - 2: leggermente simili -> le parole non hanno un significato molto simile, ma condividono lo stesso argomento, dominio, funzione oppure sono correlati (es casa e finestra)
# - 1: diversi -> le due parole sono diverse, ma potrebbero avere piccoli dettagli che le accomunino; potrebbero essere trovato in un articolo che tochi il loro argomento (es: software e tastiera)
# - 0: completamente diversi -> le due parole non hanno lo stesso significato e appartengono a topic diversi (es: biro e rana)
# Avremo quindi un file di 100 linee ciascuna contenente due parole seguite da un numero in [0,4]. NOTA: magari inserisci anche un commento sulla motivazione che ti ha spinto a mettere quel valore
# Dobbiamo calcolare il valore medio dato dagli annotatori e l'iner-rater agreement (sempre basandosi sui numeri dati da noi. Qui usiamo Pearson e Spearman)
# NOTA: NEL CORPUS CI SONO DEGLI ACCENTI. SE HAI PROBLEMI SAPPILO

# Sense Identification
# Nell’attribuire un valore di similarità a una coppia di termini (per esempio, società e cultura) quali sensi vengono selezionati?
# Partiamo dall’assunzione che i due termini funzionino come contesto di disambiguazione l’uno per l’altro.
# Calcolare la similarità come il massimo ottenuto (come per es 1) utilizzando come metrica la cosine-similarity fra i vettori NASARI dei sensi associati ai vari termini
# A differenza di quanto fatto nella prima esercitazione, ora non siamo interessati a calcolare il punteggio di similarità fra 2 termini, ma a individuare i sensi che massimizzano tale punteggio
# Si tratta quindi di eseguire questa operazione: c1, c2 = argmax [sim(c1,c2)] con c1€s(w1) e c2€s(w2) [prima era sim(w1,w2)=...]

# OUTPUT 
# 2 BabelNet synset ID e dalla relativa glossa (la glossa serve perche il synset id ci dice molto poco)
# Valutiamo il risultato ottenuto (cioè la coppia dei sensi identificati, e la relativa appropriatezza) direttamente,
# stabilendo se i sensi in questione sono quelli idealmente selezionati da noi stessi nel momento dell’annotazione [a mano]
# Misuriamo in questo caso l’accuratezza sia sui singoli elementi, sia sulle coppie
# NB: per questa valutazione non è necessario conoscere il BabelNet synset ID corretto, ma è sufficiente valutare sulla base della glossa, se il senso individuato è appropriato.

# ORA DEVI STAMPARE LA GLOSSA CHE CORRISPONDE ALL'ID TROVATO
# TROVATO PACKAGE ONLINE, MA NON RIESCO A SCARICARLO: http://babelscape.com/doc/pythondoc/modules.html

from itertools import islice
from scipy import spatial
import numpy as np

def main():
	corpora_ro = infer_file("words_ro.txt")
	corpora_umbo = infer_file("words_umbo.txt")
	avg = average(corpora_ro, corpora_umbo)
	# Computing inter-rater agreement
	sim_ro = infer_sim(corpora_ro)
	sim_umbo = infer_sim(corpora_umbo)
	pearson_index = pearson(sim_ro, sim_umbo)
	print("Pearson:", pearson_index, "\n")
	spearman_index = spearman(sim_ro, sim_umbo)
	print("Spearman:", spearman_index, "\n")
	# Saving nasari vectors in a structure
	nasari_vectors = nasari_to_vectors()
	sem_eval_vectors = sem_eval_to_vectors()
	senseIdentification(corpora_ro, nasari_vectors, sem_eval_vectors)

# infer_file returns the array corpora
# Each element of corpora represents a line of words file and it contains the first and the second words followed by the similarity given in the file
def infer_file(file):
	file = open(file,"r")
	corpora = []
	for line in islice(file, 1, None): # don't read the first line, start from 1: first line contains an introduction
		fst_word = line.split("\t")[0]
		snd_word = line.split("\t")[1]
		similarity = line.split("\t")[2].strip('\n')
		elem = []
		elem.append(fst_word)
		elem.append(snd_word)
		elem.append(similarity)
		corpora.append(elem)
	file.close()
	return corpora

# nasari_to_vectors() returns nasari_vectors
# Each element of nasari_vector represents a line of the mini nasari file
def nasari_to_vectors():
	file = open("mini_NASARI.tsv","r")
	nasari_vectors = []
	for line in file:
		elem = []
		for i in range (301):
			elem.append(line.split("\t")[i].strip('\n'))
		nasari_vectors.append(elem)
	file.close()
	return nasari_vectors

# sem_eval_to_vectors() returns sem_eval_vectors
# Each element represents a word followed by its BabelNet synsets
def sem_eval_to_vectors():
	file = open("SemEval17_IT_senses2synsets.txt","r")
	sem_eval_vectors = []
	elem = []
	for line in file:
		if "#" in line:
			if(len(elem)>0): # we aren't in the first line
				sem_eval_vectors.append(elem)
				elem = []
			elem.append(line.strip('\n'))
		else:
			elem.append(line.strip('\n'))
	file.close()
	return sem_eval_vectors

def infer_sim(corpora):
	sim = []
	for elem in corpora:
		sim.append(float(elem[2]))
	return sim

def average(fst, snd):
	if len(fst) != len(snd):
		print("Arguments have different lengths")
		return -1
	print("MEDIA")
	avg = []
	for i in range(len(fst)):
		average = (float(fst[i][2])+(float(snd[i][2]))) / 2
		elem = []
		elem.append(fst[i][0])
		elem.append(fst[i][1])
		elem.append(round(average, 2)) # SENZA ROUND OGNI TANTO VENIVANO FUORI NUMERI MOLTO MOLTO VICINI, MA LUNGHI
		avg.append(elem)
		print(avg[i])
	print()
	return avg

# UGUALI A QUELLI DELL'ES 1. LIBRERIA?????????
# spearman() returns the Spearman's correlation indexes
def spearman(fst, snd):
	fst.sort()
	snd.sort()
	return pearson(fst, snd) # VALORI MOLTO PIU ALTI RISPETTO AGLI ALTRI!!

def pearson(fst, snd):
	arr1 = np.asarray(fst)
	arr2 = np.asarray(snd)
	std_dev_sim = np.std(fst)
	std_dev_wup = np.std(snd)
	std1 = arr1.std()
	std2 = arr2.std()
	pearson_index = ((arr1*arr2).mean()-arr1.mean()*arr2.mean())/(std1*std2)
	return pearson_index

# senseIdentification() returns the cosine similarity for each pair of words that are in the parameter words
def senseIdentification(words, nasari_vectors, sem_eval_vectors):
	# For every pair in words file ...
	for elem_words in words:
		fst_word = elem_words[0]
		snd_word = elem_words[1]
		fst_word_synset = None
		snd_word_synset = None
		fst_word_vector = None
		snd_word_vector = None
		fst_vector_int = []
		snd_vector_int = []
		cos_sim = 0
		fst_word_sense = None
		snd_word_sense = None
		# ... the BabelNet synset of each word (presents in SemEval file) is taken...
		for elem_sem_eval in sem_eval_vectors: # SE HAI TROVATO ENTRAMBI PUOI SMETTERE
			if fst_word in elem_sem_eval[0]:
				fst_word_synset = elem_sem_eval
			if snd_word in elem_sem_eval[0]:
				snd_word_synset = elem_sem_eval
		# ... for each BeblNet sysnet found ...
		if(found(fst_word_synset) and found(snd_word_synset)):
			for i in range(1, len(fst_word_synset)): # 1...len-1
				for j in range(1, len(snd_word_synset)):
					# ... a NASARI vector is searched ...
					for elem_nasari in nasari_vectors: # SE HAI TROVATO ENTRAMBI PUOI SMETTERE
						if fst_word_synset[i] in elem_nasari[0]:
							fst_word_vector = elem_nasari
						if snd_word_synset[j] in elem_nasari[0]:
							snd_word_vector = elem_nasari
					# ... if for both the senses a NASARI vector is found ...
					if(found(fst_word_vector) and found(snd_word_vector)):
						# ... their cosine similarity is computed
						for k in range(1, len(fst_word_vector)):
							fst_vector_int.append(float(fst_word_vector[k]))
							snd_vector_int.append(float(snd_word_vector[k]))
						new_cos_sim = 1 - spatial.distance.cosine(fst_vector_int, snd_vector_int)
						if new_cos_sim>cos_sim:
							cos_sim = new_cos_sim
							fst_word_sense = fst_word_synset[i]
							snd_word_sense = snd_word_synset[j]
		print("coppia", fst_word,snd_word)
		print("sensi", fst_word_sense,snd_word_sense)
		print("cosine similarity", cos_sim)
		print()

def found(elem):
	if elem is None:
		return False
	else:
		return True

if __name__== "__main__":
	main()