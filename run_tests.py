import unittest
import sys
from tests.test_base import TestBase
from tests.test_cards import TestCards
from tests.test_media import TestMedia
from tests.test_interview import TestInterview

def run_tests():
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestBase))
    suite.addTest(unittest.makeSuite(TestCards))
    suite.addTest(unittest.makeSuite(TestMedia))
    suite.addTest(unittest.makeSuite(TestInterview))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 