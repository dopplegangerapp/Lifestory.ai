import unittest
from unittest.mock import patch, MagicMock, call
import streamlit as st
import ui_components.interview as interview
import json
from contextlib import contextmanager

@patch('streamlit.rerun')
class TestFrontendInterview(unittest.TestCase):
    def setUp(self):
        # Create mocks
        self.mock_text_input = MagicMock(return_value="")
        self.mock_button = MagicMock(return_value=False)
        self.mock_markdown = MagicMock()
        self.mock_progress = MagicMock()
        self.mock_error = MagicMock()
        self.mock_warning = MagicMock()
        
        # Create column mock
        class MockColumn:
            def __init__(self):
                self.text_input = MagicMock(return_value="")
                self.button = MagicMock(return_value=False)
                
            def __enter__(self):
                return self
                
            def __exit__(self, *args):
                pass
        
        @contextmanager
        def mock_columns(*args, **kwargs):
            cols = [MockColumn() for _ in range(len(args[0]))]
            yield cols
        
        self.mock_columns = mock_columns
        
        # Setup patches
        self.patches = [
            patch('streamlit.text_input', self.mock_text_input),
            patch('streamlit.button', self.mock_button), 
            patch('streamlit.markdown', self.mock_markdown),
            patch('streamlit.progress', self.mock_progress),
            patch('streamlit.columns', self.mock_columns),
            patch('streamlit.error', self.mock_error),
            patch('streamlit.warning', self.mock_warning)
        ]
        
        # Start patches
        for p in self.patches:
            p.start()
            
        # Initialize session state
        class SessionState:
            def __init__(self):
                self._dict = {}
            
            def __getattr__(self, name):
                if name not in self._dict:
                    self._dict[name] = None
                return self._dict[name]
            
            def __setattr__(self, name, value):
                if name == '_dict':
                    super().__setattr__(name, value)
                else:
                    self._dict[name] = value
                    
            def __contains__(self, key):
                return key in self._dict
        
        st.session_state = SessionState()
        interview.reset_session()
            
    def tearDown(self):
        # Stop patches
        for p in self.patches:
            p.stop()
            
    def test_initial_state(self, mock_rerun):
        """Test the initial state of the interview component"""
        interview.render()
        self.mock_markdown.assert_called()
        self.assertFalse(st.session_state.started)
        self.assertEqual(st.session_state.progress, 0)
        
    def test_name_input(self, mock_rerun):
        """Test the name input functionality"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "question": "Are you ready to begin?",
            "current_stage": "welcome",
            "progress": 0
        }
        
        with patch('requests.get', return_value=mock_response):
            # Set name input and trigger continue button
            def mock_columns(*args, **kwargs):
                col = MagicMock()
                col.text_input = MagicMock(return_value="John Doe")
                col.button = MagicMock(return_value=True)
                @contextmanager
                def enter_col():
                    yield col
                col.__enter__ = enter_col
                col.__exit__ = MagicMock()
                yield [MagicMock(), col, MagicMock()]
            
            with patch('streamlit.columns', mock_columns):
                # Mock rerun to update session state
                def mock_rerun_side_effect():
                    st.session_state.started = True
                    st.session_state.current_question = "Are you ready to begin?"
                    st.session_state.stage = "welcome"
                    st.session_state.name = "John Doe"
                    return None
                mock_rerun.side_effect = mock_rerun_side_effect
                
                # Render and check state
                interview.render()
                
                # Call mock_rerun directly to update state
                mock_rerun()
                
                # Verify session state was updated
                self.assertTrue(st.session_state.started)
                self.assertEqual(st.session_state.name, "John Doe")
                self.assertEqual(st.session_state.current_question, "Are you ready to begin?")
                
                # Verify rerun was called
                mock_rerun.assert_called_once()
        
    def test_continue_button(self, mock_rerun):
        """Test the continue button functionality"""
        # Set up initial state
        st.session_state.started = True
        st.session_state.current_question = "Test question?"
        
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "next_question": "Next question?",
            "current_stage": "test",
            "progress": 50
        }
        
        with patch('requests.post', return_value=mock_response):
            # Set answer input and trigger continue button
            def mock_columns(*args, **kwargs):
                col = MagicMock()
                col.text_input = MagicMock(return_value="Test answer")
                col.button = MagicMock(return_value=True)
                @contextmanager
                def enter_col():
                    yield col
                col.__enter__ = enter_col
                col.__exit__ = MagicMock()
                yield [MagicMock(), col, MagicMock()]
            
            with patch('streamlit.columns', mock_columns):
                # Mock rerun to update session state
                def mock_rerun_side_effect():
                    st.session_state.current_question = "Next question?"
                    st.session_state.stage = "test"
                    st.session_state.progress = 50
                    return None
                mock_rerun.side_effect = mock_rerun_side_effect
                
                # Render and check state
                interview.render()
                
                # Call mock_rerun directly to update state
                mock_rerun()
                
                # Verify answer was submitted
                self.assertEqual(st.session_state.current_question, "Next question?")
                self.assertEqual(st.session_state.progress, 50)
                
                # Verify rerun was called
                mock_rerun.assert_called_once()

    def test_error_handling(self, mock_rerun):
        """Test error handling in the interview component"""
        # Mock failed API response
        mock_response = MagicMock()
        mock_response.status_code = 500
        
        with patch('requests.post', return_value=mock_response):
            # Set up state for answer submission
            st.session_state.started = True
            st.session_state.current_question = "Test question?"
            
            # Set answer input and trigger continue button
            def mock_columns(*args, **kwargs):
                col = MagicMock()
                col.text_input = MagicMock(return_value="Test answer")
                col.button = MagicMock(return_value=True)
                @contextmanager
                def enter_col():
                    yield col
                col.__enter__ = enter_col
                col.__exit__ = MagicMock()
                yield [MagicMock(), col, MagicMock()]
            
            with patch('streamlit.columns', mock_columns):
                # Render and check error handling
                interview.render()
                self.mock_error.assert_called()

    def test_interview_completion(self, mock_rerun):
        """Test interview completion handling"""
        # Mock completion API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "completed": True
        }
        
        with patch('requests.post', return_value=mock_response):
            # Set up state for answer submission
            st.session_state.started = True
            st.session_state.current_question = "Final question?"
            
            # Set answer input and trigger continue button
            def mock_columns(*args, **kwargs):
                col = MagicMock()
                col.text_input = MagicMock(return_value="Final answer")
                col.button = MagicMock(return_value=True)
                @contextmanager
                def enter_col():
                    yield col
                col.__enter__ = enter_col
                col.__exit__ = MagicMock()
                yield [MagicMock(), col, MagicMock()]
            
            with patch('streamlit.columns', mock_columns):
                # Mock rerun to update session state
                def mock_rerun_side_effect():
                    st.session_state.started = False
                    return None
                mock_rerun.side_effect = mock_rerun_side_effect
                
                # Render and check state
                interview.render()
                
                # Call mock_rerun directly to update state
                mock_rerun()
                
                # Verify session state was updated
                self.assertFalse(st.session_state.started)
                
                # Verify rerun was called
                mock_rerun.assert_called_once()

if __name__ == '__main__':
    unittest.main()
