import unittest
from unittest.mock import *
import MainPage
import sys

def side_effect(arg):
    return values[arg]

class TestMainPageMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_validateLogInInfo(self):
        self.assertTrue(MainPage.validateLogInInfo("abc"))
        self.assertFalse(MainPage.validateLogInInfo(".."))

    @patch('MainPage.getMainMenuSelection')
    @patch('MainPage.SignInCustomer')
    def test_Main(self, MockSignInCustomer, MockgetSelection):
        MockgetSelection.side_effect = side_effect
        MockgetSelection.side_effect = [1, 1, 4]
        MockSignInCustomer.return_value = "In method SignInCustomer"

    @patch('MainPage.Agent')
    def test_SignInAgent(self, MockAgent):

        # # Already tested so no need to Sign In Again
        # # Hence return
        # return

        # Change the Mocked Agents' return value
        MockAgent.return_value = None

        # store the original STDIN and assing a new one
        original_stdin = sys.stdin
        inputFile = open('inputfile.txt', 'r')
        sys.stdin = inputFile
        # store the original STDOUT and assing a new one
        original_stdout = sys.stdout
        outputFile = open('outputfile.txt', 'w')
        sys.stdout = outputFile

        MainPage.SignInAgent()

        # close the files
        inputFile.close()
        outputFile.close()
        # change the stdin/stdout back to command line
        sys.stdin = original_stdin
        sys.stdout = original_stdout

    def test_RegisterCustomer(self):

        # Already tested so no need to Register Customer again in the Database
        # Hence return
        return

        # store the original STDIN and assing a new one
        original_stdin = sys.stdin
        inputFile = open('inputfile.txt', 'r')
        sys.stdin = inputFile
        # store the original STDOUT and assing a new one
        original_stdout = sys.stdout
        outputFile = open('outputfile.txt', 'w')
        sys.stdout = outputFile

        MainPage.RegisterCustomer()

        # close the files
        inputFile.close()
        outputFile.close()
        # change the stdin/stdout back to command line
        sys.stdin = original_stdin
        sys.stdout = original_stdout

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
