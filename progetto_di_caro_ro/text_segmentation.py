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
    # Subdivide text into pseudosentences of a predefined size w
    w = 20
    pseudosentences = list_pseudosentences(w, words)
    # find k: number of sentences in each block
    # each block contains 10% of the words text (not considering punctuation)
    k = int(0.1 * len(pseudosentences))  # SOLITAMENTE QUANTI ARGOMENTI AFFRONTA UN TESTO?
    # put pseudosentences in blocks of length k
    blocks = find_blocks(pseudosentences, k)
    # Lexical Score Determination
    # dentro ad ogni blocco confronti le parole in pseudo frasi contigue
    weights = find_weights(pseudosentences)
    # Boundary Identification

# divide input text into individual lexical units (list of words)
def extrapolate_file(file_to_open):
    file = open(file_to_open, "r", encoding="utf8")
    words = []
    for line in file:
        for word in word_tokenize(line):
            words.append(word.lower())
    file.close()
    return words


# LASCIA DELLA PUNTEGGIATURA: ' " (FORSE) ALTRO. LASCIARLA E QUANDO NON LO TROVI NON LO CONSIDERI O AGGIUNGERLE A MANO?
# remove stop words and punctuation + reduce to morpheme
# sw_punct: list containing english stop words and punctuation
def tokenize_words(words):
    tokens = []
    sw_punct = stopwords.words('english') + list(string.punctuation)
    lemmatizer = WordNetLemmatizer()
    for word in words:
        if word not in sw_punct:
            tokens.append(lemmatizer.lemmatize(word))
    return tokens


# Subdivide text into pseudosentences of a predefined size w
def list_pseudosentences(w, words):
    pseudosentences = []
    pseudosentence = ""
    count = w
    for i in range(len(words)):
        if count > 0:
            if words[i] not in list(string.punctuation):
                pseudosentence += words[i] + " "
                count -= 1
        else:
            count = w
            pseudosentences.append(pseudosentence)
            pseudosentence = "" + words[i] + " "
    pseudosentences.append(pseudosentence)
    return pseudosentences


# put pseudosentences in blocks of length k
def find_blocks(pseudosentences, k):
    count = k
    blocks = []
    block = []
    for pseudosent in pseudosentences:
        if count > 0:
            block.append(pseudosent)
            count -= 1
        else:
            count = k
            blocks.append(block)
            block = []
    return blocks


def find_weights(pseudosentences):
    weights = []
    # per ogni pseudo frase
    for pseudosent in pseudosentences:
        # per ogni parola
        words = word_tokenize(pseudosent)
        wups = []
        for i, word1 in enumerate(words):
            if word1 not in list(string.punctuation):
                # calcolo wup con ogni altra parola in pseudo frase
                for j, word2 in enumerate(words):
                    if i != j and word2 not in list(string.punctuation):
                        wups.append(sim.wu_and_palmer(word1, word2))
                # faccio la media
                weight = 0.0
                for wup in wups:
                    weight += wup
                weights.append(weight / len(wups))
    return weights


if __name__ == "__main__":
    main()
