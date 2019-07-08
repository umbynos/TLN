# Automatic Summarization with NASARI

from nltk.corpus import stopwords
from itertools import islice


# reads file starting from line 5 (title, then paragraphs)
def main():
    # per ogni file mi serve l'elenco delle parole senza stop words del titolo e di ogni paragrafo
    trump_file = "text_data_modified/Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt"
    # open file
    file = open(trump_file, "r", encoding="utf8")
    # save title
    for i in range(4):
        file.readline()
    title = file.readline()
    title_words = []
    for word in title.split():
        title_words.append(word)
    title_no_sw = remove_stop_words(title_words)
    # salvo i paragrafi
    for line in islice(file, 7, None):
        print(line)
    # poi sostituisco le parole con i vettori nasari
    # mi servono raggruppati per poter fare i confronti


# creates NASARI vectors
def file_to_vectors(file):
    return 1


# remove stop words
def remove_stop_words(tokenized_words):
    # Load stop words
    stop_words = stopwords.words('english')
    # Remove stop words
    no_stopwords = []
    for word in tokenized_words:
        if word not in stop_words:
            no_stopwords.append(word)
    return no_stopwords


if __name__ == "__main__":
    main()