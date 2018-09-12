# https://github.com/bonzanini/nlp-tutorial/blob/master/notebooks/03%20text_classification_Generic.ipynb

from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_predict

import logging
logger = logging.getLogger(__name__)

def train_classifier(classifier, train_data, train_labels):
    return train_linear_svc(train_data, train_labels)


def train_linear_svc(train_data, train_labels):
    # Train
    classifier = LinearSVC()
    classifier.fit(train_data, train_labels)

    return classifier

# http://scikit-learn.org/stable/modules/cross_validation.html
def cross_validation(classifier, train_data, train_labels, folds=5):
    return cross_validation_linear_svc(train_data,train_labels, folds)



def cross_validation_linear_svc(train_data, train_labels, folds=5):
    classifier = LinearSVC()
    return cross_val_predict(classifier, train_data, train_labels, cv=folds, verbose=2)


# TODO https://towardsdatascience.com/multi-label-text-classification-with-scikit-learn-30714b7819c5
# multilabel, returting several types and their scores (when possible)