import unittest
from unittest.mock import *
import MainPage
import sys

inputFile = open('inputfile.txt', 'r')
outputFile = open('outputfile.txt', 'w')

class TestCustomer(unittest.TestCase):

    global inputFile
    global outputFile

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':

    # store the original STDIN and assing a new one
    original_stdin = sys.stdin
    sys.stdin = inputFile
    # store the original STDOUT and assing a new one
    original_stdout = sys.stdout
    sys.stdout = outputFile

    # Call the unit tests
    unittest.main()

    # close the files
    inputFile.close()
    outputFile.close()
    # change the stdin/stdout back to command line
    sys.stdin = original_stdin
    sys.stdout = original_stdout
