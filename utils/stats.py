import logging
logger = logging.getLogger(__name__)


def save_to_file(file, list1, list2):
    logger.info("Writing %s/%s lines to file %s" % (len(list1), len(list2), file))

    thefile = open(file, 'w')

    for i in range(0, len(list1)):
        thefile.write("%s, %s\n" % (list1[i], list2[i]))


def column_count(df, col):
    logger.debug("Got %s entries from DF" % len(df))

    indexes = df[col].value_counts().index.tolist()
    values = df[col].value_counts().values.tolist()

    save_to_file(col+"_count_stats.txt", indexes, values)
