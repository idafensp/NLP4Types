from nltk.stem import *
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords

import logging
logger = logging.getLogger(__name__)
STEP_PROGRESS = 5000

# TODO: we could add stemmer and lemmatizer objects as params, so as to save time
def process_text(raw_text, use_sw = False, use_lemma = False, use_stemm = False):

    # TODO: improve the way we tokenize if necessary
    words = raw_text.lower().split()

    if use_sw:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]

    if use_lemma:
        wordnet_lemmatizer = WordNetLemmatizer()
        # TODO: here we should use POS tagging to improve lemmas
        words = [wordnet_lemmatizer.lemmatize(word) for word in words]

    if use_stemm:
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]

    #return words
    return (" ".join(words))

def process_data_frame(df, use_abs = True, col_abs = "", use_ne = True, colne = "", ne_w = 1,
                       use_sw = False, use_lemma = False, use_stemm = False):

    logger.info("Starting process_data_frame for a df with %s rows" % (len(df)))
    logger.debug("""use_abs = %s, col_abs = %s, use_ne = %s, colne = %s, 
                    ne_w = %s, use_sw = %s, use_lemma = %s, use_stemm = %s"""
                 % (use_abs, col_abs, use_ne, colne ,
                    ne_w , use_sw , use_lemma , use_stemm))

    colabs_index = df.columns.get_loc(col_abs)+1
    colne_index = df.columns.get_loc(colne)+1

    # list of preprocessed text
    pp_list = []
    for (index, tup) in enumerate(df.itertuples()):

        if index % STEP_PROGRESS == 0:
            logger.debug("Preprocessed %s/%s" % (index, len(df)))

        pp_text = ""
        if use_abs:
            text = tup[colabs_index]
            pp_text = pp_text + " " + process_text(text, use_sw, use_lemma, use_stemm)

        if use_ne:
            ne_types = tup[colne_index]

            if isinstance(ne_types, unicode):
                ne_types = (ne_types+" ") * ne_w
                pp_text = pp_text + " " + ne_types

        pp_list.append(pp_text)


    return pp_list