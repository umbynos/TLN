class BinaryTree:
	def __init__(self, value):
		self.value = value
		self.left_child = None
		self.right_child = None
		#leaf used to keep the value of the words
		self.leaf_child = None  #se lo mettiamo nel left child è inutile (?)
	
	def get_value(self):
		return self.value

	def insert_left(self,binary_tree):
		self.left_child = binary_tree

	def get_left_child(self):
		l_c = self.left_child
		self.left_child = None
		return l_c

	def insert_right(self,binary_tree):
		self.right_child = binary_tree

	def get_right_child(self):
		r_c = self.right_child
		self.right_child = None
		return r_c

	def insert_leaf(self,value):
		self.leaf_child = value

	def search_left(self, value_to_search):
		if self.left_child.get_value() != value_to_search:
			return self.left_child.search_left(value_to_search)
		return self.get_left_child()

	def dfs(self):
		print(self.value)
		if self.left_child:
			self.left_child.dfs()
		if self.right_child:
			self.right_child.dfs()

	def print_leaves(self):
		if self.leaf_child:
			print(self.leaf_child, end=' ') #used to print oneline
		if self.left_child:
			self.left_child.print_leaves()
		if self.right_child:
			self.right_child.print_leaves()