# WIKIPEDIA

import logging
logger = logging.getLogger(__name__)


def get_entries_missing_infoboxes():
    """
    Get all the entries in a Wikipedia version missing infoboxes
    :return: Returns a dataframe with
        - id
        - URL of the entry
        - HTML content
        - Abstract
    """
    logger.debug("Starting get_missing_infoboxes")