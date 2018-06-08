import logging as logger
import pickle
import pandas as pd


import utils.dbpedia as dbp
import utils.filesutils as fu
import utils.stats as stats
import utils.stringutils as su
import utils.spotlight as sl
import utils.features as feat
import utils.preprocess as pp
import utils.classifiers as cls
import utils.utils as ut
import utils.args as uarg
import utils.unseen_data as ud


COL_ABSTRACT_NAME = 'abstract'
COL_TYPE_NAME = 'type'
COL_NE_TYPE_NAME = 'ne_types'
COL_PREDICTIONS_NAME = 'predictions'
COL_LABELS_NAME = 'labels'

def get_types_and_abstracts(types_path, abstract_path, res_path):
    logger.info("Starting get_types_and_abstracts")
    dft = dbp.get_resources_from_types([], types_path)

    dfa = dbp.get_resource_abstracts([], abstract_path)

    # print(dfa)

    df_full = fu.join_dataframes(dft, dfa)

    # print(len(df_full))
    # print(df_full['individual'])
    # print(df_full['type'])
    # print(df_full['abstract'])

    fu.df_to_csv(res_path, df_full)

    logger.info("End of get_types_and_abstracts")


def main():
    """
    # Entry method of the NLP4Types method
    """
    logger.info("Starting NLP 4 Types")

    ps = uarg.Args()
    args = ps.get_args()

    logger.info("Arguments %s" % args)

    # TODO: add these as CLI parameters
    # Files
    prefix = args.prefix
    input_base = args.ibase
    output_base = args.obase

    types_path = '../../data/' + prefix + '_instance_types_en.ttl'
    abstract_path = '../../data/' + prefix + '_long_abstracts_en.ttl'
    res_path = '../../data/results/' + prefix + '_merged_types_abstract.csv'
    ne_res_path = '../../data/results/' + prefix + '_ne_types_abstract.csv'
    pred_res_path = '../../data/results/' + prefix + '_pred_and_labels.csv'
    file_pp_text_list = '../../data/results/' + prefix + '_pp_text_list.p'
    file_vec_data = '../../data/results/' + prefix + '_vec_data.p'
    file_vectorizer = '../../data/results/' + prefix + '_vectorizer.p'
    file_classifier = '../../data/results/' + prefix + '_classifier.p'
    file_train_index = '../../data/results/' + prefix + '_train_index.p'
    file_args = '../../data/results/' + prefix + '_args.p'
    file_unseen_df = '../../data/results/' + prefix + '_unseen_df.p'
    file_unseen_data_vec = '../../data/results/' + prefix + '_unseen_data_vec.p'

    # Parameters
    first_step = args.fstep
    last_step = args.lstep
    get_stats = args.stats
    use_abstract = args.abstract
    use_ne_types = args.ner
    use_stemm = args.stemm
    dbonly = args.dbonly
    confidence = args.confidence
    support = args.support
    train_size = args.tsize
    ne_weight = args.neweight
    unseen = args.unseen





    st = ut.Steps(first_step, last_step)

    if st.isstep(1):
        # generate data for types and abstracts
        get_types_and_abstracts(types_path, abstract_path, res_path)

    if st.isstep(2):  # generate NE types as words

        # load data from disk
        df_types_abs = fu.csv_to_df(res_path)

        # generate stats if necessary
        if get_stats:
            stats.column_count(df_types_abs, COL_TYPE_NAME)

        # add a new column for NE types, if not use_ne_types, then is empty anyways
        if use_ne_types:
            slservice = sl.SpotLightNER()

            net_list = []  # list for NE types
            abs_index = df_types_abs.columns.get_loc(COL_ABSTRACT_NAME) + 1
            for (tupin, tup) in enumerate(df_types_abs.itertuples()):
                logger.debug("NER %s/%s" % (tupin, len(df_types_abs)))
                abstract = tup[abs_index]
                net = su.to_string(slservice.get_annotations(abstract, confidence, support, dbonly), " ")
                net_list.append(net)

            net_series = pd.Series(net_list)
            df_types_abs[COL_NE_TYPE_NAME] = net_series.values

        else:
            df_types_abs[COL_NE_TYPE_NAME] = ""

        fu.df_to_csv(ne_res_path, df_types_abs)

    if st.isstep(3):  # start preprocessing text

        # load data from disk
        df_pre = fu.csv_to_df(ne_res_path)

        print(df_pre.columns)

        # preprocess data
        pp_text_list = pp.process_data_frame(df_pre, use_abstract, COL_ABSTRACT_NAME,
                                             use_ne_types, COL_NE_TYPE_NAME, ne_weight, use_stemm=use_stemm)

        # TODO pickle pp_text_list
        pickle.dump(pp_text_list, open(file_pp_text_list, "wb"))

    if st.isstep(4): # start vectorization

        # TODO un-pickle pp_text_list
        pp_text_list = pickle.load(open(file_pp_text_list, "rb"))

        # calculate features

        # using training size to calculate the final index
        train_index = int(train_size * len(pp_text_list))

        logger.info("Training rows [%s-%s], testing rows [%s-%s]" % (0, train_index, train_index, len(pp_text_list)))

        # vectorize data
        vec_data, vectorizer = feat.vectorize_data(pp_text_list, 0, len(pp_text_list))

        # TODO pickle vec_data
        pickle.dump(vec_data, open(file_vec_data, "wb"))
        # TODO pickle vectorizer
        pickle.dump(vectorizer, open(file_vectorizer, "wb"))
        # TODO pickle train_index
        pickle.dump(train_index, open(file_train_index, "wb"))


    if st.isstep(5):  # start training

        # TODO un-pickle vec_data
        vec_data = pickle.load(open(file_vec_data, "rb"))

        if 'train_index' not in locals():
            # TODO un-pickle train index
            train_index = pickle.load(open(file_train_index, "rb"))
            print("train index is ", train_index)

        train_data = vec_data[:train_index]

        # get training labels
        if 'df_pre' not in locals():
            # load data from disk
            df_pre = fu.csv_to_df(ne_res_path)
            print("Df pre rescued")

        trainig_labels = df_pre[COL_TYPE_NAME].tolist()[:train_index]


        # train the classifier
        classifier = cls.train_linear_svc(train_data, trainig_labels)

        # TODO pickle classifier
        pickle.dump(classifier, open(file_classifier, "wb"))

    if st.isstep(6):  # start prediction

        if 'vec_data' not in locals():
            # un-pickle vec_data
            vec_data = pickle.load(open(file_vec_data, "rb"))

        if 'classifier' not in locals():
            # un-pickle classifier
            classifier = pickle.load(open(file_classifier, "rb"))

        # Predict
        if unseen:
            prediction_data = ud.get_unseen_data_features(file_vectorizer, unseen_df_file,
                                        unseen_data_vec_file, use_abstract, COL_ABSTRACT_NAME,
                                        use_ne_types, COL_NE_TYPE_NAME, ne_weight,
                                        use_stemm=use_stemm)
        else:
            prediction_data = vec_data[train_index:]



        # makes no sense to predict
        if not prediction_data.any():
            return

        predictions = []
        try:
            predictions = classifier.predict(prediction_data)
        except Exception as e:
            logger.error('Failed to classify: ' + str(e))
            logger.error('Exiting')
            return

        # save predictions and labels
        labels = df_pre['type'].tolist()[train_index:]
        df_pred = pd.DataFrame({COL_PREDICTIONS_NAME: predictions, COL_LABELS_NAME: labels})

        fu.df_to_csv(pred_res_path, df_pred)

    if st.isstep(7): # start measuring performance

        # load data from df
        df_pred_label = fu.csv_to_df(pred_res_path)

        pred_index = df_pred_label.columns.get_loc(COL_PREDICTIONS_NAME) + 1
        label_index = df_pred_label.columns.get_loc(COL_LABELS_NAME) + 1

        hits = 0
        for tup in df_pred_label.itertuples():
            prec = tup[pred_index]
            labc = tup[label_index]
            if prec == labc:
                hits += 1

        logger.info("Hits=%s, errors=%s" % (hits, len(df_pred_label)-hits))
        logger.info("Accuracy %s/%s=%s" % (hits, len(df_pred_label), float(hits)/len(df_pred_label)))


    st.endsteps()

    logger.info(st.get_print_times())

    logger.info("Arguments %s" % args)

    pickle.dump(args, open(file_args, "wb"))

    logger.info("End of NLP 4 Types")


# change this to file config
if __name__ == '__main__':
    import logging.config

    logging.basicConfig(filename='log_nlp4types.log', format='%(asctime)s %(levelname)s %(message)s',
                        level=logger.DEBUG)
    main()
