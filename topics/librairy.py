# SPOTLIGHT
# https://github.com/dbpedia-spotlight/dbpedia-spotlighthttps://github.com/dbpedia-spotlight/dbpedia-spotlight
import requests
from requests.utils import quote
import json

import logging
logger = logging.getLogger(__name__)


class Librairy:

    def __init__(self, asu="http://librairy.linkeddata.es/dbpedia-model/inferences"):
        self.annotate_service_url = asu



    def get_annotations(self, text, topics=False):

        logger.debug("Get_annotations")

        #create empty list for returning NE types
        return_list = []

        #request header and parameters
        headerinfo = {'Accept': 'application/json', 'Content-Type' : 'application/json'}


        parameters = {'text': text, 'topics': topics}
        #parameters = str(parameters)

        try:
            resp = requests.post(self.annotate_service_url, data=parameters, headers=headerinfo)
        except:
            logger.error("Failed requesting URL for request url=%s, json=%s" % (self.annotate_service_url, parameters))
            return []

        if resp.status_code != 200:
            # This means something went wrong.
            logger.error("Failed requesting URL for request url=%s, wrong code=%s, json=%s" % (resp.url, resp.status_code,parameters))
            return []
        else:
            logger.debug("Got results: %s" % resp.text)
            decoded = json.loads(resp.text)

            #if 'Resources' in decoded:
            #    for dec in decoded['Resources']:
            #       return_list += dec['@types'].split(",")



        return return_list