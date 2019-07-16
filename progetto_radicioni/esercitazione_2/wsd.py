import lesk_algorithm as lesk
import re
from nltk.corpus import semcor
from nltk.tree import Tree
from nltk.corpus import wordnet as wn

path = "utils/sentences.txt" # percorso del file che contiene le sentence

def main():
	sentences_file = open(path,'r')
	for i,line in enumerate(sentences_file):
		if line != '\n' and not line.lstrip().startswith('#'): # ignora i commenti e gli a capo
			sentence = line.replace('- ', '').replace('*', '').replace('.', '').replace('\n','') # toglie i caratteri inutili dalla stringa
			word = re.search("(\*\*)(.*)(\*\*)", line).group(2) # cerca la stringa compresa tra gli **
			print("---------------------------------------------------------------------------------")
			print(sentence) # stampa la frase
			print(word) # stampa la parola da disambiguare
			print()
			best_sense = lesk.simplifiedLesk(word, sentence)
			print()
			for lemma in best_sense.lemma_names(): # stampa la frase con i sinonimi
				print(re.sub("(\*\*)(.*)(\*\*)", lemma, line)) # sostituisce la parola tra ** con tutti i suoi sinonimi
			print("---------------------------------------------------------------------------------")

	sentences_file.close()
	print("--------------------------------------SEMCOR--------------------------------------------------")

	semcor_sentences = (semcor.sents())[:50] # prende le prime 50 frasi da semcor
	semcor_tag_sentences = (semcor.tagged_sents(tag='both'))[:50] # prende le prime 50 frasi da semcor (con tag e semantica)
	equals = 0
	for i,s in enumerate(semcor_sentences):
		print("---------------------------------------------------------------------------------")
		sentence = ' '.join(s).lower() # compone la frase (prima era una lista)
		expected_sense=''
		for j,t_s in enumerate(semcor_tag_sentences[i]): # prende le parole per ogni frase annotata e cicla su queste ultime
			if type(semcor_tag_sentences[i][j][0]) is Tree and semcor_tag_sentences[i][j][0].label() == 'NN': # se è un nome
				expected_sense = semcor_tag_sentences[i][j].label().synset() # La label è del tipo "Lemma('resignation.n.03.resignation')"
				word = find_suitable_word(semcor_tag_sentences[i][j].leaves())
				break # esce dal ciclo non appena trova la prima parola
		print(sentence)
		print(word)		
		print(expected_sense)
		print()
		best_sense = lesk.simplifiedLesk(word, sentence)
		if best_sense == expected_sense:
			equals += 1
		print("---------------------------------------------------------------------------------")
	print('Accuracy: ' + str(equals/len(semcor_sentences)))

def find_suitable_word(words): # lista in input
	if len(words) > 1: # se non è una singola parola
		if wn.synsets(''.join(words).lower()) == []: # se le parole unite da un carattere vuoto non ritornano nulla
			return '_'.join(words).lower() # ritorna le parole separate da un _
		return ''.join(words).lower() # ritorna le parole separate da un carattere vuoto
	return ''.join(words).lower() # fa il lower e restituisce una stringa

if __name__== "__main__":
	main()