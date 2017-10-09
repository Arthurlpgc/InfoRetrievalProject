from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd

from pprint import pprint
from time import time

class TextPipeline:
    def __init__(self, classifier, clf_parameters, n_jobs=-1, verbose=1):
        self.pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', classifier),
        ])
        self.parameters = {
            'vect__max_df': (0.5, 0.75, 1.0), #corpus-based stopwords selection
            'vect__max_features': (None, 5000, 10000, 50000), #frequency feature selection
            'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
            'tfidf__use_idf': (True, False),
            'tfidf__norm': ('l1', 'l2')

        }
        #Insert clf parameters
        for key, value in clf_parameters.items():
            self.parameters.update({"clf__" + key: value})
        self.verbose = verbose
        self.scoring = ['precision_macro', 'f1_macro', 'recall_macro', 'accuracy', 'roc_auc']

        #Init Grid Search
        self.grid_search = GridSearchCV(self.pipeline, self.parameters, n_jobs=n_jobs, verbose=self.verbose, scoring=self.scoring, refit="f1_macro")


    def fit(self, corpus, output):
        if(self.verbose):
            print("Performing grid search...")
            print("pipeline:", [name for name, _ in self.pipeline.steps])
            print("parameters:")
            pprint(self.parameters)
            t0 = time()
            self.grid_search.fit(corpus, output)
            print("done in %0.3fs" % (time() - t0))
            print()
            print("Best score: %0.3f" % self.grid_search.best_score_)
            print("Best parameters set:")
            best_parameters = self.grid_search.best_estimator_.get_params()
            for param_name in sorted(self.parameters.keys()):
                print("\t%s: %r" % (param_name, best_parameters[param_name]))
        else:
            self.grid_search.fit(corpus, output)

    def get_grid_search(self):
        return self.grid_search

    def get_best_score_and_parameters(self):
        return self.grid_search.best_score_, self.grid_search.best_estimator_.get_params()

    def save_results(self, pathfile):
        df = pd.DataFrame(self.grid_search.cv_results_)

        if(pathfile.endswith('.csv')):
            df.to_csv(pathfile)
        else:
            raise NameError('The file has to be a csv!')
