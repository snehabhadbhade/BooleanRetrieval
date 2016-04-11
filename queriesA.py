import json
import sys
import nltk
from nltk.stem.snowball import SnowballStemmer
import re
from collections import defaultdict
from operator import itemgetter
import utils

query_file = sys.argv[1]
stemmer = SnowballStemmer("english")

with open('indexA.json', 'r') as infile:
    index_data = json.load(infile)

with open('docinfoA.json', 'r') as infile:
    doc_info = json.load(infile)

with open(query_file, 'r') as f:
	queries = f.readlines()

#pattern = '\".+?\"|\s+'
pattern = '\".+?\"|\w+'

for query in queries:
	print query
	flag_AND = 0
	final_list = []
	merged_list = []
	retrieved_docs = []
	score = defaultdict(int)
	query = query.rstrip('\n')
	
	for token in re.findall(pattern, query):
		merged_list = []	
		token = token.strip()
		if not token:
			continue	
		if token == 'AND':
			flag_AND = 1
			continue
		if re.match('\".+?\"',token):
			phrase_list = []
			token = token.strip('"')
			token = token.lower()
			phrase_tokens = token.split()
			i=0
			for phrase_token in phrase_tokens:
				doc_list = []
				temp_list = []
				phrase_token = stemmer.stem(phrase_token)
				for item in index_data:
					if item[0] == phrase_token:
						doc_list = item[1]
				
				if phrase_list:
					for doc,pos in doc_list:
						val = [doc,pos-1]
						if val in phrase_list:
							temp_list.append(val)
					phrase_list = temp_list
				else:
					phrase_list = doc_list
			temp_list = [val[0] for val in phrase_list]
			for doc in temp_list:
				score[doc]+=2
			if not final_list:
                                final_list = temp_list
                                continue
                        else:
                                if flag_AND == 0:
                                        merged_list = final_list
                                        for val in temp_list:
                                                if val not in merged_list:
                                                        merged_list.append(val)
                                else:
                                        merged_list = [val for val in temp_list if val in final_list]
							
		else:
			token = token.lower()
			token = stemmer.stem(token)
			doc_list = []
			for item in index_data:
				if item[0] == token:
					doc_list = item[1]
					break
			temp_list = [val[0] for val in doc_list]
			for doc in temp_list:
				score[doc]+=1
			#finding union and intersection
			if not final_list:
				final_list = temp_list			
				continue
			else:
				if flag_AND == 0:
					merged_list = final_list
					for val in temp_list:
						if val not in merged_list:
							merged_list.append(val)
				else:
					 merged_list = [val for val in temp_list if val in final_list] 

		
		final_list = merged_list
	for doc_id in final_list:
		doc_num, doc_size = doc_info[doc_id]
		if (doc_num,score[doc_id],doc_size) not in retrieved_docs:
			retrieved_docs.append((doc_num,score[doc_id],doc_size))
	retrieved_docs.sort(key=lambda x:(-x[1], x[2]))
	document_list = [val[0] for val in retrieved_docs]
	utils.print_documents(document_list)

		
 


