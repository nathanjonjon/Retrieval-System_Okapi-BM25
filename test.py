import xml.dom.minidom as minidom
import numpy as np
import pickle
import json
from utils import computeWeight, computeTF, buildMaps, make3Files, buildDict
import sys

opts = sys.argv
relevance_feedback = 0
if '-r' in opts:
	relevance_feedback = 1
query_file_path = opts[2+relevance_feedback]
ranked_list_path = opts[4+relevance_feedback]
model_dir_path = opts[6+relevance_feedback]
docs_dir_path = opts[8+relevance_feedback]

def getNodeText(node):
	nodelist = node.childNodes
	result = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			result.append(node.data)
	return ''.join(result)



Voc2ID, ID2Voc = buildDict(model_dir_path+"/vocab.all")


MakeNewMaps = 1 # make sure the switch is on before submitting
if MakeNewMaps == 1:
	invert = open(model_dir_path+"/inverted-file")
	Bigram2DF, Doc2Bigrams, DocLens = buildMaps(invert)
	invert.close()

all_files = open(model_dir_path+'/file-list')



ID2DocName = {}
ID = 0
for line in all_files:
	ID2DocName.setdefault(ID,line[:-1])
	ID += 1
	
all_files.close()

output = open(ranked_list_path, "w")
output.write("query_id,retrieved_docs\n")
doc = minidom.parse(query_file_path)
topics = doc.getElementsByTagName("topic")
for item in topics:
	qnum = getNodeText(item.getElementsByTagName("number")[0])
	qtitle = getNodeText(item.getElementsByTagName("title")[0])
	qkeyword = getNodeText(item.getElementsByTagName("concepts")[0])
	qquestion = getNodeText(item.getElementsByTagName("question")[0])
	query_string = qtitle+qkeyword+qkeyword; query_string = query_string.replace('\n', ''); query_string = query_string.replace(' ', ''); query_string = query_string.replace('。', ''); query_string = query_string.replace('，', ''); query_string = query_string.replace('、', '')
	n = 2

	QList = [query_string[i:i+n] for i in range(0, len(query_string), n)] + [query_string[i:i+n] for i in range(1, len(query_string), n)]


	QTermIDList = []


	for item in QList:
		if len(item) == 1:
			QList.remove(item)
			continue
		# print(item)
		count = query_string.count(item, 0, len(query_string)-1)
		Bigram = (int(Voc2ID[item[0]]), int(Voc2ID[item[1]]))
		if Bigram in Bigram2DF:
			QTermIDList.append((Bigram, count))
	for char in set(query_string):
		Bigram = (int(Voc2ID[char]), -1)
		if Bigram in Bigram2DF:
			# print(item[0]+item[1], Bigram, Bigram2DF[Bigram])
			QTermIDList.append((Bigram, query_string.count(char)))
	
	# print(QTermIDList)

	ScoreNDocIDList = computeWeight(QTermIDList,DocLens, Bigram2DF, 100)

	# relevance feedback
	if relevance_feedback == 1:
		rand = np.random.randint(10)
		DocID = (ScoreNDocIDList[rand])[1]
		QTermIDList = QTermIDList + QTermIDList + Doc2Bigrams[DocID]
		ScoreNDocIDList = computeWeight(QTermIDList,DocLens, Bigram2DF, 100)
	
	qnum = qnum[-3:]
	# print("query number:",qnum)

	line = qnum + ','
	for i in range(len(ScoreNDocIDList)):
		FineDocName = (ID2DocName[(ScoreNDocIDList[i])[1]]).split('/')[3].lower()
		if i == len(ScoreNDocIDList)-1:
			line = line + FineDocName + '\n'
			break
		line = line + FineDocName + ' ' # + ' ================= ' + ans_docs[i] + '\n'
	# print(line)
	output.write(line)



	# break # only try one query





	

	































# query = [((3, 6850), 1)]