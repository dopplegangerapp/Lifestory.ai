
import unittest
from streamlit.testing.v1 import AppTest
import ui_components.interview as interview

class TestFrontendInterview(unittest.TestCase):
    def setUp(self):
        self.app = AppTest()
        
    def test_initial_state(self):
        """Test the initial state of the interview component"""
        interview.render()
        self.assertTrue(self.app.markdown[0].value.startswith('<div class="orb">'))
        self.assertTrue("Let's talk about your life" in self.app.markdown[1].value)
        
    def test_name_input(self):
        """Test the name input functionality"""
        interview.render()
        self.app.text_input[0].input("John Doe").run()
        self.assertEqual(self.app.text_input[0].value, "John Doe")
        
    def test_continue_button(self):
        """Test the continue button presence"""
        interview.render()
        self.assertTrue(any("CONTINUE" in btn.label for btn in self.app.button))

if __name__ == '__main__':
    unittest.main()
