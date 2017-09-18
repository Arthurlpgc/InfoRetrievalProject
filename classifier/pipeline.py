import features
from sklearn.feature_extraction.text import CountVectorizer
import models
import numpy as np

folder = "pages_preprocessed/"
corpus, metadata = features.create_corpus(folder, ["bad", "good"])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
models.svm(X.toarray(), np.array(metadata['label']))
