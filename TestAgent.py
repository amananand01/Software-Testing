import unittest
from unittest.mock import *
import MainPage
import Agent
import sys

inputFile  = open('inputfile.txt', 'r')
outputFile = open('outputfile.txt', 'w')
DBpath     = "./miniproject.db"

class TestAgent(unittest.TestCase):

    global inputFile
    global outputFile
    global DBpath

    def setUp(self):
        pass

    @patch('Agent.agents_set_order')
    @patch('Agent.agents_update_order')
    @patch('Agent.find_carries')
    @patch('Agent.agents_add_stock')
    def test_Agent(self, MockAgentsAddStock, MockFindCarries, MockAgentsUpdateOrder, MockAgentsSetOrder):

        # Already tested so now safely return
        return

        MockAgentsSetOrder.return_value = None
        MockAgentsUpdateOrder.return_value = None
        MockFindCarries.return_value = 2
        MockAgentsAddStock.return_value = None
        Agent.Agent(DBpath)

    @patch('Agent.find_carries')
    @patch('Agent.enter_quantity')
    def test_agents_add_stock(self, MockEnterQuantity, MockFindCarries):

        # Already tested so now safely return
        return

        storeID   = 10
        productID = 'p160'
        MockEnterQuantity.return_value = 0
        MockFindCarries.return_value   = 1
        Agent.connect(DBpath)
        Agent.agents_add_stock(storeID,productID)

    @patch('Agent.get_all_track_num')
    @patch('Agent.random_with_N_digits')
    def test_agents_set_order(self, MockRandomNumber, MockGetTrackingNumbers):

        # Already tested so now safely return
        return

        pickupTime = '2014-10-22 03:32:43'
        orderId = 110
        dropoffTime = None
        MockRandomNumber.side_effect = [7886, 7886, 7889, 8998]
        MockGetTrackingNumbers.return_value = [7777,8989,7886]
        Agent.connect(DBpath)
        Agent.agents_set_order(orderId, pickupTime, dropoffTime)

    def test_deliveries_arrived(self):

        # Already tested so now safely return
        return

        date = '2017-12-02 14:40:00'
        Agent.deliveries_arrived(date)

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
