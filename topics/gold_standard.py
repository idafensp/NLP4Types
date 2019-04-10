import logging as logger
import args as uarg
import filesutils as fu
import librairy as lib



def main():
    """
    # Entry method of the NLP4Types method
    """
    logger.info("Starting Topics @ NLP 4 Types")

    data_path = args.upath

    df_data = fu.csv_to_df(data_path)

    col_abs_index = 3
    col_type_index = 2
    col_ind_index = 1

    lib_service = lib.Librairy()

    for (index, tup) in enumerate(df_data.itertuples()):

        if index % 10 == 0:
            logger.debug("Preprocessed %s/%s" % (index, len(df_data)))

        abstract = tup[col_abs_index]
        type = tup[col_type_index]
        individual = tup[col_ind_index]

        logger.debug("Reading %s, %s\n --------\n %s" % (individual, type, abstract))

        topics = lib_service.get_annotations(abstract,True)

        logger.debug("Topics %s" % (topics))



# change this to file config
if __name__ == '__main__':
    import logging.config

    ps = uarg.Args()
    args = ps.get_args()


    logfile='log_topics_n4t.log'
    if args.log:
        logfile = args.log


    logging.basicConfig(filename=logfile, format='%(asctime)s %(levelname)s %(message)s',
                        level=logger.DEBUG)


    logger.info("Arguments %s" % args)

    main()



