from nltk.corpus import wordnet as wn

def SimplifiedLesk(word,sentence): #word->termine polisemico; sentence->contesto
	best_sense = most_frequent_sense(word) # il primo elencato in wordnet
	max_overlap = 0
	context = word_set(sentence)
	for sense in senses(word):
		signature = #? set of words in the gloss and examples of sense
		overlap = compute_overlap(signature, context) #returns the number of words in common between two sets, ignoring function words or other words on a stop list
		if (overlap > max_overlap)
			max_overlap = overlap
			best_sense = sense
	return best_sense

def most_frequent_sense(word):
	wn.synsets(word)[0]

def word_set(sentence):
	set(sentence.split(" "))

def senses(word):
	wn.synsets(word)

def compute_overlap(signature, context):