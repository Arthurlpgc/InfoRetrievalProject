from PlainTextRanker import PlainTextRanker
from scipy.stats import spearmanr

class SpearmanCorrelation():
    def __init__(self, rank1, rank2):
        self.rank1 = list(map(lambda x: x[0], rank1))
        self.rank2 = list(map(lambda x: x[0], rank2))
    
    def get(self):
        return spearmanr(self.rank1, self.rank2)[0]

queries = ['Chef wants to prepare a Cook-Off contest with 5 problems chosen from a set of  N  problems','the petya and of you maximize the income', 'Dynamic Programming', 'A map of treasures', 'help ivan maximize', 'petya and the required tree', 'the following lines contain words']

ranker = PlainTextRanker('indexes/indexNot Shortened.json')

file = open("ranker/SpearmanLog.txt", "w")


for query in queries:
    rank1 = ranker.getRank(query, False)
    rank2 = ranker.getRank(query, True)
    spearman = SpearmanCorrelation(rank1, rank2)
    file.write('Calculating spearmarn correlation for [{}] query\n'.format(str(query)))
    file.write(str(spearman.get()))
    file.write('\n\n')

