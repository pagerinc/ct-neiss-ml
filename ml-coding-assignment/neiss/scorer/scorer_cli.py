#########
# A command line interface for using the scorer object
#########

import argparse
from scorer import Scorer

def usage():
    """
    Prints out intended usage of CLI
    :return: None
    """

    print 'scorer_cli.py [(optional) -p] [(opt) path to pickled model] [' ### TODO: finish

def get_parser():
    parser = argparse.ArgumentParser(description='Parameterize scorer run')

    parser.add_argument('-p', help='explicit path to pickled model to use', default=None)
    parser.add_argument()
    ### TODO: finish

if __name__ == '__main__':
    s = Scorer()


