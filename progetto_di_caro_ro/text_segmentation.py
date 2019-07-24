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
    # Subdivide text into pseudosentences of a predefined size w
    w = 10
    pseudosentences = list_pseudosentences(w, words)
    # find k: number of sentences in each block
    # each block contains 10% of the pseudosentences text (not considering punctuation)
    k = int(0.1 * len(pseudosentences))  # SOLITAMENTE QUANTI ARGOMENTI AFFRONTA UN TESTO?
    # put pseudosentences in blocks of length k
    # block = [strings]
    blocks = find_blocks(pseudosentences, k)
    # Lexical Score Determination
    # dentro ad ogni blocco confronti le parole di pseudo frasi contigue
    dict_similarities = find_similarities(blocks)
    # Boundary Identification
    new_blocks = find_new_blocks(dict_similarities, blocks)
    print()


# divide input text into individual lexical units (list of words)
def extrapolate_file(file_to_open):
    file = open(file_to_open, "r", encoding="utf8")
    words = []
    for line in file:
        for word in word_tokenize(line):
            words.append(word.lower())
    file.close()
    return words


# LASCIA DELLA PUNTEGGIATURA: ' " (FORSE) ALTRO. LASCIARLA E QUANDO NON LO TROVI NON LO CONSIDERI O AGGIUNGERLE A MANO? (questi ci sono già  + ['\'', '\"'])
# remove stop words and punctuation + reduce to morpheme
# sw_punct: list containing english stop words and punctuation
def tokenize_words(words):
    tokens = []
    sw_punct = stopwords.words('english') + list(string.punctuation)
    lemmatizer = WordNetLemmatizer()
    for word in word_tokenize(words):
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
    if block:  # if block isn't empty
        blocks.append(block)
    return blocks


# compute wup similarity for every word in the first pseudo sentence with every word of the second
def find_similarities(blocks):
    dict_similarities = {}
    pseudo_sent_pos = 0
    for block in blocks:
        for i in range(len(block)):
            if i+1 < len(block):
                # token:  no stopwords and punctuation + morpheme
                tokens1 = tokenize_words(block[i])
                tokens2 = tokenize_words(block[i+1])
                wups = []
                for token1 in tokens1:
                    for token2 in tokens2:
                        wups.append(sim.wu_and_palmer(token1, token2))
                    # average
                weight = 0.0
                for wup in wups:
                    weight += wup
                dict_similarities[(pseudo_sent_pos, pseudo_sent_pos+1)] = weight / len(wups)  # O SOLO IL PESO SENZA DIVIDERE???
                pseudo_sent_pos += 1
    return dict_similarities


# NON C'è SIMMETRIA TRA GLI INDICI -> METTERE LE SIM IN UN DIZIONARIO: KEY: POS DELLE PSEUDO FRASI; VALORE: SIMILARITà
def find_new_blocks(similarities, blocks):
    new_blocks = []
    new_block = []
    for block_sims in similarities:
        minimum = block_sims[0]
        i = 0
        for j, similarity in enumerate(block_sims):
            if similarity < minimum:
                minimum = similarity
                i = j
        for k in range(i):
            new_block.append(blocks[i][k])
        new_blocks.append(new_block)
        new_block = []
    return new_blocks


if __name__ == "__main__":
    main()
