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
    for line_number, line in enumerate(file):
        if line != "\n" and not line.startswith("#") and line_number != 4:
            lines.append(line)
            lines_no_stopwords.append(remove_stopwords(line))
    file.close()

    # divide sentences into blocks
    blocks = list(chunks(lines, 3))
    print(blocks)

    # rearrange sentences into blocks


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


def weighted_overlap(vector1, vector2):  # i valori nei vettori devono essere in ordine crescente
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
        return sqrt(numerator / denominator)
    return similarity  # between [0,1]


if __name__ == "__main__":
    main()
