import os
from sklearn.feature_extraction.text import CountVectorizer

def create_features(corpus):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(X.toarray())

def create_corpus(folder, label):
    corpus_metadata = {'file_name': [], 'label':[]}
    corpus = []

    for item in label:
        folder_path = os.path.abspath(folder + item)
        for file in  os.listdir(folder_path):
            with open(folder_path + "/" + file, 'r', encoding="utf8") as myfile:
                corpus_metadata['file_name'].append(file)
                corpus_metadata['label'].append(item)
                corpus.append(myfile.read())
                myfile.close()

    return corpus, corpus_metadata


def main():
    folder = "pages_preprocessed/"
    corpus, metadata = create_corpus(folder, ["bad", "good"])
    create_features(corpus)

if __name__ == "__main__":
    main()
