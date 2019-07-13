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
    # files
    trump_file = "data/Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt"
    smartphone_file = "data/People-Arent-Upgrading-Smartphones-as-Quickly-and-That-Is-Bad-for-Apple.txt"
    moon_file = "data/The-Last-Man-on-the-Moon--Eugene-Cernan-gives-a-compelling-account.txt"
    # open file
    file = open(moon_file, "r", encoding="utf8")
    # list of stopwords and punctuation
    stop_words = stopwords.words('english') + list(string.punctuation)
    # save title in title_set: it contains a set of non stop words included in the title
    for i in range(4):
        file.readline()
    title = file.readline()
    # create a dictionary containing as keys the normalized words in title
    title_dict = words_to_vectors(title, stop_words, nasari_dict)
    # create a dictionary containing as keys the normalized words in sentences
    sentences_words_dict = []
    sentences = []
    for line in file:
        if line != "\n":
            for sentence in sent_tokenize(line):
                sentences_words_dict.append(words_to_vectors(sentence, stop_words, nasari_dict))
                sentences.append(sentence)
    # Relevance criteria: title method
    cohesions = []
    for sentence_dict in sentences_words_dict:
        cohesions.append(title_cohesion(title_dict, sentence_dict))


# assign nasari vectors to each words found
def words_to_vectors(sentence, stop_words, nasari_dict):
    dictionary = {}
    # normalize words (morpheme and lower case)
    lemmatizer = WordNetLemmatizer()
    # table: remove punctuation
    table = str.maketrans({key: None for key in string.punctuation})
    for word in sentence.split():
        word = word.translate(table)  # remove punctuation
        if word not in stop_words:
            dictionary[lemmatizer.lemmatize(word.lower())] = []
    # initialize title_dict values
    init_dict(dictionary, nasari_dict)
    # increase title_dict adding value from
    increase_dict(dictionary, nasari_dict)
    return dictionary


# get of dd-small-nasari-15.txt file
def nasari_to_dict(nasari):
    nasari_dict = {}
    for line in nasari:
        key = line.strip("\n").split(";")[1]
        synset = line.split(";")[2:]
        nasari_dict[key.lower()] = synset
    return nasari_dict


# initialize dict values
def init_dict(dict, nasari_dict):
    for key in dict:
        if key in nasari_dict:
            for value in nasari_dict[key]:
                dict[key].append(value)


# increase dict adding vectors of old values
def increase_dict(dict, nasari_dict):
    for key in dict:
        if key in nasari_dict:
            for value in nasari_dict[key]:
                # value is now a key
                if value.split("_")[0] in nasari_dict:
                    dict[key].extend(nasari_dict[value.split("_")[0]])


def title_cohesion(title_dict, sentence_dict):
    wo = 0
    for word_title in title_dict:
        for word_sentence in sentence_dict:
            wo += weigheted_overlap(title_dict[word_title],sentence_dict[word_sentence])
    return wo


def weigheted_overlap(vector1, vector2):
    overlap = []
    numerator = 0
    denominator = 0
    for definition1 in vector1:
        word1 = definition1.split("_")[0]
        value1 = float(definition1.split("_")[1])
        for definition2 in vector2:
            word2 = definition2.split("_")[0]
            value2 = float(definition2.split("_")[1])
            if word1 == word2:
                overlap.append([word1, value1, value2])
    for (word, value1, value2) in overlap:
        numerator += (value1+value2)**(-1)
    for i in range(1, len(overlap)):
        denominator += (2*i)**(-1)
    if denominator == 0:
        return 0
    else:
        return numerator / denominator


if __name__ == "__main__":
    main()