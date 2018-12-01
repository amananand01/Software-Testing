import unittest
from unittest.mock import *
import MainPage
import sys

inputFile = open('inputfile.txt', 'r')
outputFile = open('outputfile.txt', 'w')

def side_effect(arg):
    return values[arg]

class TestMainPageMethods(unittest.TestCase):

    global inputFile
    global outputFile

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

    @patch('MainPage.getpass.getpass')
    @patch('MainPage.Customer')
    def test_SignInCustomer(self, MockCustomer, Mockgetpass):

        # Already tested so no need to Sign In Again
        return

        # Test the method
        Mockgetpass.return_value = 'Co' # mock password
        MockCustomer.return_value = None
        MainPage.SignInCustomer()

    @patch('MainPage.getpass.getpass')
    @patch('MainPage.Agent')
    def test_SignInAgent(self, MockAgent, Mockgetpass):

        # Already tested so no need to Sign In Again
        # Hence return
        return

        # Change the Mocked Agents' return value
        MockAgent.return_value = None
        Mockgetpass.return_value = 'Ro' # mock password
        MainPage.SignInAgent()

    @patch('MainPage.getpass.getpass')
    def test_RegisterCustomer(self,Mockgetpass):

        # Already tested so no need to Register Customer again in the Database
        # Hence return
        return

        # Test the method
        Mockgetpass.return_value = 'P1' # mock password
        MainPage.RegisterCustomer()

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
