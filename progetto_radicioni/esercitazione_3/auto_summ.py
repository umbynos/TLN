# Automatic Summarization with NASARI

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import string


# reads file starting from line 5 (title, then paragraphs)
def main():
    # files
    trump_file = "data/Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt"
    smartphone_file = "data/People-Arent-Upgrading-Smartphones-as-Quickly-and-That-Is-Bad-for-Apple.txt"
    moon_file = "data/The-Last-Man-on-the-Moon--Eugene-Cernan-gives-a-compelling-account.txt"
    # open file
    file = open(trump_file, "r", encoding="utf8")
    # list of stopwords and punctuation
    stop_words = stopwords.words('english') + list(string.punctuation)
    # save title in title_set: it contains a set of non stop words included in the title
    for i in range(4):
        file.readline()
    title = file.readline()
    title_set = {word for word in title.split() if word not in stop_words}
    # save sentences: list of sets. Each set contains non stop words included in the sentence
    sentences_words = []
    for line in file:
        if line != "\n":
            for sentence in sent_tokenize(line):
                sentences_words.append({word for word in sentence.split() if word not in stop_words})
    # poi sostituisco le parole con i vettori nasari
    sentences_vectors = []
    vectors_set = {}
    for sentence in sentences_words:
        for word in sentence:
            vectors_set.add(word_to_vectors(word))
        sentences_vectors.append(vectors_set)
    # mi servono raggruppati per poter fare i confronti


# creates NASARI vectors
def word_to_vectors(word):
    # forse: se la parola è nei sinonimi di un vettore, allora ci associ tutti i sinonimi di quel vettore
    return 1


def find_bn_id(word):
    return 1


if __name__ == "__main__":
    main()