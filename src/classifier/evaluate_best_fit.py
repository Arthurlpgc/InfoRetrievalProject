from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from features import create_corpus

import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(y_test, y_pred, cm, classes, normalize=True, title='Confusion matrix'):
    cmap=plt.cm.Blues
    if (normalize):
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for (i, j) in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    # Compute confusion matrix
    cnf_matrix = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)

    plt.show()

def binarize(string):
    if(string == "bad"):
        return 0
    else:
        return 1

def svm():
    train_corpus = "train_pages_preprocessed/"
    test_corpus = "test_pages_preprocessed/"
    corpus_train, metadata_train = create_corpus(train_corpus, ["bad", "good"])
    corpus_test, metadata_test = create_corpus(test_corpus, ["bad", "good"])
    vfunc = np.vectorize(binarize)

    scoring = ['precision_macro', 'f1_macro', 'recall_macro', 'accuracy', 'roc_auc']
    clf = make_pipeline(CountVectorizer(max_df=1.0, max_features=5000, ngram_range=(1,2)),TfidfTransformer(use_idf=False, norm="l2"),SVC(C=10, gamma=1, kernel='poly'))
    clf.fit(corpus_train, vfunc(metadata_train['label']))
    predicao = clf.predict(corpus_test)
    print(classification_report(vfunc(metadata_test['label']), predicao))
    plot_confusion_matrix(vfunc(metadata_test['label']), predicao, confusion_matrix(vfunc(metadata_test['label']), predicao), ["Coding Question", "Junk"],
                              normalize=False,
                              title='Confusion matrix')

svm()
