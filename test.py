import unittest

# Make seperate classes depending on what particular features you want to test.
# Could also make multiple test files. This is just an example class I made, 
# feel free to remove or delete. Run the tests here via this command: 
# python -m unittest test.py
class TestMessageHandlingExample(unittest.TestCase): 
    # Expected JSON responses for the relevant events you want to handle for your feature can be 
    # found here: https://api.slack.com/events?filter=Events
    def setUp(self):
        self.payload = {}
    def test_function(self):
        self.payload = {"hi":"hi"}
        self.assertEqual(self.payload, {"hi":"hi"})

if __name__ == '__main__':
    unittest.main()