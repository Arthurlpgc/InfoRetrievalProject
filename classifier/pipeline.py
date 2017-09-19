import features
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import pandas as pd

from pprint import pprint
from time import time
import logging

import models
import numpy as np

folder = "pages_preprocessed/"
corpus, metadata = features.create_corpus(folder, ["bad", "good"])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
# models.svm(X.toarray(), np.array(metadata['label']))

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# #############################################################################
# Define a pipeline combining a text feature extractor with a simple
# classifier
#Fazer o clf virar um parametro externo a classe
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC()),
])

# uncommenting more parameters will give better exploring power but will
# increase processing time in a combinatorial way
#fazer os parametros do clf virarem parametros externos a classe
parameters = {
    'vect__max_df': (0.5, 0.75, 1.0),
    'vect__max_features': (None, 5000, 10000, 50000),
    'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    'tfidf__use_idf': (True, False),
    'tfidf__norm': ('l1', 'l2'),
    'clf__C': (1, 10, 100, 1000),
    'clf__gamma': ('auto', 0.001, 0.01, 0.1, 1),
    'clf__kernel': ('poly', 'rbf')
}

if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=6, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(corpus, np.array(metadata['label']))
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
    #Save Results
    df = pd.DataFrame(grid_search.cv_results_)
    df.to_csv('results/svm_results.csv')
