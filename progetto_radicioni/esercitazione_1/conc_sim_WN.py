import sys
from word_sim_structure import WordSim
from itertools import islice
from nltk.corpus import wordnet as wn
import math
import scipy

def main():
	# Saving the file in an array structure. Each element is a node_structure
	words_file = sys.argv[1] # The file is given by argument
	file = open(words_file,"r")
	words_array = []
	for line in islice(file, 1, None): # don't read the first line, start from 1: first line contains an introduction
		fst_word = line.split("\t")[0]
		snd_word = line.split("\t")[1]
		similarity = line.split("\t")[2]
		word_sim = WordSim(fst_word, snd_word, similarity)
		words_array.append(word_sim)
	file.close()
	# Depth of WordNet structure
	global depth_max
	depth_max = WN_DepthMax()
	# Computing similarities
	wu_and_palmer_sim = [] # List with Wu & Palmer Similarity for each entry of words_array
	shortest_path_sim = [] # List with Shortest Path Similarity for each entry of words_array
	leacock_chodorow_sim = [] # List with Leacock Chodorow Similarity for each entry of words_array
	for i in range(len(words_array)):
		word1 = words_array[i].get_fst_word()
		word2 = words_array[i].get_snd_word()
		print("words:",word1,word2)
		# Wu & Palmer Similarity
		wu_and_palmer_sim.append(float(wu_and_palmer(word1,word2)))
		print("wu_and_palmer nostro:", wu_and_palmer_sim[i])
		# Shortest Path Similarity
		shortest_path_sim.append(sht_path_sim(word1,word2))
		print("shortest_path_sim:", shortest_path_sim[i])
		# Leacock CHodorow Similarity
		leacock_chodorow_sim.append(leacock_chodorow(word1,word2))
		print("leacock_chodorow nostro:",leacock_chodorow_sim[i])
		print()
	# Correlation indexes
	sim = []
	for elem in words_array:
	 	sim.append(float(elem.get_similarity()))
	corr_pearson_WUP, p_value_pearson_WUP = scipy.stats.pearsonr(sim,wu_and_palmer_sim)
	print("Pearson, WUP: ", corr_pearson_WUP)
	corr_pearson_SP, p_value_pearson_SP = scipy.stats.pearsonr(sim,shortest_path_sim)
	print("Pearson, SP: ", corr_pearson_SP)
	corr_pearson_LC, p_value_pearson_LC = scipy.stats.pearsonr(sim,leacock_chodorow_sim)
	print("Pearson, LC: ", corr_pearson_LC)
	corr_spearman_WUP, p_value__spearman_WUP = scipy.stats.spearmanr(sim, wu_and_palmer_sim)
	print("Spearman, WUP: ", corr_spearman_WUP)
	corr_spearman_SP, p_value__spearman_SP = scipy.stats.spearmanr(sim, shortest_path_sim)
	print("Spearman, SP: ", corr_spearman_SP)
	corr_spearman_LC, p_value__spearman_LC = scipy.stats.spearmanr(sim, leacock_chodorow_sim)
	print("Spearman, LC: ", corr_spearman_LC)

# wu_and_palmer() takes two words and returns the Wu & Palmer Similarity considering the two synsets that give the maximum similarity
# If no synsets are found, the similarity is considered to be zero
def wu_and_palmer(word1, word2):
	synset1 = wn.synsets(word1)
	synset2 = wn.synsets(word2)
	cs = 0
	res1 = None
	res2 = None
	if(len(synset1)>0 and len(synset2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synset1:
			for s2 in synset2:	
				# LCS: Lowest Common Subsumer. It is the lower common ancestor between s1 and s2, id est the lowest common hypernym
				lcs = lowest_common_subsumer(s1, s2)
				if lcs: # not all synsets have a root in common
					new_cs = 2*(max_depth(lcs)+1) / ((max_depth(s1)+1) + (max_depth(s2)+1))
					# Get the longest path from the LCS to the root, with correction: add one because the calculations include both the start and end nodes
					if(new_cs > cs):
						cs = new_cs
						res1 = s1
						res2 = s2
		if res1 and res2: # not all synsets have a root in common
			print("wu_and_palmer WN: ", res1.wup_similarity(res2))
	return cs # QUALCHE RISULTATO è UN FILO DIVERSO (+-0.3). SCEGLIERE MEGLIO L'IPERONIMO COMUNE?


# max_depth(synset) returns the length of the longest hypernym path from this synset to the root
def max_depth(synset):
	hypernyms = synset.hypernyms()
	if not hypernyms:
		return 0
	else:
		return 1 + max(max_depth(h) for h in hypernyms)

# Get a list of lowest synset(s) that both synsets have as a hypernym
def lowest_common_subsumer(synset1, synset2):
	paths1 = hypernym_paths(synset1)
	paths2 = hypernym_paths(synset2)
	common_hypernym = None
	position = -1
	for path1 in paths1:
		for path2 in paths2:
			for i in range(len(path1)-1, -1, -1):
				for j in range(len(path2)-1, -1, -1):
					if path1[i]==path2[j] and (i>position or j>position):
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

# sht_path_sim(word1, word2) returns a similarity based on the shortest path length from word1 to word2 considering the two synsets that give the minimum path
# If no synsets are found, the similarity is considered to be zero
def sht_path_sim(word1, word2):
	synsets1 = wn.synsets(word1)
	synsets2 = wn.synsets(word2)
	sim = None
	sht_path = None
	if(len(synsets1)>0 and len(synsets2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synsets1:
			for s2 in synsets2:
				tmp_shortest_path = shortest_path(s1, s2)
				if (sht_path==None or tmp_shortest_path<sht_path) and tmp_shortest_path != -1:
					sht_path = tmp_shortest_path
					sim = 2*depth_max-sht_path
	if sim:
		return sim
	else:
		return 0

# shortest_path(synset1, synset2) returns the minum paths between two synsets
def shortest_path(synset1, synset2):
	paths1 = hypernym_paths(synset1)
	paths2 = hypernym_paths(synset2)
	best_len_path = None
	for path1 in paths1:
		for path2 in paths2:
			for i in range(len(path1)-1, -1, -1):
				for j in range(len(path2)-1, -1, -1):
					if path1[i]==path2[j]:
						# if a match is found, the number of step from the synsets to their common hypernym is computed
						len_path = (len(path1)-1)-i + (len(path2)-1)-j
						if best_len_path==None or len_path<best_len_path: # not best_len_path: first assignment, best_first_path is None
							best_len_path = len_path
	if best_len_path!=None:
		return best_len_path
	else:
		return -1

# leacock_chodorow() returns the Leacock Chodorow Similarity considering the two synsets that give the maximum similarity
# If no synsets are found, the similarity is considered to be zero
def leacock_chodorow(word1, word2):
	synsets1 = wn.synsets(word1)
	synsets2 = wn.synsets(word2)
	sim = 0
	found = False # the similarity is computed only if the parameters have at least one synset in common with the same POS
	res1 = None
	res2 = None
	if(len(synsets1)>0 and len(synsets2)>0): # some words in the file WordSim353.tab are not present in WordNet DataBase
		for s1 in synsets1:
			for s2 in synsets2:
				if(s1.pos()==s2.pos()):
					length = shortest_path(s1, s2)
					if length != -1:
						if(length == 0):
							new_sim = abs(math.log((length+1)/(2.0*depth_max+1)))
						else:
							new_sim =  abs(math.log((length+1)/(2.0*depth_max)))
						if new_sim>sim:
							sim = new_sim
							res1 = s1
							res2 = s2
							found = True
	if(found):
		print("leakock_chodorow WN: ", res1.lch_similarity(res2, simulate_root=False))
		return sim
	else:
		return 0

# WN_DepthMax() returns the maximum depth of WordNet's structure
def WN_DepthMax(): # TI SEMBRA RAGIONEVOLE???????
	max_hyp_path = 0
	max_all = 0
	for synset in wn.all_synsets():
		for hyp_path in hypernym_paths(synset):
			if(len(hyp_path) > max_hyp_path):
				max_hyp_path = len(hyp_path)
		if(max_hyp_path > max_all):
			max_all = max_hyp_path
	return max_all

if __name__== "__main__":
	main()