import logging as logger
import pickle
import pandas as pd
from sklearn.externals import joblib



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
import utils.measurements as meas
import utils.ne as ne


COL_INDIVIDUAL_NAME = 'individual'
COL_ABSTRACT_NAME = 'abstract'
COL_TYPE_NAME = 'type'
COL_NE_TYPE_NAME = 'ne_types'
COL_PREDICTIONS_NAME = 'predictions'
COL_LABELS_NAME = 'labels'
COL_UNSEEN_NAME = 'unseen'

def add_named_entities(une, df, confidence, support, dbonly, reuse_ne_path = ""):

    logger.info("Starting add_named_entities")

    if reuse_ne_path:
        rne_dict = ne.get_ne_dict(reuse_ne_path, COL_INDIVIDUAL_NAME, COL_NE_TYPE_NAME)


    # add a new column for NE types, if not use_ne_types, then is empty anyways
    if une:
        slservice = sl.SpotLightNER()

        net_list = []  # list for NE types
        abs_index = df.columns.get_loc(COL_ABSTRACT_NAME) + 1
        ind_index = df.columns.get_loc(COL_INDIVIDUAL_NAME) + 1

        for (tupin, tup) in enumerate(df.itertuples()):
            logger.debug("NER %s/%s" % (tupin + 1, len(df)))

            individual = tup[ind_index]

            rne_found = False
            if reuse_ne_path:
                logger.debug("Checkin if reusable NE for individual %s" % individual)

                if individual in rne_dict:
                    # there is an existing entry
                    rne_found = True

                    net = rne_dict[individual]

                    logger.debug("Found entities for individual %s, NEs=%s" % (individual,net))

            if not rne_found:

                # if it was not available for reuse, we have to parse it
                abstract = tup[abs_index]
                net = su.to_string(slservice.get_annotations(abstract, confidence, support, dbonly), " ")

            net_list.append(net)

        net_series = pd.Series(net_list)
        df[COL_NE_TYPE_NAME] = net_series.values

    else:
        df[COL_NE_TYPE_NAME] = ""


    logger.info("End add_named_entities")


def get_types_and_abstracts(types_path, abstract_path, res_path, usn=False, upa="", enctyp=False, encabs=False, tmp = False):

    logger.info("Starting get_types_and_abstracts")

    # get types df
    dft = dbp.get_resources_from_types([], types_path, enctyp)

    if usn:
        logger.info("Removing unseen data from the %s entries found" % len(dft))

        # get types df from unseen
        dfut = dbp.get_resources_from_types([], upa)

        # https://stackoverflow.com/questions/27965295/dropping-rows-from-dataframe-based-on-a-not-in-condition
        unseen_ind_list = dfut[COL_INDIVIDUAL_NAME].tolist()


        logger.info("Removing %s unseen entries" % len(unseen_ind_list))

        # save length for loggin
        pre_len = len(dft)

        # remove individuals that are in unseen
        dft = dft[~dft[COL_INDIVIDUAL_NAME].isin(unseen_ind_list)]

        logger.info("Removed %s unseen entries from the total of %s" % (pre_len-len(dft),pre_len))


    # get abstract df
    dfa = dbp.get_resource_abstracts([], abstract_path, encabs)

    # full df types and abstract
    df_full = fu.join_dataframes(dft, dfa)

    #### TEMP

    if tmp:

        gs_list = df_full[COL_INDIVIDUAL_NAME].tolist()

        print(gs_list)

        df_gs_excluded = dft[~dft[COL_INDIVIDUAL_NAME].isin(gs_list)]

        fu.df_to_csv("./tmp_df_gs_excluded", df_gs_excluded)

    ##### TEMP

    logger.info("Got %s type entries, %s abstracts. Combined size=%s" % (len(dft), len(dfa), len(df_full)))

    # store types to disk
    fu.df_to_csv(res_path, df_full)

    logger.debug("Got finally %s entries combining abstract and NEs" % len(df_full))
    logger.info("End of get_types_and_abstracts")


def main():
    """
    # Entry method of the NLP4Types method
    """
    logger.info("Starting NLP 4 Types")


    # TODO: add these as CLI parameters
    # Files
    prefix = args.prefix
    uprefix = args.uprefix
    input_base = args.ibase
    output_base = args.obase
    file_dbo_tree = args.dbtree
    unseen_path = args.upath
    rne_path = args.rnepath


    types_path = '../../data/' + prefix + '_instance_types_en.ttl'
    abstract_path = '../../data/' + prefix + '_long_abstracts_en.ttl'
    unseen_abstract_path = '../../data/' + uprefix + '_long_abstracts_en.ttl'
    res_path = '../../data/results/' + prefix + '_merged_types_abstract.csv'
    res_unseen_path = '../../data/results/' + prefix + '_merged_types_abstract_unseen.csv'
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
    use_lemma = args.lemma
    use_sw = args.sw

    dbonly = args.dbonly
    confidence = args.confidence
    support = args.support
    train_size = args.tsize
    ne_weight = args.neweight
    unseen = args.unseen




    st = ut.Steps(first_step, last_step)

    if st.isstep(1, "Generate types and abstracts"):
        # generate data for types and abstracts
        get_types_and_abstracts(types_path, abstract_path, res_path, unseen, unseen_path, enctyp =True, encabs = True)

    if st.isstep(2, "NER"):  # generate NE types as words

        # load data from disk
        df_types_abs = fu.csv_to_df(res_path)
        logger.info("Combined seen data for a total of %s entries" % len(df_types_abs))


        # generate stats if necessary
        if get_stats:
            stats.column_count(df_types_abs, COL_TYPE_NAME)

        add_named_entities(use_ne_types, df_types_abs, confidence, support, dbonly, reuse_ne_path=rne_path)

        logger.debug("Writing df_types_abs with NE to % s" % ne_res_path)
        fu.df_to_csv(ne_res_path, df_types_abs)

    if st.isstep(3, "Preprocessing"):  # start preprocessing text

        # load data from disk
        df_pre = fu.csv_to_df(ne_res_path)

        print(df_pre.columns)

        # preprocess data
        pp_text_list = pp.process_data_frame(df_pre, use_abstract, COL_ABSTRACT_NAME,
                                             use_ne_types, COL_NE_TYPE_NAME, ne_weight,
                                             use_stemm=use_stemm, use_lemma=use_lemma,use_sw=use_sw)

        # TODO pickle pp_text_list
        pickle.dump(pp_text_list, open(file_pp_text_list, "wb"))

    if st.isstep(4, "Vectorization"): # start vectorization

        # TODO un-pickle pp_text_list
        pp_text_list = pickle.load(open(file_pp_text_list, "rb"))

        # calculate features

        # using training size to calculate the final index
        if not unseen:
            train_index = int(train_size * len(pp_text_list))
        else:
            train_index = len(pp_text_list) #with unseen data, train with everything


        logger.info("Training rows [%s-%s], testing rows [%s-%s]" % (0, train_index, train_index, len(pp_text_list)))

        # vectorize data
        vec_data, vectorizer = feat.vectorize_data(pp_text_list, 0, len(pp_text_list))
        

        # pickle vec_data
        pickle.dump(vec_data, open(file_vec_data, "wb"))
        # pickle vectorizer
        pickle.dump(vectorizer, open(file_vectorizer, "wb"))
        # pickle train_index
        pickle.dump(train_index, open(file_train_index, "wb"))


    if st.isstep(5, "Training"):  # start training


        if 'vec_data' not in locals():
            # un-pickle vec_data
            logger.debug("unpickled %s"  % file_vec_data)
            vec_data = pickle.load(open(file_vec_data, "rb"))


        if 'train_index' not in locals():
            # un-pickle train index
            train_index = pickle.load(open(file_train_index, "rb"))
            logger.debug("unpickled %s, value=%s"  % (file_train_index,train_index))


        # get training labels
        if 'df_pre' not in locals():
            # load data from disk
            df_pre = fu.csv_to_df(ne_res_path)
            logger.debug("Df pre rescued from %s" %  ne_res_path)


        trainig_labels = df_pre[COL_TYPE_NAME].tolist()[:train_index]
        train_data = vec_data[:train_index]

        logger.debug("Training labels ready %s" % len(trainig_labels))

        # train the classifier
        logger.debug("Start training")
        classifier = cls.train_linear_svc(train_data, trainig_labels)
        logger.debug("End training")

        # TODO pickle classifier
        logger.debug("Save classifier to %s" % file_classifier)
        # pickle.dump(classifier, open(file_classifier, "wb"))
        joblib.dump(classifier, file_classifier)

    if st.isstep(6, "Prediction/testing"):  # start prediction

        if unseen:

            if 'vectorizer' not in locals():
                # un-pickle vec_data
                logger.debug("unpickled %s" % file_vectorizer)
                vectorizer = pickle.load(open(file_vectorizer, "rb"))

            logger.info("Getting unseen data for prediction")
            logger.debug("Mind that data from %s should have been previously removed from training set" % res_unseen_path)

            # generate type and abstract for unseen data
            get_types_and_abstracts(unseen_path, unseen_abstract_path, res_unseen_path, enctyp=False, encabs=True, tmp=True)

            # get unseen data from disk
            df_types_abs_unseen = fu.csv_to_df(res_unseen_path)

            logger.info("Got %s entries of unseen data " % len(df_types_abs_unseen))

            add_named_entities(use_ne_types, df_types_abs_unseen, confidence, support, dbonly)

            # preprocess data
            pp_unseen_text_list = pp.process_data_frame(df_types_abs_unseen, use_abstract, COL_ABSTRACT_NAME,
                                                 use_ne_types, COL_NE_TYPE_NAME, ne_weight, use_stemm=use_stemm)


            # use the vectorizer from training data to vectorize unseen data
            prediction_data = feat.vectorize_data_unseen(vectorizer, pp_unseen_text_list)


        else:

            if 'vec_data' not in locals():
                # un-pickle vec_data
                logger.debug("unpickled %s"  % file_vec_data)
                vec_data = pickle.load(open(file_vec_data, "rb"))

            if 'train_index' not in locals():
                # un-pickle train index
                train_index = pickle.load(open(file_train_index, "rb"))
                logger.debug("unpickled %s, value=%s"  % (file_train_index,train_index))

            if 'df_pre' not in locals():
                # load data from disk
                logger.debug("unpickled %s"  % ne_res_path)
                df_pre = fu.csv_to_df(ne_res_path)



            logger.info("train_index=%s" % train_index)
            prediction_data = vec_data[train_index:]


        if 'classifier' not in locals():
            # un-pickle classifier
            logger.debug("unpickled %s"  % file_classifier)
            #classifier = pickle.load(open(file_classifier, "rb"))
            classifier = joblib.load(file_classifier)

        # makes no sense to predict
        if prediction_data.shape[0] <= 0:
            logger.info("Data for prediction is empty, makes no sense to predict. Stopping")
            return

        predictions = []
        try:
            predictions = classifier.predict(prediction_data)
        except Exception as e:
            logger.error('Failed to classify: ' + str(e))
            logger.error('Exiting')
            return

        # save predictions and labels
        if unseen:
            labels = df_types_abs_unseen[COL_TYPE_NAME].tolist()

            print("Predictions %s vs. labels %s" % (len(predictions), len(labels)))
            df_pred = pd.DataFrame({COL_PREDICTIONS_NAME: predictions, COL_LABELS_NAME: labels})
            fu.df_to_csv(pred_res_path, df_pred)
        else:
            labels = df_pre[COL_TYPE_NAME].tolist()[train_index:]
            df_pred = pd.DataFrame({COL_PREDICTIONS_NAME: predictions, COL_LABELS_NAME: labels})
            fu.df_to_csv(pred_res_path, df_pred)



    if st.isstep(7, "Evaluation"): # start measuring performance

        # load data from df
        df_pred_label = fu.csv_to_df(pred_res_path)

        dbtree = pickle.load(open(file_dbo_tree, "rb"))
        logger.debug("unpickled dbtree from: %s" % (file_dbo_tree))

        general_accuracy, hier_prec, hier_recall, hier_f_meas = meas.get_hierarchical_measurements(df_pred_label, COL_PREDICTIONS_NAME, COL_LABELS_NAME, dbtree)

        logger.info("****  Results *****")
        logger.info("* General accuracy=%s" % general_accuracy)
        logger.info("* Hierachical precission=%s" % hier_prec)
        logger.info("* Hierachical recall=%s" % hier_recall)
        logger.info("* Hierachical F-measure=%s" % hier_f_meas)

    st.endsteps()

    logger.info(st.get_print_times())

    logger.info("Arguments %s" % args)

    pickle.dump(args, open(file_args, "wb"))

    logger.info("End of NLP 4 Types")


# change this to file config
if __name__ == '__main__':
    import logging.config


    ps = uarg.Args()
    args = ps.get_args()


    logfile='log_nlp4types.log'
    if args.log:
        logfile = args.log


    logging.basicConfig(filename=logfile, format='%(asctime)s %(levelname)s %(message)s',
                        level=logger.DEBUG)

    logger.info("Arguments %s" % args)

    main()
