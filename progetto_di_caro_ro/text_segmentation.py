# Text Segmentation with Text Tiling Method


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import progetto_di_caro_ro.similarity as sim
import string
import copy


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
    # each block contains 10% of the pseudosentences text
    k = int(0.1 * len(pseudosentences))  # SOLITAMENTE QUANTI ARGOMENTI AFFRONTA UN TESTO?
    # put pseudosentences in blocks of length k
    # block type: [strings]
    blocks = find_blocks(pseudosentences, k)
    # Lexical Score Determination
    dict_similarities = find_similarities(blocks)
    # Boundary Identification
    iteration_number = 3
    new_segmentation = find_new_boundaries(iteration_number, dict_similarities, blocks)
    print("###########################")
    print("## OLD SEGMENTS' LENGTH ##")
    print("###########################")
    for i, block in enumerate(blocks):
        print(str(i) + " " + str(len(block)))
    print("###########################")
    print("## NEW SEGMENTS' LENGTH ##")
    print("###########################")
    for i, block in enumerate(new_segmentation):
        print(str(i) + " " + str(len(block)))
    print("###########################")
    print("###### OLD SEGMENTS ######")
    print("###########################")
    for block in blocks:
        print(block)
    print("###########################")
    print("###### NEW SEGMENTS ######")
    print("###########################")
    for block in new_segmentation:
        print(block)


# divide input text into individual lexical units (list of words)
def extrapolate_file(file_to_open):
    file = open(file_to_open, "r", encoding="utf8")
    words = []
    for line in file:
        for word in word_tokenize(line):
            words.append(word.lower())
    file.close()
    return words


# remove stop words and punctuation + reduce to lemma
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
                # token:  no stopwords and punctuation + lemma
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
                if len(wups) > 0:
                    dict_similarities[(pseudo_sent_pos, pseudo_sent_pos+1)] = weight / len(wups)  # O SOLO IL PESO SENZA DIVIDERE???
                pseudo_sent_pos += 1
    return dict_similarities


def find_new_boundaries(iteration_number, dict_similarities, blocks):
    aux_blocks = copy.deepcopy(blocks)
    while iteration_number > 0:
        aux_blocks = copy.deepcopy(find_new_blocks(dict_similarities, aux_blocks))
        iteration_number -= 1
    return aux_blocks


def find_new_blocks(dict_similarities, blocks):
    new_blocks = []
    new_block = []
    pseudo_sent_pos = 0
    bad_pseudosent_pos = 1  # if the minimum is between the first couple, is moved the pseudosentence with index 1
    for b, block in enumerate(blocks):
        minimum = dict_similarities[(pseudo_sent_pos, pseudo_sent_pos+1)]
        for ps in range(len(block)-1):  # -1: if last one is considered it goes out of range
            actual_sim = dict_similarities[(pseudo_sent_pos, pseudo_sent_pos+1)]
            if actual_sim < minimum:
                minimum = actual_sim
                bad_pseudosent_pos = ps+1
            pseudo_sent_pos += 1
        for k in range(bad_pseudosent_pos):
            new_block.append(block[k])
        new_blocks.append(new_block)
        new_block = []
        remaining = bad_pseudosent_pos
        while remaining < len(block):
            new_block.append(block[remaining])
            remaining += 1
    if new_block:  # if new_block isn't empty
        new_blocks.append(new_block)
    return new_blocks


if __name__ == "__main__":
    main()
