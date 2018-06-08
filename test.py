import logging as logger
import utils.spotlight as sl

def main():
    """
    # Entry method of the Testing methods
    """
    logger.info("Starting tests")

    slservice = sl.SpotLightNER()

    ne_types = slservice.get_annotations("Barack Obama hates Donald Trump while in Gran Canaria and Tenerife", 0.2, 0, True, True)

    print(ne_types)

    logger.info("End of tests")


# change this to file config
if __name__ == '__main__':
    import logging.config

    logging.basicConfig(filename='log_tests.log', format='%(asctime)s %(levelname)s %(message)s', level=logger.DEBUG)
    main()