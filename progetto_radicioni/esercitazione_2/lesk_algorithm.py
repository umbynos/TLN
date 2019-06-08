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
		signature = {i for i in word_tokenize(sense.definition() + ' '.join(sense.examples())) if i not in stop}#? set of words in the gloss and examples of sense
		overlap = compute_overlap(signature, context) #returns the number of words in common between two sets, ignoring function words or other words on a stop list
		print(str(sense) + 'o:' + str(overlap) + " -> " + str(sense.definition()) + str(sense.examples()))
		if (overlap > max_overlap):
			max_overlap = overlap
			best_sense = sense
	print()
	print(str(best_sense) + 'o:' + str(max_overlap) + " -> " + str(best_sense.definition()) + str(best_sense.examples()))
	return best_sense

def most_frequent_sense(word):
	return wn.synsets(word)[0] #verificare che la prima sia la più frequente

def word_set(sentence):
	return {i for i in word_tokenize(sentence) if i not in stop}

def senses(word):
	#print(wn.synsets(word))
	return wn.synsets(word)

def compute_overlap(signature, context):
	return len(signature.intersection(context))