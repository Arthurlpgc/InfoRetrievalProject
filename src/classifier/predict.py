from classifier.features import create_corpus
from classifier.preprocesser import text_from_html

from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

print("Training classifier with 100 coding questions examples and 100 junk examples...")
all_corpus, all_metadata = create_corpus("classifier/pages_preprocessed/", ["bad", "good"])
clf = make_pipeline(CountVectorizer(max_df=1.0, max_features=5000, ngram_range=(1,2)),
                    TfidfTransformer(use_idf=False, norm="l2"),
                    SVC(C=10, gamma=1, kernel='poly'))
clf.fit(all_corpus, all_metadata['label'])
print("Training complete")

#Receives page html FILE
def check_if_is_coding_question(page_body):
    visible_text = text_from_html(page_body)
    predicao = clf.predict([visible_text])
    return predicao[0]
