import pandas as pd
import filesutils as fu

import logging
logger = logging.getLogger(__name__)


def get_ne_dict(path, col_ind, col_ne):
    # there is an existing instane of NEs, lets reuse it
    logger.info("Reusing existing NEs, loading data from file %s" % path)
    df_rne = fu.csv_to_df(path)

    # convert to dictionary
    ne_dict = {}

    d_ind = df_rne.to_dict()[col_ind]
    d_ne = df_rne.to_dict()[col_ne]

    logger.debug("Converting to dictionary")

    for i in range(0, len(d_ind)):
        ne_dict[d_ind[i]] = d_ne[i]

    logger.debug("Loaded %s entries from file %s" % (len(ne_dict), path))

    return ne_dict

