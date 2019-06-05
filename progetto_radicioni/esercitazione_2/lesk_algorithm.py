from nltk.corpus import wordnet as wn

def SimplifiedLesk(word,sentence): #word->termine polisemico; sentence->contesto
	best_sense = most_frequent_sense(word) # il primo elencato in wordnet
	max_overlap = 0
	context = word_set(sentence) # si considerano solo parole con significato (articoli etc quindi no)
	for sense in senses(word): #? da dove viene senses? sarà un array
		signature = #set of words in the gloss and examples of sense
		overlap = compute_overlap(signature, context) #returns the number of words in common between two sets, ignoring function words or other words on a stop list
		if (overlap > max_overlap)
			max_overlap = overlap
			best_sense = sense
	return best_sense

def most_frequent_sense(word):

def word_set(sentence): #ritorna il srt di parole nella frase

def senses(word):

def compute_overlap(signature, context):