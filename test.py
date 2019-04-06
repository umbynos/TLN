from nltk import load_parser
import sys
cp = load_parser(sys.argv[1])
sen = sys.argv[2]
tokens = sen.split()
for tree in cp.parse(tokens):
	print(tree.label()['SEM'])