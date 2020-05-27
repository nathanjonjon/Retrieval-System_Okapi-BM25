import numpy as np
import pickle
import json
def buildMaps(invert):
	Bigram2DF = {}
	Doc2Bigrams = [[] for i in range(46972)]
	DocLens = [0 for i in range(46972)]
	line = invert.readline()
	while line:
		if line.count(' ') == 2:
			three_nums = (line[:-1]).split(' ')
			df = int(three_nums[2])
			bigram = (int(three_nums[0]), int(three_nums[1]))
			temp = []
			for i in range(df):
				line = invert.readline()
				two_nums = (line[:-1]).split(' ')
				temp.append((int(two_nums[0]), int(two_nums[1])))
				Doc2Bigrams[int(two_nums[0])].append((bigram, int(two_nums[1]))) # Doc2Bigrams is for relevance feedback
				DocLens[int(two_nums[0])] += int(two_nums[1]) # DocLen = num of bigrams
			Bigram2DF.setdefault(bigram, (temp, np.log(46972/df))    ) # Bigram2DF has tf and idf (沒改到
		line = invert.readline()
	return Bigram2DF, Doc2Bigrams, DocLens

def computeTF(count, d_len, avdlen):
	k = 1.5
	b = 0.4
	# return ((k+1) * count) / (k  + count)
	return ((k+1) * count) / (k * ((1-b)+(b*d_len/avdlen)) + count)


def computeWeight(query, DocLens, Bigram2DF, TopK): # query is a list of bigram tuple, ex: [((term_id1, term_id2), num1), ((term_id3, term_id4), num2), ... ]
	DocScores = [0 for i in range(46972)]
	avdlen = sum(DocLens) / 46972
	# print(query)
	for termNnum in query:
		Qterm = termNnum[0]
		Qtf =  computeTF(termNnum[1], len(query), avdlen)
		IDF = Bigram2DF[Qterm][1]
		QWeight = Qtf * IDF
		for docNtf in Bigram2DF[Qterm][0]:
			docID = docNtf[0]
			# print(docID)  # should be 10849
			tf = computeTF(docNtf[1], DocLens[docID], avdlen)
			DWeight = (tf * IDF)
			DocScores[docID] += (QWeight * DWeight)



	ScoreNDocIDList = ( sorted( [(x,i) for (i,x) in enumerate(DocScores)], reverse=True )[:TopK] )
	return ScoreNDocIDList

def make3Files(model_dir_path):
	invert_file_pathname = model_dir_path+'/inverted-file'
	invert = open(invert_file_pathname)
	Bigram2DF, Doc2Bigrams, DocLens = buildMaps(invert)

	with open("TestDictFile_new", "wb") as file:
		pickle.dump(Bigram2DF, file)
	with open('TestDoc2Bigrams_new', 'wb') as file2:
		pickle.dump(Doc2Bigrams, file2)
	with open('TestDocLens_new', 'wb') as file3:
		pickle.dump(DocLens, file3)
	file.close(); file2.close(); file3.close()

def buildDict(vocab_path):
	vocab = open(vocab_path)
	Voc2ID = {}
	ID2Voc = {}
	lines = vocab.readlines()
	current_id = 0
	for term in lines:
		if current_id == 0: current_id += 1; continue
		Voc2ID.setdefault(term.replace('\n',''), current_id)
		ID2Voc.setdefault(current_id, term.replace('\n',''))
		current_id += 1
	return Voc2ID, ID2Voc






