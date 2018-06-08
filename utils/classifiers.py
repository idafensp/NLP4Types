# https://github.com/bonzanini/nlp-tutorial/blob/master/notebooks/03%20text_classification_Generic.ipynb

from sklearn.svm import LinearSVC
import preprocess as pp


import logging
logger = logging.getLogger(__name__)

def train_classifier(classifier, train_data, train_labels):
    return train_linear_svc(train_data, train_labels)

def train_linear_svc(train_data, train_labels):
    # Train
    classifier = LinearSVC()
    classifier.fit(train_data, train_labels)

    return classifier
