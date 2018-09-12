# SPOTLIGHT
# https://github.com/dbpedia-spotlight/dbpedia-spotlighthttps://github.com/dbpedia-spotlight/dbpedia-spotlight
import requests
from requests.utils import quote
import json

import logging
logger = logging.getLogger(__name__)


class SpotLightNER:

    def __init__(self, asu="http://localhost:2222/rest/annotate/"):
        self.annotate_service_url = asu

    def get_nes(self, text):
        """
        :param text: text from wikipedia/dbpedia abstract, to obtain NEs from
        :return: a list of NE
        """



    def get_annotations(self, text, confidence=0.0, support=0, dboonly=True, leaftypes=False):

        logger.debug("Get_annotations for confidence=%s, support=%s, text=%s" % (confidence, support, text))

        #create empty list for returning NE types
        return_list = []

        #request header and parameters
        headerinfo = {'Accept': 'application/json'}
        parameters = {'text': text, 'confidence': confidence, 'support': support}

        try:
            resp = requests.post(self.annotate_service_url, data=parameters, headers=headerinfo)
        except:
            logger.error("Failed requesting URL for request url=%s" % (self.annotate_service_url))
            return []

        if resp.status_code != 200:
            # This means something went wrong.
            logger.error("Failed requesting URL for request url=%s, wrong code=%s" % (resp.url, resp.status_code))
            return []
        else:
            logger.debug("Got results: %s" % resp.text)
            decoded = json.loads(resp.text)

            if 'Resources' in decoded:
                for dec in decoded['Resources']:
                    return_list += dec['@types'].split(",")

        if(dboonly):
            return_list = [t for t in return_list if "DBpedia:" in t]

        if(leaftypes):
            #TODO: pending, this will require a dictionary of types and hierarchy
            #TODO: this should probabily moved to the loop (for dec), to ensure one path at a time
            logger.warn("TODO: Checking leaftypes still pending")


        return return_list