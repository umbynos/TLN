# Automatic Summarization with NASARI

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import string
import copy


# reads file starting from line 5 (title, then paragraphs)
def main():
    # read NASARI file
    nasari_file = open("dd-small-nasari-15.txt", "r", encoding="utf8")
    nasari_dict = nasari_to_dict(nasari_file)
    nasari_file.close()
    # adding recursivly istances in nasari_dict
    increased_nasari_dict = increase_nasari_dict(nasari_dict)
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
    # lemmatizzare le parole che vengono utilizzate come chiavi del dizionario
    # weighted_overlap: cerchiamo le parole e i suoi sinonimi (-> key e valore) del titolo nelle frasi e calcoliamo overlap
    # trovare un modo per sapere da quali frasi vengono le parole




# creates NASARI vectors
def word_to_vectors(word):
    # forse: se la parola è nei sinonimi di un vettore, allora ci associ tutti i sinonimi di quel vettore
    # nei vettori mettiamo i lemmi -> le parole
    return 1


def nasari_to_dict(nasari):
    nasari_dict = {}
    for line in nasari:
        key = line.strip("\n").split(";")[1]
        synset = line.split(";")[2:]
        nasari_dict[key.lower()] = synset
    return nasari_dict


def increase_nasari_dict(nasari_dict):
    nasari_dict_aux = copy.deepcopy(nasari_dict)
    for key in nasari_dict:
        for value in nasari_dict[key]:
            if value in nasari_dict:
                nasari_dict_aux[key].append(nasari_dict_aux[value])
    return nasari_dict_aux



if __name__ == "__main__":
    main()