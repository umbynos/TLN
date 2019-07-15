# Structure containing words and similarity misure

class WordSim:
	def __init__(self, fst_word, snd_word, similarity):
		self.fst_word = fst_word
		self.snd_word = snd_word
		self.similarity = similarity

	def get_fst_word(self):
		return self.fst_word

	def get_snd_word(self):
		return self.snd_word

	def get_similarity(self):
		return self.similarity

	def set_fst_word(self, fst_word):
		self.fst_word = fst_word

	def set_snd_word(self, snd_word):
		self.snd_word = snd_word

	def set_similarity(self, similarity):
		self.similarity = similarity 