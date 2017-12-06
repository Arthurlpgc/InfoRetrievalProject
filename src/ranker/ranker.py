import json
import numpy
import re
import csv
import math

class Ranker():
    def __init__(self, indexPath):
        self.index = json.load(open(indexPath))
        #build a vocabulary from each word that appears in index
        self.titleVocabulary = {}
        self.titleVocabularyIndex = 0
        self.statementVocabulary = {}
        self.statementVocabularyIndex = 0
        for key in self.index:
            if('.title' in key):
                self.titleVocabulary[key] = self.titleVocabularyIndex
                self.titleVocabularyIndex = self.titleVocabularyIndex + 1
            elif('.statement' in key):
                self.statementVocabulary[key] = self.statementVocabularyIndex
                self.statementVocabularyIndex = self.statementVocabularyIndex + 1
        #defines weights for each attribute in the query
        self.weights = {'title': 1, 'statement': 2}
        self.vocabularySizes = {'title': len(self.titleVocabulary), 'statement': len(self.statementVocabulary)}
        #creates the vector space representation for each document in index database
        self.vectors = []
        self.vectorsSize = 0
        with open('indexes/name.csv') as documents:
            for row in csv.reader(documents):
                self.aa = -1
                for name in row:
                    self.aa += 1
                    if(self.aa == 58):
                        print(name)
                    self.vectors.append({'title': numpy.zeros(self.vocabularySizes['title']), 'statement': numpy.zeros(self.vocabularySizes['statement'])})
                    document = json.load(open('retrieved/objects/{}.json'.format(name)))
                    title = re.sub("[^\w]", " ",  document['title']).split()
                    title=list(map(lambda x:x.lower()+'.title',title))
                    statement = re.sub("[^\w]", " ",  document['statement']).split()
                    statement=list(map(lambda x:x.lower()+'.statement',statement))
                    for word in title:
                        self.vectors[self.vectorsSize]['title'][self.titleVocabulary[word]] += 1
                    for word in statement:
                        self.vectors[self.vectorsSize]['statement'][self.statementVocabulary[word]] += 1
                    self.vectorsSize += 1

    def getStructuredRank(self, title, statement):
        title = [word + '.title' for word in title.lower().split(' ')]
        statement = [word + '.statement' for word in statement.lower().split(' ')]
        #gets the list of relevant documents for this query
        relevantDocs = []
        for word in title:
            if(word in self.index):
                relevantDocs += self.index[word]
        for word in statement:
            if(word in self.index):
                relevantDocs += self.index[word]
        relevantDocs = list(set(relevantDocs))
        #creates the vector space for this query
        return self.rankDocumentAtTime(relevantDocs, title, statement)

    def rankDocumentAtTime(self, relevantDocs, title, statement):
        queryVector = {'title': numpy.zeros(self.vocabularySizes['title']), 'statement': numpy.zeros(self.vocabularySizes['statement'])}
        for word in title:
            if(word in self.titleVocabulary):
                queryVector['title'][self.titleVocabulary[word]] += 1
        for word in statement:
            if(word in self.statementVocabulary):
                queryVector['statement'][self.statementVocabulary[word]] += 1
        ranks = []
        for doc in relevantDocs:
            rank = 0
            for attribute in self.weights:
                vector = self.vectors[doc][attribute]
                rank += self.weights[attribute] * self.cossineSimilarity(vector, queryVector[attribute])
            ranks.append((doc, rank))
        ranks.sort(reverse=True, key= lambda tup:tup[1])
        ranks = list(map(lambda rank: (rank[0],rank[1]/ranks[0][1]),ranks))
        return ranks
    
    def cossineSimilarity(self, a, b):
        return self.dotProduct(a, b) / math.sqrt(self.dotProduct(a, a)) + math.sqrt(self.dotProduct(b, b))

    def dotProduct(self, a, b):
        ans = 0
        for i in range(0, len(a)):
            ans += a[i] * b[i]
        return ans


        
    
        
