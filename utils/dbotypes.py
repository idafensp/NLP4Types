# DBOTYPES
import rdflib
from treelib import Node, Tree

import logging
logger = logging.getLogger(__name__)

# http://treelib.readthedocs.io/en/latest/pyapi.html

class OntoTypes:

    def __init__(self, tcu="http://www.w3.org/2002/07/owl#Thing"):
        self.top_class_uri = tcu
        self.tree = Tree()

    # TODO
    def get_dbo_type_levels_dict(self, path, top_class_uri):

        logger.info("Starting get_dbo_types_dict from %s, topclass=%s" % (path, top_class_uri))
        # http://rdflib.readthedocs.io/en/stable/intro_to_sparql.html
        g = rdflib.Graph()

        # ... add some triples to g somehow ...

        g.parse(path)

        orgClass = rdflib.term.URIRef(top_class_uri)

        class_list = [orgClass]

        stack = [orgClass]
        while stack:
            currentClass = stack.pop()
            logger.debug("Current class %s" % currentClass)

            subclasses = [s for s, p, o in g if p == rdflib.RDFS.subClassOf and o == currentClass]
            if subclasses:
                stack = stack + subclasses
                class_list = class_list + subclasses
            # print(subclasses)

        class_list = set(class_list)
        return class_list


    # get all parent types from a given one
    def get_subclassesof_tree(self, ifile):
        # http://rdflib.readthedocs.io/en/stable/intro_to_sparql.html
        g = rdflib.Graph()
        g.parse(ifile)


        orgClass = rdflib.term.URIRef(self.top_class_uri)
        stack  = [orgClass]

        self.tree.create_node(orgClass,orgClass)
        while stack:
            currentClass = stack.pop()
            logger.debug("Current class %s" % currentClass)
            subclasses = [s for s, p, o in g if p == rdflib.RDFS.subClassOf and o == currentClass]
            logger.debug("Subclasses: %s" % subclasses)
            if subclasses:
                stack  =  stack + subclasses

                for sc in subclasses:
                    if not self.tree.contains(sc):
                        self.tree.create_node(sc, sc, parent=currentClass)
                    else:
                        sc_bis =  str(sc) + "_bis"
                        self.tree.create_node(sc_bis, sc_bis, parent=currentClass)