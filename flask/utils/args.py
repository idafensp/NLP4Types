import argparse

# from https://docs.python.org/3/howto/argparse.html

class Args:
    parser = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='NLP4Types Flask Server parser.')

        # boolean args
        self.parser.add_argument('--ner', help='Use NER types from spotlight', action="store_true")
        self.parser.add_argument('--stemm', help='Use stemming', action="store_true")
        self.parser.add_argument('--lemma', help='Use lemmatizing', action="store_true")
        self.parser.add_argument('--sw', help='Use stopwords', action="store_true")
        self.parser.add_argument('--dbonly', help='Use only dbo types', action="store_true")

        # path args
        self.parser.add_argument("--log", help="Log file", default="./log_flask_nlp4types.log")
        self.parser.add_argument("--classifier", help="Classifier for Flask UI", default="./flask_classifier.p")
        self.parser.add_argument("--vect", help="Vectorizer file for Flask UI", default="./flask_vectorizer.p")

        # string args
        self.parser.add_argument("--model", help="Name of the model", default="not_defined")
        self.parser.add_argument("--collection", help="Name of the collection for feedback", default="feedback")

        # num args
        self.parser.add_argument("--confidence", help="Conficence for NE at spotlight, default 0.3", type=float, default=0.3)
        self.parser.add_argument("--support", help="Support for NE at spotlight, default 0", type=int, default=0)


    def get_args(self):
        return self.parser.parse_args()

