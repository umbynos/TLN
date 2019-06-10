# Node structure containing words and similarity misure
# NOTA: node_structure come nome non va bene: sono inseriti in un array, non sono collegati fra di loro!!!!!!!!!!!!!

class Node:
	def __init__(self, fst_word, snd_word, similarity):
		self.fst_word = fst_word
		self.snd_word = snd_word
		self.similarity = similarity
#		self.fst_word_sense = None
		#self.snd_word_sense = None

	def get_fst_word(self):
		return self.fst_word

	def get_snd_word(self):
		return self.snd_word

	def get_similarity(self):
		return self.similarity

#	def get_fst_word_sense(self):
#		return self.fst_word_sense
#
#	def get_snd_word_sense(self):
#		return self.snd_word_sense
#
	def set_fst_word(self, fst_word):
		self.fst_word = fst_word

	def set_snd_word(self, snd_word):
		self.snd_word = snd_word

	def set_similarity(self, similarity):
		self.similarity = similarity

#	def set_fst_word_sense(self, sense):
#		self.fst_word_sense = sense
#
#	def set_snd_word_sense(self, sense):
#		self.snd_word_sense = sense

	def print_node(self):
		print(self.fst_word, self.snd_word, self.similarity) 