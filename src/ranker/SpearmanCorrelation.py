from PlainTextRanker import PlainTextRanker
from StructuredRanker import StructuredRanker
from scipy.stats import spearmanr

class SpearmanCorrelation():
    def __init__(self, rank1, rank2):
        self.rank1 = list(map(lambda x: x[0], rank1))
        self.rank2 = list(map(lambda x: x[0], rank2))

    def get(self):
        return spearmanr(self.rank1, self.rank2)[0]

structuredQueries = [
    {'title': 'Forbidden Indices',
     'statement': 'You are given a string consisting of'},

    {'title': 'Beautiful Divisors',
     'statement': 'Luba learned about'}
]

queries = ['Chef wants to prepare a Cook-Off contest with 5 problems chosen from a set of  N  problems',
            'the petya and of you maximize the income',
            'Dynamic Programming',
            'help ivan maximize',
            'petya and the required tree']

ranker = PlainTextRanker('indexes/indexNot Shortened.json')
structuredRanker = StructuredRanker('indexes/indexNot Shortened.json')

# file = open("ranker/SpearmanLog.txt", "w")


for query in queries:
    rank1 = ranker.getRank(query, False)
    rank2 = ranker.getRank(query, True)
    spearman = SpearmanCorrelation(rank1, rank2)
    file.write('Calculating spearmarn correlation for [{}] query\n'.format(str(query)))
    file.write(str(spearman.get()))
    file.write('\n\n')

for query in structuredQueries:
    rank1 = structuredRanker.getStructuredRank(query['title'], query['statement'], False)
    rank2 = structuredRanker.getStructuredRank(query['title'], query['statement'], True)
    spearman = SpearmanCorrelation(rank1, rank2)
    file.write('Calculating spearmarn correlation for structured query: ')
    file.write('title:{}\nstatement:{}\n'.format(query['title'], query['statement']))
    file.write(str(spearman.get()))
    file.write('\n\n')
