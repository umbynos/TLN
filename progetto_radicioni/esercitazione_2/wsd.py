import lesk_algorithm as lesk
import re

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

if __name__== "__main__":
	main()