# Text Segmentation with Text Tiling method


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import progetto_di_caro_ro.similarity as sim
import string


def main():
    # Tokenization
    # files
    trump_file = "data/Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt"
    smartphone_file = "data/People-Arent-Upgrading-Smartphones-as-Quickly-and-That-Is-Bad-for-Apple.txt"
    moon_file = "data/The-Last-Man-on-the-Moon--Eugene-Cernan-gives-a-compelling-account.txt"
    # divide input text into individual lexical units (list of words)
    words = extrapolate_file(trump_file)
    # skip stop words and punctuation + convert to lower-case + reduce to morpheme
    tokens = tokenize_words(words)
    # find w
    # DIMENSIONE DI W???
    # each segment contains 10% of the words (not considering punctuation)
    no_punct_words = []
    for word in words:
        if word not in list(string.punctuation):
            no_punct_words.append(word)
    w = int(0.1 * len(no_punct_words))
    # Subdivide text into pseudosentences of a predefined size w
    pseudosentences = list_pseudosentences(w, words)
    # scegliere il metodo per calcolare la coesione
    # applicare il metodo
    # risistemare le finestre


# divide input text into individual lexical units (list of words)
def extrapolate_file(file_to_open):
    file = open(file_to_open, "r", encoding="utf8")
    words = []
    for line in file:
        for word in word_tokenize(line):
            words.append(word)
    file.close()
    return words


# LASCIA DELLA PUNTEGGIATURA: ' " (FORSE) ALTRO. LASCIARLA E QUANDO NON LO TROVI NON LO CONSIDERI O AGGIUNGERLE A MANO?
# remove stop words and punctuation + convert to lower-case + reduce to morpheme
# sw_punct: list containing english stop words and punctuation
def tokenize_words(words):
    tokens = []
    sw_punct = stopwords.words('english') + list(string.punctuation)
    lemmatizer = WordNetLemmatizer()
    for word in words:
        if word not in sw_punct:
            tokens.append(lemmatizer.lemmatize(word.lower()))
    return tokens


# Subdivide text into pseudosentences of a predefined size w
def list_pseudosentences(w, words):
    pseudosentences = []
    pseudosentence = ""
    count = w
    for i in range(len(words)):
        if count > 0:
            pseudosentence += words[i] + " "
            if words[i] not in list(string.punctuation):
                count -= 1
        else:
            count = w
            pseudosentences.append(pseudosentence)
            pseudosentence = ""
    return pseudosentences


if __name__ == "__main__":
    main()
