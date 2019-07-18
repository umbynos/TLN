# Text Segmentation with Text Tiling method


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
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
    print(words)
    print(tokens)
    # decidere in quante parti suddividere il testo
    # suddividerlo
    # scegliere il metodo per calcolare la coesione
    # applicare il metodo
    # risistemare le finestre
    return 1


# divide input text into individual lexical units (list of words)
def extrapolate_file(file_to_open):
    file = open(file_to_open, "r", encoding="utf8")
    words = []
    for line in file:
        for word in word_tokenize(line):
            words.append(word)
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


if __name__ == "__main__":
    main()
