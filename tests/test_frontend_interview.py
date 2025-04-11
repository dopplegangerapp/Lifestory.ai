
import unittest
import os
from streamlit.testing.v1 import AppTest
import ui_components.interview as interview

class TestFrontendInterview(unittest.TestCase):
    def setUp(self):
        self.app = AppTest(os.path.join(os.path.dirname(__file__), '../app.py'))
        
    def test_initial_state(self):
        """Test the initial state of the interview component"""
        interview.render()
        self.assertTrue(any("orb" in str(widget.markdown) for widget in self.app.markdown))
        self.assertTrue(any("Let's talk about your life" in str(widget.markdown) for widget in self.app.markdown))
        
    def test_name_input(self):
        """Test the name input functionality"""
        interview.render()
        name_input = self.app.text_input[0]
        name_input.input("John Doe").run()
        self.assertEqual(name_input.value, "John Doe")
        
    def test_continue_button(self):
        """Test the continue button presence"""
        interview.render()
        continue_buttons = [btn for btn in self.app.button if "CONTINUE" in btn.label]
        self.assertTrue(len(continue_buttons) > 0)

if __name__ == '__main__':
    unittest.main()
