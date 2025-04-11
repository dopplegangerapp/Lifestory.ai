
import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import ui_components.interview as interview

class TestFrontendInterview(unittest.TestCase):
    def setUp(self):
        # Create mocks
        self.mock_text_input = MagicMock(return_value="")
        self.mock_button = MagicMock(return_value=False)
        self.mock_markdown = MagicMock()
        
        # Setup patches
        self.patches = [
            patch('streamlit.text_input', self.mock_text_input),
            patch('streamlit.button', self.mock_button), 
            patch('streamlit.markdown', self.mock_markdown)
        ]
        
        # Start patches
        for p in self.patches:
            p.start()
            
        # Setup session state
        if not hasattr(st, 'session_state'):
            setattr(st, 'session_state', {})
            
    def tearDown(self):
        for p in self.patches:
            p.stop()
            
    def test_initial_state(self):
        """Test the initial state of the interview component"""
        interview.render()
        self.mock_markdown.assert_called()
        
    def test_name_input(self):
        """Test the name input functionality"""
        self.mock_text_input.return_value = "John Doe"
        interview.render()
        self.mock_text_input.assert_called()
        
    def test_continue_button(self):
        """Test the continue button functionality"""
        self.mock_button.return_value = True
        interview.render()
        self.mock_button.assert_called()

if __name__ == '__main__':
    unittest.main()
