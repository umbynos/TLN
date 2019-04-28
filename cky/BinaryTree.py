class BinaryTree:
	def __init__(self, value):
		self.value = value
		self.left_child = None
		self.right_child = None

	def insert_left(self,value):
		if self.left_child == None:
			self.left_child = BinaryTree(value)
		else:
			new_node = BinaryTree(value)
			new_node.left_child = self.left_child
			self.left_child = new_node

	def insert_right(self,value):
		if self.right_child == None:
			self.right_child = BinaryTree(value)
		else:
			new_node = BinaryTree(value)
			new_node.right_child = self.right_child
			self.right_child = new_node

	def dfs(self):
		print(self.value)
		if self.left_child:
			self.left_child.dfs()
		if self.right_child:
			self.right_child.dfs()
		