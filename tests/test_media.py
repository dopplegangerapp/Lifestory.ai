from tests.test_base import TestBase
import os
import tempfile
from datetime import datetime
from routes.media import allowed_file, get_media_type

class TestMedia(TestBase):
    def setUp(self):
        super().setUp()
        # Create a temporary directory for media uploads
        self.media_dir = tempfile.mkdtemp()
        with self.app.application.app_context():
            self.app.application.config['UPLOAD_FOLDER'] = self.media_dir
    
    def test_allowed_file(self):
        self.assertTrue(allowed_file('test.jpg'))
        self.assertTrue(allowed_file('test.png'))
        self.assertTrue(allowed_file('test.mp4'))
        self.assertTrue(allowed_file('test.mp3'))
        self.assertFalse(allowed_file('test.exe'))
        self.assertFalse(allowed_file('test.txt'))
    
    def test_get_media_type(self):
        self.assertEqual(get_media_type('test.jpg'), 'image')
        self.assertEqual(get_media_type('test.png'), 'image')
        self.assertEqual(get_media_type('test.mp4'), 'video')
        self.assertEqual(get_media_type('test.mp3'), 'audio')
        self.assertEqual(get_media_type('test.txt'), 'document')
    
    def test_media_upload(self):
        # Create a test file
        test_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_file.write(b'test data')
        test_file.seek(0)
        
        # Test file upload
        response = self.app.post('/media/upload',
                               data={'file': (test_file, 'test.jpg'),
                                    'description': 'Test image'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('file_path', data)
        self.assertIn('media_id', data)
        
        # Clean up
        test_file.close()
    
    def test_media_upload_invalid_file(self):
        # Test invalid file upload
        response = self.app.post('/media/upload',
                               data={'file': (tempfile.NamedTemporaryFile(suffix='.exe'), 'test.exe')})
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_media_upload_no_file(self):
        # Test upload without file
        response = self.app.post('/media/upload')
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_get_media(self):
        # First upload a file
        test_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_file.write(b'test data')
        test_file.seek(0)
        
        upload_response = self.app.post('/media/upload',
                                      data={'file': (test_file, 'test.jpg'),
                                           'description': 'Test image'})
        media_id = upload_response.get_json()['media_id']
        
        # Test getting media info
        response = self.app.get(f'/media/{media_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], media_id)
        self.assertEqual(data['description'], 'Test image')
        
        # Clean up
        test_file.close()
    
    def test_get_nonexistent_media(self):
        # Test getting non-existent media
        response = self.app.get('/media/999999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_generate_image(self):
        # Test image generation
        response = self.app.post('/media/generate_image',
                               json={'prompt': 'A beautiful sunset',
                                    'description': 'Generated sunset'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('image_url', data)
        self.assertIn('media_id', data)
    
    def test_generate_image_no_prompt(self):
        # Test image generation without prompt
        response = self.app.post('/media/generate_image',
                               json={'description': 'No prompt'})
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data) 