import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from math import sqrt


def main():

    # read NASARI file
    relative_file_path = "../progetto_radicioni/esercitazione_3/"
    nasari_file = open(relative_file_path + "dd-small-nasari-15.txt", "r", encoding="utf8")
    nasari_dict = nasari_to_dict(nasari_file)
    nasari_file.close()

    # read articles
    trump_file = "data/Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt"
    smartphone_file = "data/People-Arent-Upgrading-Smartphones-as-Quickly-and-That-Is-Bad-for-Apple.txt"
    moon_file = "data/The-Last-Man-on-the-Moon--Eugene-Cernan-gives-a-compelling-account.txt"
    file = open(relative_file_path + moon_file, "r", encoding="utf8")

    # create data structures
    lines = []
    lines_no_stopwords = []
    i = 0
    for line_number, line in enumerate(file):
        if line != "\n" and not line.startswith("#") and line_number != 4:
            #  contains a list of sentences from the articles
            lines.append((i, line.strip("\n")))
            #  contains a list of sets of the words taken from the sentences (w/o the stopwords)
            lines_no_stopwords.append(remove_stopwords(line))
            i += 1
    file.close()

    # divide sentences into blocks with max 3 elem
    blocks = list(chunks(lines, 3))

    # print the division of the paragraphs
    print_blocks(blocks)

    # compute similarity between sentences in a block
    wo_all = {}
    for b in blocks:
        if len(b) > 1: #  the block must contain at least 2 elems, to compute similarity
            for index_1, index_2 in zip(b[:-1],b[1:]):
                wo_partial = 0
                i_1 = index_1[0]
                i_2 = index_2[0]
                for word1 in lines_no_stopwords[i_1]:
                    v1 = search_in_dict(word1, nasari_dict)
                    for word2 in lines_no_stopwords[i_2]:
                        v2 = search_in_dict(word2, nasari_dict)
                        if v1 and v2: #  se v1 e v2 non sono vuoti
                            wo_partial += weighted_overlap(v1,v2)
                wo_all[(i_1, i_2)] = round(wo_partial, 3)
    print(wo_all)

    # rearrange sentences into blocks

    new_blocks = [[]]
    i1_min = i2_min = 0
    for i, block in enumerate(blocks):
        min = None
        for index_1, index_2 in zip(block[:-1], block[1:]):
            i_1 = index_1[0]
            i_2 = index_2[0]
            wo = wo_all[(i_1, i_2)]
            if min == None or wo < min:
                min = wo
                i1_min = i_1
                i2_min = i_2
        new_block1 = [old_tuple for old_tuple in block if old_tuple[0] <= i1_min]
        new_blocks[i].extend(new_block1)
        new_block2 = [old_tuple for old_tuple in block if old_tuple[0] >= i2_min]
        new_blocks.append(new_block2)

    print_blocks(new_blocks)


def nasari_to_dict(nasari_file):
    nasari_dict = {}
    for line in nasari_file:
        key = line.strip("\n").split(";")[1]
        synset = line.strip("\n").split(";")[2:]
        synset.reverse()
        nasari_dict[key.lower()] = synset
    return nasari_dict


def remove_stopwords(sentence):
    stop_words = stopwords.words('english') + list(string.punctuation + '–' + '“' + '’' + '”')
    return {word.lower() for word in word_tokenize(sentence) if word not in stop_words}


def chunks(l, n):
    # Yield successive n-sized chunks from l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def weighted_overlap(vector1, vector2):
    overlap = []
    numerator = 0
    denominator = 0
    for index1, s1 in enumerate(vector1):
        word1 = s1.split("_")[0]
        for index2, s2 in enumerate(vector2):
            word2 = s2.split("_")[0]
            if word1 == word2:
                overlap.append([word1, index1, index2])
    for (word, value1, value2) in overlap:
        numerator += (index1+index2)**(-1)
    for i in range(1, len(overlap)):
        denominator += (2*i)**(-1)
    if denominator == 0:
        return 0
    else:
        return sqrt(numerator / denominator) # between [0,1]


def search_in_dict(w, nasari_d):
    if w in nasari_d:
        return nasari_d[w]
    else:
        return []

def print_blocks(blocks):
    for block in blocks:
        for sent in block:
            print(sent[0], end=" ")
        print("|", end=" ")
    print("")

if __name__ == "__main__":
    main()
