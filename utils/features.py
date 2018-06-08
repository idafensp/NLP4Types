# https://github.com/bonzanini/nlp-tutorial/blob/master/notebooks/03%20text_classification_Generic.ipynb

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import preprocess as pp

import logging
logger = logging.getLogger(__name__)


def custom_tokenizer(s):
    return s.split()

def vectorize_data(text_list, from_ind, to_ind,  use_tf_idf = True):

    logger.info("Starting vectorize_data for a text list with %s entries, use_tf_idf?=%s," % (len(text_list), use_tf_idf))
    logger.debug("From entry= %s, to entry = %s" % (from_ind, to_ind))


    #time to vectorize, either using count or tf-idf
    logger.info("vectorize_data - vectorization")
    if use_tf_idf:

        train_data = text_list[from_ind:to_ind]

        # Representation of the data using TF-IDF
        vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
        vectorised_train_data = vectorizer.fit_transform(train_data)
        return vectorised_train_data

    else:
        # TODO:
        logger.warning("TODO: pending count vectorizer")

    logger.info("End of vectorize_data, returning a list of %s entries" % len(return_list))

    return []
