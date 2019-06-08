import lesk_algorithm as lesk
import re

path = "utils/sentences.txt" # path of the file which contains the sentences

def main():
	sentences_list=[]
	word_list=[]
	sentences_file = open(path,'r')
	for i,line in enumerate(sentences_file):
		if line != '\n' and not line.lstrip().startswith('#'): # ignora i commenti e gli a capo
			word_list.append(re.search("(\*\*)(.*)(\*\*)", line).group(2)) # cerca la stringa compresa tra gli **
			sentences_list.append(line.replace('- ', '').replace('*', '').replace('.', '').replace('\n','')) # toglie i caratteri inutili dalla stringa
	sentences_file.close()

	for i,sentence in enumerate(sentences_list):
		print("---------------------------------------------------------------------------------")

		print(sentences_list[i])
		print(word_list[i])
		print()
		lesk.simplifiedLesk(word_list[i], sentences_list[i])
		print("---------------------------------------------------------------------------------")

if __name__== "__main__":
	main()