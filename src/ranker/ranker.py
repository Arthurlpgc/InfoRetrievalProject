import json
import numpy
import re
import csv

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
        self.weights = {'title': 2, 'statement': 1}
        self.vocabularySizes = {'title': len(self.titleVocabulary), 'statement': len(self.statementVocabulary)}
        #creates the vector space representation for each document in index database
        self.vectors = []
        self.vectorsSize = 0
        with open('indexes/name.csv') as documents:
            for row in csv.reader(documents):
                for name in row:
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
                    print(self.vectors[self.vectorsSize])
                    self.vectorsSize += 1



    def getStructuredRank(self, title, statement):
        title = [word + '.title' for word in title.lower().split(' ')]
        statement = [word + '.statement' for word in statement.lower().split(' ')]
    
        
