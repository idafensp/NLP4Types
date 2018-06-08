import argparse

# from https://docs.python.org/3/howto/argparse.html

class Args:
    parser = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='NLP4Types parser.')

        # boolean args
        self.parser.add_argument('--stemm', help='Use stemming', action="store_true")
        self.parser.add_argument('--dbonly', help='Use only dbo types', action="store_true")
        self.parser.add_argument('--abstract', help='Use abstract text', action="store_true")
        self.parser.add_argument('--ner', help='Use NER types from spotlight', action="store_true")
        self.parser.add_argument('--stats', help='Generate stats of types', action="store_true")

        # num args

        self.parser.add_argument("--neweight", help="Weight for the NE types, default 1", type=int, default=1)
        self.parser.add_argument("--fstep", help="First step of the pipeline, default 0", type=int, default=0)
        self.parser.add_argument("--lstep", help="Last step of the pipeline, default = 100", type=int, default=100)
        self.parser.add_argument("--support", help="Support for NE at spotlight, default 0", type=int, default=0)
        self.parser.add_argument("--confidence", help="Conficence for NE at spotlight, default 0.3", type=float, default=0.3)
        self.parser.add_argument("--tsize", help="Training set size proportion [0-1], default 0.9", type=float, default=0.9)


    def get_args(self):
        return self.parser.parse_args()

