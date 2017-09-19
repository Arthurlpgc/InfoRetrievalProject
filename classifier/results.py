from features import create_corpus
from text_pipeline import TextPipeline
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

def grid_search_random_forest():
    rf_parameters = {
        "max_depth": [3, None],
        "max_features": ["log2", "sqrt", None],
        "min_samples_split": [2, 3, 10],
        "min_samples_leaf": [1, 3, 10],
        "bootstrap": [True, False],
        "criterion": ["gini", "entropy"]
    }

    pipeline = TextPipeline(RandomForestClassifier(), rf_parameters, n_jobs=6, verbose = 1)
    corpus_folder = "pages_preprocessed/"
    corpus, metadata = create_corpus(corpus_folder, ["bad", "good"])
    pipeline.fit(corpus, np.array(metadata['label']))
    pipeline.save_results("results/random_forest_results.csv")


def grid_search_svm():
    svc_parameters = {
        'C': (1, 10, 100, 1000),
        'gamma': ('auto', 0.001, 0.01, 0.1, 1),
        'kernel': ('poly', 'rbf')
    }

    pipeline = TextPipeline(SVC(), svc_parameters, n_jobs=6, verbose = 1)
    corpus_folder = "pages_preprocessed/"
    corpus, metadata = create_corpus(corpus_folder, ["bad", "good"])
    pipeline.fit(corpus, np.array(metadata['label']))
    pipeline.save_results("results/svm_results.csv")

if __name__ == "__main__":
    # grid_search_svm()
    grid_search_random_forest()
