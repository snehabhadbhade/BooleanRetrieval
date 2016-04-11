import sys
import os
import xml.etree.ElementTree as ET
import nltk
from nltk.stem.snowball import SnowballStemmer
import string
import collections
import json
from operator import itemgetter
import utils

dir_path = sys.argv[1]
dirs = os.listdir(dir_path)
stemmer = SnowballStemmer("english")

word_dist = collections.OrderedDict()
index_list = []
doc_info = {}

doc_no = 0
for file in dirs:
	final_tokens = []
	file_path = dir_path+"/"+file
	tree = ET.parse(file_path)
	root = tree.getroot()
	doc_no = doc_no + 1
	for child in root:
		if child.tag != 'DOCNO':
			text = child.text
			tokens = nltk.word_tokenize(text)
			tokens = [stemmer.stem(i) for i in tokens]
			tokens = [i for i in tokens if i not in string.punctuation]
			for token in tokens:
				final_tokens.append(token)
		else:
			doc_num = child.text.strip('\n')
	doc_size = len(final_tokens)	
	doc_id = "D" + str(doc_no)		
	for i in range(len(final_tokens)):
		pos = i+1
		word = final_tokens[i]
		#doc_id = "D" + str(doc_no)
		index_found = 0
		for index in range(len(index_list)):
			if index_list[index][0]==word:
				item = index_list[index][1]
				item.append([str(doc_id), pos])
				index_list[index][1] = item
				index_found = 1
				break
		if index_found == 0:
			index_list.append([word,[[str(doc_id),pos]]])
	doc_info[doc_id] = (doc_num, doc_size)
	
index_list.sort(key=itemgetter(0,1))
with open('indexA.json', 'w') as outfile:
    json.dump(index_list, outfile)

with open('docinfoA.json', 'w') as outfile:
    json.dump(doc_info, outfile)

for item in index_list:
	word_dist[str(item[0])] = len(item[1])

index_size = len(index_list)
utils.print_statistics(doc_no, word_dist, index_size)
