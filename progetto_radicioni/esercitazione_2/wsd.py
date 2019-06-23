import lesk_algorithm as lesk
import re
from nltk.corpus import semcor

path = "utils/sentences.txt" # path of the file which contains the sentences

def main():
	sentences_file = open(path,'r')
	for i,line in enumerate(sentences_file):
		if line != '\n' and not line.lstrip().startswith('#'): # ignora i commenti e gli a capo
			sentence = line.replace('- ', '').replace('*', '').replace('.', '').replace('\n','') # toglie i caratteri inutili dalla stringa
			word = re.search("(\*\*)(.*)(\*\*)", line).group(2) # cerca la stringa compresa tra gli **
			print("---------------------------------------------------------------------------------")
			print(sentence)
			print(word)
			print()
			best_sense = lesk.simplifiedLesk(word, sentence)
			print("---------------------------------------------------------------------------------")
			for lemma in best_sense.lemma_names():
				print(re.sub("(\*\*)(.*)(\*\*)", lemma, line))

	sentences_file.close()
	print("-------------------------------SemCor-------------------------------")

	semcor_sentences = (semcor.sents())[:50]
	semcor_tag_sentences = (semcor.tagged_sents(tag='both'))[:50]
	for i,s in enumerate(semcor_sentences):
		sentence = ' '.join(s)
		for j,t_s in enumerate(semcor_tag_sentences[i]):
			if semcor_tag_sentences[i][j][0].label == 'NN': #è un nome (sostantivo?)
				label = semcor_tag_sentences[i][j].label()
				word = semcor_tag_sentences[i][j].leaves()
				break

		print("---------------------------------------------------------------------------------")
		print(sentence)
		print(word)
		print()
		best_sense = lesk.simplifiedLesk(word, sentence)
		print("---------------------------------------------------------------------------------")
		for lemma in best_sense.lemma_names():
			print(re.sub("(\*\*)(.*)(\*\*)", lemma, line))
		print(label)

# Per la word prendo la prima in semcor.tagged_sents(tag='both')[i][j][0].label() == 'NN' e mi salvo la semcor.tagged_sents(tag='both')[i][j].label() -> per confrontarla dopo.

if __name__== "__main__":
	main()