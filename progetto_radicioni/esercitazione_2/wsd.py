import lesk_algorithm as lesk

path = "utils/sentences.txt" # path of the file which contains the sentences

def main():
	sentences_file = open(path,'r')
	sentences_list = sentences_file.readlines()
	sentences_list = [x for x in sentences_list if x != '\n'] #remove '\n' from the list
	#sentences_list = [re.compile(r"\n").sub("", m) for m in sentences_list] #finire regex per filtrare la lista e poi **
	print(sentences_list)
	#lesk.simplifiedLesk("Arms", "Arms bend at the elbow.")
	sentences_file.close()

if __name__== "__main__":
	main()