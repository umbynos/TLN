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

from itertools import islice
from io import StringIO
import numpy as np
import json
import gzip
import requests
from nltk.corpus import wordnet as wn
import math
import scipy

def main():
	corpora_ro = infer_file("words_ro.txt")
	corpora_umbo = infer_file("words_umbo.txt")
	avg = average(corpora_ro, corpora_umbo)
	# Computing inter-rater agreement (correlation indexes)
	sim_ro = infer_sim(corpora_ro)
	sim_umbo = infer_sim(corpora_umbo)
	corr_pearson, p_value_pearson = scipy.stats.pearsonr(sim_ro,sim_umbo)
	print("Pearson:", corr_pearson, "\n")
	# corr_pearson_SP, p_value_pearson_SP = scipy.stats.pearsonr(sim,shortest_path_sim)
	corr_spearman, p_value_spearman = scipy.stats.spearmanr(sim_ro, sim_umbo)
	print("Spearman:", corr_spearman, "\n")
	# Saving nasari vectors in a structure
	nasari_vectors = nasari_to_vectors()
	sem_eval_vectors = sem_eval_to_vectors()
	best_senses = senseIdentification(corpora_ro, nasari_vectors, sem_eval_vectors)
	for elem in best_senses:
	 	print("sense first word:", elem[0])
	 	find_gloss(elem[0])
	 	print("sense second word:", elem[1])
	 	find_gloss(elem[1])
	 	print()

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

def cosine_similarity(v1,v2):
    #"compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

# senseIdentification() returns the cosine similarity for each pair of words that are in the parameter words
def senseIdentification(words, nasari_vectors, sem_eval_vectors):
	best_senses = []
	# For every pair in words file ...
	for elem_words in words:
		final_senses = []
		fst_word = elem_words[0]
		snd_word = elem_words[1]
		fst_word_synset = None
		snd_word_synset = None
		fst_word_vector = None
		snd_word_vector = None
		fst_vector_number = []
		snd_vector_number = []
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
							fst_vector_number.append(float(fst_word_vector[k]))
							snd_vector_number.append(float(snd_word_vector[k]))
						new_cos_sim = cosine_similarity(fst_vector_number, snd_vector_number)
						fst_vector_number.clear()
						snd_vector_number.clear()
						if new_cos_sim>cos_sim:
							final_senses.clear()
							fst_word_sense = fst_word_synset[i]
							final_senses.append(fst_word_sense)
							snd_word_sense = snd_word_synset[j]
							final_senses.append(snd_word_sense)
							cos_sim = new_cos_sim
							#final_senses.append(cos_sim)
		if final_senses:
			best_senses.append(final_senses)
	return best_senses

def found(elem):
	return elem

def find_gloss(bn_id):
	service_url = 'https://babelnet.io/v5/getSynset'

	id = bn_id
	key  = 'aa3561e2-0643-4541-90bd-b39b44fe1dca'

	params = {
		'id' : id,
		'key'  : key
	}
	res = requests.get(service_url, params=params, headers={'Accept-encoding':'gzip'})
	if res.headers['Content-Encoding'] == 'gzip':
		buf = StringIO(res.text)
		data = json.loads(buf.getvalue())
		# finding all the glosses
		glosses = data['glosses']
		for result in glosses:
			gloss = result.get('gloss')
			language = result.get('language')
			print(str(language.encode('utf-8')) + "\t" + str(gloss.encode('utf-8')))

if __name__== "__main__":
	main()