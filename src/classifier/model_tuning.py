from features import create_corpus
from text_pipeline import TextPipeline
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

def binarize(string):
    if(string == "bad"):
        return 0
    else:
        return 1

def grid_search_knn():
    knn_parameters = {
        "n_neighbors": [1, 2, 3, 4],
        "weights": ["uniform", "distance"],
    }

    pipeline = TextPipeline(KNeighborsClassifier(), knn_parameters, n_jobs=-1, verbose = 1)
    corpus_folder = "train_pages_preprocessed/"
    corpus, metadata = create_corpus(corpus_folder, ["bad", "good"])
    vfunc = np.vectorize(binarize)
    pipeline.fit(corpus, vfunc(metadata['label']))
    pipeline.save_results("results/knn_results.csv")

def grid_search_mlp():
    mlp_parameters = {
        "activation": ["relu", "tanh", "logistic"],
        "learning_rate_init":[0.001, 0.01, 0.1, 1],
        "hidden_layer_sizes":[(1000,), (5000,), (10000,),(30000,)]
    }

    pipeline = TextPipeline(MLPClassifier(), mlp_parameters, n_jobs=4, verbose = 1)
    corpus_folder = "train_pages_preprocessed/"
    corpus, metadata = create_corpus(corpus_folder, ["bad", "good"])
    vfunc = np.vectorize(binarize)
    pipeline.fit(corpus, vfunc(metadata['label']))
    pipeline.save_results("results/mlp_results.csv")

def grid_search_multinomial_nb():
    nb_parameters = {
        "alpha": [1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    }

    pipeline = TextPipeline(MultinomialNB(), nb_parameters, n_jobs=6, verbose = 1)
    corpus_folder = "train_pages_preprocessed/"
    corpus, metadata = create_corpus(corpus_folder, ["bad", "good"])
    vfunc = np.vectorize(binarize)
    pipeline.fit(corpus, vfunc(metadata['label']))
    pipeline.save_results("results/naive_bayes_results.csv")

def grid_search_logistic_regression():
    lg_parameters = {
        "penalty": ["l1", "l2"],
        "C": [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    }

    pipeline = TextPipeline(LogisticRegression(), lg_parameters, n_jobs=6, verbose = 1)
    corpus_folder = "train_pages_preprocessed/"
    corpus, metadata = create_corpus(corpus_folder, ["bad", "good"])
    vfunc = np.vectorize(binarize)
    pipeline.fit(corpus, vfunc(metadata['label']))
    pipeline.save_results("results/logistic_regression_results.csv")

def grid_search_random_forest():
    rf_parameters = {
        "max_depth": [3, None],
        "max_features": ["log2", "sqrt", None],
        "min_samples_split": [2, 3, 10],
        "min_samples_leaf": [1, 3, 10],
        "criterion": ["gini"]
    }

    pipeline = TextPipeline(RandomForestClassifier(), rf_parameters, n_jobs=6, verbose = 1)
    corpus_folder = "train_pages_preprocessed/"
    corpus, metadata = create_corpus(corpus_folder, ["bad", "good"])
    vfunc = np.vectorize(binarize)
    pipeline.fit(corpus, vfunc(metadata['label']))
    pipeline.save_results("results/random_forest_results2.csv")


def grid_search_svm():
    svc_parameters = {
        'C': (0.1, 1, 10, 100), #0.1 remover 100
        'gamma': ('auto', 0.001, 0.01, 0.1, 1),
        'kernel': ('poly', 'rbf')
    }

    pipeline = TextPipeline(SVC(), svc_parameters, n_jobs=6, verbose = 1)
    corpus_folder = "train_pages_preprocessed/"
    corpus, metadata = create_corpus(corpus_folder, ["bad", "good"])
    vfunc = np.vectorize(binarize)
    pipeline.fit(corpus, vfunc(metadata['label']))
    pipeline.save_results("results/svm_results2.csv")
#
if __name__ == "__main__":
    # grid_search_svm()
    # grid_search_random_forest()
    # grid_search_logistic_regression()
    # grid_search_multinomial_nb()
    # Descomente se quiser brincar de interstellar
    # grid_search_mlp()
    grid_search_knn()
