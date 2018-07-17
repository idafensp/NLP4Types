import pandas
from treelib import Tree
import rdflib
import stringutils as su

import logging
logger = logging.getLogger(__name__)


def get_hierarchical_measurements(df_pred_label, col_predictions_name, cols_labels_name, dbtree):
    pred_index = df_pred_label.columns.get_loc(col_predictions_name) + 1
    label_index = df_pred_label.columns.get_loc(cols_labels_name) + 1

    hits = 0
    hprec_num = 0.0
    hprec_den = 0.0

    hrec_num = 0.0
    hrec_den = 0.0

    df_pred_label[col_predictions_name] = df_pred_label[col_predictions_name].apply(su.remove_ducks)
    df_pred_label[cols_labels_name] = df_pred_label[cols_labels_name].apply(su.remove_ducks)

    for tup in df_pred_label.itertuples():

        prec = tup[pred_index]
        labc = tup[label_index]

        print("prec=%s" % prec)
        print("labc=%s" % labc)

        if prec == labc:
            hits += 1

        prec_class = rdflib.term.URIRef(prec)

        try:
            prec_path = [p for p in dbtree.rsearch(prec_class)]
        except:
            logger.error("Issue parsing prediction URI: %s" % prec_class)
            continue

        labc_class = rdflib.term.URIRef(labc)

        try:
            labc_path = [p for p in dbtree.rsearch(labc_class)]
        except:
            logger.error("Issue parsing label URI: %s" % labc_class)
            continue

        # get intersection between predictions and labels paths
        hprec_num = hprec_num + len(list(set(prec_path) & set(labc_path)))
        hrec_num = hrec_num + len(list(set(prec_path) & set(labc_path)))

        hprec_den = hprec_den + len(prec_path)
        hrec_den = hrec_den + len(labc_path)

    print("Hits=%s" % hits)
    print("hprec_num=%s" % hprec_num)
    print("hprec_den=%s" % hprec_den)
    print("hrec_num=%s" % hrec_num)
    print("hrec_den=%s" % hrec_den)


    general_accuracy = float(hits) / len(df_pred_label)
    hier_prec = hprec_num / float(hprec_den)
    hier_recall = hrec_num / float(hrec_den)
    hier_f_meas = (2 * hier_prec * hier_recall) / (hier_prec + hier_recall)

    logger.debug("Hits=%s, errors=%s" % (hits, len(df_pred_label) - hits))

    return general_accuracy, hier_prec, hier_recall, hier_f_meas

