import logging as logger
import pickle
import rdflib
import utils.measurements as meas
import utils.filesutils as fu

COL_ABSTRACT_NAME = 'abstract'
COL_TYPE_NAME = 'type'
COL_NE_TYPE_NAME = 'ne_types'
COL_PREDICTIONS_NAME = 'predictions'
COL_LABELS_NAME = 'labels'

import utils.dbotypes as dbo

def main():
    test_hier_meas()

def test_hier_meas():
    # load data from df
    dbotree_pickle = "/Users/isantana/Nextcloud/UPM/OEG/esTextAnalytics/testsnlp/dbotree.p"
    pred_res_path = "/Users/isantana/Nextcloud/UPM/OEG/esTextAnalytics/testsnlp/100l_pred_and_labels.csv"

    df_pred_label = fu.csv_to_df(pred_res_path)


    dbtree = pickle.load(open(dbotree_pickle, "rb"))
    logger.debug("unpickled dbtree from: %s" % (dbotree_pickle))

    general_accuracy, hier_prec, hier_recall, hier_f_meas = meas.get_hierarchical_measurements(df_pred_label,
                                                                                               COL_PREDICTIONS_NAME,
                                                                                               COL_LABELS_NAME, dbtree)

    logger.info("****  Results *****")
    logger.info("* General accuracy=%s" % general_accuracy)
    logger.info("* Hierachical precission=%s" % hier_prec)
    logger.info("* Hierachical recall=%s" % hier_recall)
    logger.info("* Hierachical F-measure=%s" % hier_f_meas)

def pickle_dbo_tree():
    """
    # Entry method of the Testing methods
    """
    logger.info("Starting tests")

    calculate = False
    dbotree_pickle = "/Users/isantana/Nextcloud/UPM/OEG/esTextAnalytics/dbotree.p"

    if calculate:
        ontofile = "/Users/isantana/Nextcloud/UPM/OEG/esTextAnalytics/opencorporates/files/dbpedia_2016-10.owl"

        dbotypes = dbo.OntoTypes()
        dbotypes.get_subclassesof_tree(ontofile)

        pickle.dump(dbotypes.tree, open(dbotree_pickle, "wb"))

    pdbt = pickle.load(open(dbotree_pickle, "rb"))

    pdbt.show()
    logger.info("Tree depth=%s" % pdbt.depth())

    orgClass = rdflib.term.URIRef("http://dbpedia.org/ontology/BoxingCategory")

    logger.info("Level of boxingcategory=%s" % pdbt.level(orgClass))
    logger.info("Path to boxingcategory")
    for p in pdbt.rsearch(orgClass):
        logger.info(p)

    logger.info("End of tests")


# change this to file config
if __name__ == '__main__':
    import logging.config

    logging.basicConfig(filename='/Users/isantana/Nextcloud/UPM/OEG/esTextAnalytics/log_tests.log', format='%(asctime)s %(levelname)s %(message)s', level=logger.DEBUG)
    main()