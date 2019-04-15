# Lesk Algorithm

from nltk.corpus import wordnet as wn

# word: termine polisemico
# sentence: contesto
def SimplifiedLesk(word,sentence):
  best_sense = most_frequent_sense(word) # il primo elencato in wordnet
  max_overlap = 0
  context = word_set(sentence) # si considerano solo parole con significato (articoli etc quindi no)
  for senses in word:
    signature = 