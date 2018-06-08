from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import preprocess as pp
import pickle
import pandas as pd

import preprocess as pp
import features as feat


import logging
logger = logging.getLogger(__name__)


def get_unseen_data_features(vectorizer_file, df_file, vec_result_file, use_abs = True, col_abs = "", use_ne = True, colne = "", ne_w = 1,
                       use_sw = False, use_lemma = False, use_stemm = False):

    logger.info("Starting get_unseen_data_features for %s, %s" % vectorizer_file, df_file)

    # load vectorizer
    vectorizer = pickle.load(open(vectorizer_file, "rb"))

    # load dataframe
    df_pre = pickle.load(open(df_file, "rb"))

    # preprocess data
    pp_text_list = pp.process_data_frame(df_pre, use_abs, col_abs,
                                         use_ne, colne, ne_w, use_sw, use_lemma, use_stemm)

    vec_data, vectorizer = feat.vectorize_data(pp_text_list, 0, len(pp_text_list))

    # pickle vec_data
    pickle.dump(vec_data, open(vec_result_file, "wb"))

    return vec_data





