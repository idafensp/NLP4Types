import re
import urllib

import logging
logger = logging.getLogger(__name__)


def to_string(list, sep=" "):
    proc_list = [w.upper().replace(":","_") for w in list]
    return sep.join(proc_list)


def remove_ducks(uri):
    return re.sub("<|>", "", uri)

def encode_url(url):
    #remove the < and >
    inter = url[1:-1]

    #encode
    inter = urllib.quote(inter, "/,")

    #chech the : at the beggining
    inter = inter.replace("http%3A", "http:")

    return "<"+inter+">"
