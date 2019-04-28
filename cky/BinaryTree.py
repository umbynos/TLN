class BinaryTree:
	def __init__(self, value):
		self.value = value
		self.left_child = None
		self.right_child = None
		#leaf used to keep the value of the words
		self.leaf_child = None 

	def insert_left(self,binary_tree):
		self.left_child = binary_tree

	def insert_right(self,binary_tree):
		self.right_child = binary_tree

	def insert_leaf(self,value):
		self.leaf_child = value

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