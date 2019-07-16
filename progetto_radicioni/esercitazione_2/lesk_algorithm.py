from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import word_tokenize
import string

stop = stopwords.words('english') + list(string.punctuation)

def simplifiedLesk(word,sentence): #word->termine polisemico; sentence->contesto
	best_sense = most_frequent_sense(word) # il primo elencato in wordnet
	max_overlap = 0
	context = word_set(sentence)
	for sense in senses(word):
		signature = {i for i in word_tokenize(sense.definition() + ' '.join(sense.examples())) if i not in stop} # set di parole nella definizione e negli eventuali esempi di suel senso
		overlap = compute_overlap(signature, context) 
		#print('\t' + str(sense) + 'o:' + str(overlap) + " -> " + str(sense.definition()) + str(sense.examples())) # stampa i vari synsets con definizione ed esempi
		if (overlap > max_overlap):
			max_overlap = overlap
			best_sense = sense
	#print()
	print(str(best_sense) + 'o:' + str(max_overlap) + " -> " + str(best_sense.definition()) + str(best_sense.examples())) # stampa il best_sense con l'overlap, la definizione e gli eventuali esempi
	return best_sense

def most_frequent_sense(word):
	return wn.synsets(word)[0]

def word_set(sentence):
	return {i for i in word_tokenize(sentence) if i not in stop}

def senses(word):
	return wn.synsets(word)

def compute_overlap(signature, context): # ritorna il numero di parole in comune tra due set, ignora le function words e le altre parole nella stop list
	return len(signature.intersection(context))