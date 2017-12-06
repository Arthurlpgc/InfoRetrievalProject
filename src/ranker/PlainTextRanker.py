import json
import numpy
import re
import csv
import math

class PlainTextRanker():
    def __init__(self, indexPath):
        self.index = json.load(open(indexPath))
        #build a vocabulary from each word that appears in index
        self.vocabulary = {}
        self.vocabularyReverse = []
        self.vocabularyIndex = 0
        for key in self.index:
            if('.title' in key):
                if(key[:-6] not in self.vocabulary):
                    self.vocabulary[key[:-6]] = self.vocabularyIndex
                    self.vocabularyReverse.append(key[:-6])
                    self.vocabularyIndex = self.vocabularyIndex + 1
            elif('.statement' in key):
                if(key[:-10] not in self.vocabulary):
                    self.vocabulary[key[:-10]] = self.vocabularyIndex
                    self.vocabularyReverse.append(key[:-10])
                    self.vocabularyIndex = self.vocabularyIndex + 1
        #defines weights for each attribute in the query
        self.vocabularySize = len(self.vocabulary)
        #creates the vector space representation for each document in index database
        self.vectors = []
        self.numberDocs = 0
        with open('indexes/name.csv') as documents:
            for row in csv.reader(documents):
                for name in row:
                    self.vectors.append(numpy.zeros(self.vocabularySize))
                    document = json.load(open('retrieved/objects/{}.json'.format(name)))
                    title = re.sub("[^\w]", " ",  document['title']).split()
                    title=list(map(lambda x:x.lower(),title))
                    statement = re.sub("[^\w]", " ",  document['statement']).split()
                    statement=list(map(lambda x:x.lower(),statement))
                    titleLen = len(title)
                    statementLen = len(statement)
                    for word in title:
                        self.vectors[self.numberDocs][self.vocabulary[word]] += 1/(titleLen+statementLen)
                    for word in statement:
                        self.vectors[self.numberDocs][self.vocabulary[word]] += 1/(titleLen+statementLen)
                    self.numberDocs += 1
        #calculates the IDF foreach term in the vocabulary
        self.idf = {}
        for key in self.vocabulary:
            docs = self.index.get(key+'.title', []) + self.index.get(key+'.statement', [])
            self.idf[key] = 1 + math.log(self.numberDocs/len(docs))

    def getRank(self, query):
        query = [word for word in query.lower().split(' ')]
        #gets the list of relevant documents for this query
        relevantDocs = []
        for word in query:
            if((word+'.title') in self.index):
                relevantDocs += self.index[(word+'.title')]
            if((word+'.statement') in self.index):
                relevantDocs += self.index[(word+'.statement')]
    
        relevantDocs = list(set(relevantDocs))
        #creates the vector space for this query
        return self.rankDocumentAtTime(relevantDocs, query)

    def rankDocumentAtTime(self, relevantDocs, query):
        queryVector = numpy.zeros(self.vocabularySize)
        queryLen = len(query)
        for word in query:
            if(word in self.vocabulary):
                queryVector[self.vocabulary[word]] += 1/queryLen
        ranks = self.tfIdfRank(relevantDocs, queryVector)
        ranks.sort(reverse=True, key= lambda tup:tup[1])
        ranks = list(map(lambda rank: (rank[0],rank[1]/ranks[0][1]),ranks))
        return ranks

    def commonRank(self, relevantDocs, queryVector):
        ranks = []
        for doc in relevantDocs:
            rank = 0
            vector = self.vectors[doc]
            rank += self.cossineSimilarity(vector, queryVector)
            ranks.append((doc, rank))
        return ranks
    
    def tfIdfRank(self, relevantDocs, queryVector):
        ranks = []
        for doc in relevantDocs:
            rank = 0
            vector = self.vectors[doc]
            tfIdfVector = []
            for i in range(0, self.vocabularySize):
                tfIdfVector.append(vector[i]*self.idf[self.vocabularyReverse[i]])
            rank += self.cossineSimilarity(tfIdfVector, queryVector)
            ranks.append((doc, rank))
        return ranks

       
    
    def cossineSimilarity(self, a, b):
        return self.dotProduct(a, b) / math.sqrt(self.dotProduct(a, a)) + math.sqrt(self.dotProduct(b, b))

    def dotProduct(self, a, b):
        ans = 0
        for i in range(0, len(a)):
            ans += a[i] * b[i]
        return ans


        
    
        
