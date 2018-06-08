# FILE UTILS
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# TODO: check how to free mem from df after saving
def df_to_csv(file, df, sp='\t', enc='utf-8'):
    df.to_csv(file,  sep=sp, encoding=enc, index=False)


def csv_to_df(file_path, sp='\t', enc='utf-8'):
    return pd.read_csv(file_path, sep=sp, encoding=enc)


def save_to_file(file, list):
    logger.info("Writing %s lines to file %s" % (len(list), file))
    the_file = open(file, 'w')

    for item in list:
        the_file.write("%s\n" % item)


def join_dataframes(df1, df2):
    logger.info("Joining two dataframes, sizes %s  %s" % (len(df1), len(df2)))
    # https://pandas.pydata.org/pandas-docs/stable/merging.html
    # df_res = df1.set_index('individual').join(df2.set_index('individual'))

    # https://chrisalbon.com/python/data_wrangling/pandas_join_merge_dataframe/
    df_res = pd.merge(df1, df2, on='individual')
    return df_res
