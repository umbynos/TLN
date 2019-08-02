from nltk.corpus import wordnet as wn


# takes two words and returns the Wu & Palmer Similarity considering the two synsets that give the maximum similarity
# If no synsets are found, the similarity is considered to be zero
def wu_and_palmer(word1, word2):
    synset1 = wn.synsets(word1)
    synset2 = wn.synsets(word2)
    cs = 0
    res1 = None
    res2 = None
    if len(synset1)>0 and len(synset2)>0: # some words in the file WordSim353.tab are not present in WordNet DataBase
        for s1 in synset1:
            for s2 in synset2:
                # LCS: Lowest Common Subsumer
                lcs = lowest_common_subsumer(s1, s2)
                if lcs:  # not all synsets have a root in common
                    new_cs = 2*(max_depth(lcs)+1) / ((max_depth(s1)+1) + (max_depth(s2)+1))
                    # Get the longest path from the LCS to the root
                    # Add one because the calculations include both the start and end nodes
                    if new_cs > cs:
                        cs = new_cs
                        res1 = s1
                        res2 = s2
        # if res1 and res2:  # not all synsets have a root in common
        #    print("wu_and_palmer WN: ", res1.wup_similarity(res2))
    return cs


# max_depth(synset) returns the length of the longest hypernym path from this synset to the root
def max_depth(synset):
    hypernyms = synset.hypernyms()
    if not hypernyms:
        return 0
    else:
        return 1 + max(max_depth(h) for h in hypernyms)


# returns the lower common ancestor between synset1 and synset2, id est the lowest common hypernym
def lowest_common_subsumer(synset1, synset2):
    paths1 = hypernym_paths(synset1)
    paths2 = hypernym_paths(synset2)
    common_hypernym = None
    position = -1
    for path1 in paths1:
        for path2 in paths2:
            for i in range(len(path1)-1, -1, -1):
                for j in range(len(path2)-1, -1, -1):
                    if path1[i] == path2[j] and (i > position or j > position):
                        common_hypernym = path1[i]
                        position = max(i, j)
    return common_hypernym


# hypernym_paths(synset) returns paths list: a list of lists, each list gives the node sequence from a root to synset
def hypernym_paths(synset):
    paths = []
    hypernyms = synset.hypernyms()
    if len(hypernyms) == 0:
        paths = [[synset]]
    for hypernym in hypernyms:
        for ancestor_list in hypernym.hypernym_paths():
            ancestor_list.append(synset)
            paths.append(ancestor_list)
    return paths
