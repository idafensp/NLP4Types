import logging
logger = logging.getLogger(__name__)


def to_string(list, sep=" "):
    proc_list = [w.upper().replace(":","_") for w in list]
    return sep.join(proc_list)
