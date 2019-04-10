import argparse

# from https://docs.python.org/3/howto/argparse.html

class Args:
    parser = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='NLP4Types TOpics parser.')


        # path args
        self.parser.add_argument("--upath", help="Path to data that should not be seen during training" , required=True)
        self.parser.add_argument("--uprefix", help="Prefix for unseen data, used for abstracts" , required=False)
        self.parser.add_argument("--dbtree", help="Path to the ontology tree pre-calculated", required=False)
        self.parser.add_argument("--log", help="Log file", default="./log_topics_nlp4types.log")


    def get_args(self):
        return self.parser.parse_args()

