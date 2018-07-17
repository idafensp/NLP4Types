import logging as logger
import pickle
import pandas as pd
import collections



import utils.filesutils as fu
import utils.classifiers as cls
import utils.utils as ut
import utils.args as uarg
import utils.unseen_data as ud
import utils.measurements as meas


COL_ABSTRACT_NAME = 'abstract'
COL_TYPE_NAME = 'type'
COL_NE_TYPE_NAME = 'ne_types'
COL_PREDICTIONS_NAME = 'predictions'
COL_LABELS_NAME = 'labels'


def main():
    """
    # Entry method of the NLP4Types method
    """
    logger.info("Starting Cross Validation process")


    # TODO: add these as CLI parameters
    # Files
    prefix = args.prefix
    input_base = args.ibase
    output_base = args.obase
    file_dbo_tree = args.dbtree

    types_path = '../../data/' + prefix + '_instance_types_en.ttl'
    abstract_path = '../../data/' + prefix + '_long_abstracts_en.ttl'
    res_path = '../../data/results/' + prefix + '_merged_types_abstract.csv'
    ne_res_path = '../../data/results/' + prefix + '_ne_types_abstract.csv'
    pred_cv_res_path = '../../data/results/' + prefix + '_cv_pred_and_labels.csv'
    file_pp_text_list = '../../data/results/' + prefix + '_pp_text_list.p'
    file_vec_data = '../../data/results/' + prefix + '_vec_data.p'
    file_vectorizer = '../../data/results/' + prefix + '_vectorizer.p'
    file_classifier = '../../data/results/' + prefix + '_classifier.p'
    file_cv_predictions = '../../data/results/' + prefix + '_cv_predictions.p'
    file_args = '../../data/results/' + prefix + '_args_cv.p'
    file_unseen_df = '../../data/results/' + prefix + '_unseen_df.p'
    file_unseen_data_vec = '../../data/results/' + prefix + '_unseen_data_vec.p'

    # Parameters
    first_step = args.fstep
    last_step = args.lstep
    unseen = args.unseen
    cv = args.cv




    st = ut.Steps(first_step, last_step)


    if st.isstep(1):  # start CV

        if 'vec_data' not in locals():
            # un-pickle vec_data
            logger.debug("unpickled %s"  % file_vec_data)
            vec_data = pickle.load(open(file_vec_data, "rb"))


        # get training labels
        if 'df_pre' not in locals():
            # load data from disk
            df_pre = fu.csv_to_df(ne_res_path)
            logger.debug("Df pre rescued from %s" %  ne_res_path)

        trainig_labels = df_pre[COL_TYPE_NAME].tolist()

        logger.debug("CV labels ready %s" % len(trainig_labels))

        labels_counter = collections.Counter(trainig_labels)

        for c in labels_counter:
            logger.debug(c)

        # cross validation
        logger.debug("Start cross validation")
        predictions = classifier = cls.cross_validation_linear_svc(vec_data, trainig_labels, cv)
        logger.debug("End cross validation")

        # pickle cv predictions
        pickle.dump(predictions, open(file_cv_predictions, "wb"))
        logger.info("Pickled CV predictions to %s" % file_cv_predictions)

        logger.info("predictions (size=%s):\n %s" % (len(predictions),predictions))

        # we use training labels, as we are training with everything
        df_pred = pd.DataFrame({COL_PREDICTIONS_NAME: predictions, COL_LABELS_NAME: trainig_labels})
        fu.df_to_csv(pred_cv_res_path, df_pred)

    if st.isstep(2): # start measuring performance

        # load data from df
        df_pred_label = fu.csv_to_df(pred_cv_res_path)

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

    logger.info("End of Cross Validation process")


# change this to file config
if __name__ == '__main__':
    import logging.config


    ps = uarg.Args()
    args = ps.get_args()


    logfile='log_cv.log'
    if args.log:
        logfile = args.log


    logging.basicConfig(filename=logfile, format='%(asctime)s %(levelname)s %(message)s',
                        level=logger.DEBUG)

    logger.info("Arguments %s" % args)

    main()
