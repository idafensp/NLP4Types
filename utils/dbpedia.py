# DBPEDIA
import rdflib
import pandas as pd
import stringutils as su

from SPARQLWrapper import SPARQLWrapper, JSON

import logging
logger = logging.getLogger(__name__)

OWL_THING = "<http://www.w3.org/2002/07/owl#Thing>"

def get_typed_resources(class_list, db_types_file):
    """
    Get all the entries in a Wikipedia version missing infoboxes
    :return: Returns a dataframe with
        - id
        - URI
        - Types
        - Abstract
        - Text
        - Categories
    """
    logger.debug("Starting get_typed_resources")
    logger.debug("Class list" + class_list)

    logger.debug("End of get_typed_resources")



def get_resources_from_types(class_list, db_types_file, remove_owl_thing = True, encode=False):
    logger.debug("Starting get_resources_from_types from %s" % (db_types_file))

    df_types = pd.read_csv(db_types_file, sep=' ', names = ["individual", "typeprop", "type", "dot"])
    logger.debug("Got %s instances from file %s" % (len(df_types),db_types_file))

    #this takes quite some time
    #duplicated_entries = df_types[df_types.duplicated(['individual'], keep=False)]
    #logger.debug("Got %s duplicated instances" % len(duplicated_entries))

    #remove unnecesary columnes (typeprop, dot)
    df_types=df_types.drop(columns=['typeprop', 'dot'])

    if remove_owl_thing:
        df_types = df_types[df_types.type != OWL_THING]

    if encode:
        # encode all individuals uris
        df_types['individual'] = df_types['individual'].apply(su.encode_url)

    return df_types

def get_resource_abstracts(class_list, abstracts_file, encode=False):
    logger.debug("Starting get_resource_abstracts from %s" % (abstracts_file))

    df_abstract = pd.read_csv(abstracts_file, sep=' ', names = ["individual", "abstractprop", "abstract", "dot"])


    logger.debug("Got %s instance abstracts from file %s" % (len(df_abstract),abstracts_file))

    #this takes quite some time
    #duplicated_entries = df_types[df_abstract.duplicated(['individual'], keep=False)]
    #logger.debug("Got %s duplicated instances" % len(duplicated_entries))

    #remove unnecesary columnes (typeprop, dot)
    df_abstract=df_abstract.drop(columns=['abstractprop', 'dot'])


    if encode:
        # encode all individuals uris
        df_abstract['individual'] = df_abstract['individual'].apply(su.encode_url)

    return df_abstract

