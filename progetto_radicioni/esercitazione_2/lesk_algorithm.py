from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import word_tokenize
import string

stop = stopwords.words('english') + list(string.punctuation)

def simplifiedLesk(word,sentence): #word->termine polisemico; sentence->contesto
	best_sense = most_frequent_sense(word) # il primo elencato in wordnet
	max_overlap = 0
	context = word_set(sentence)
	print(context)
	for sense in senses(word):
		signature = {i for i in word_tokenize(sense.definition() + ' '.join(sense.examples())) if i not in stop}#? set of words in the gloss and examples of sense
		print(signature)
		overlap = compute_overlap(signature, context) #returns the number of words in common between two sets, ignoring function words or other words on a stop list
		print(overlap)
		if (overlap > max_overlap):
			max_overlap = overlap
			best_sense = sense
	print(best_sense)
	return best_sense

def most_frequent_sense(word):
	return wn.synsets(word)[0]

def word_set(sentence):
	return {i for i in word_tokenize(sentence) if i not in stop}

def senses(word):
	print(wn.synsets(word))
	return wn.synsets(word)

def compute_overlap(signature, context):
	return len(signature.intersection(context))