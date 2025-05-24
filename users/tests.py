from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from .models import User

# Create your tests here.

class CSVUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/users/upload/'
        
        # Create a test CSV file
        self.valid_csv_content = b'name,email,age\nJohn Doe,john@example.com,30\nJane Smith,jane@example.com,25'
        self.invalid_csv_content = b'name,email,age\n,invalid-email,150\nJohn Doe,john@example.com,abc'

    def test_valid_csv_upload(self):
        csv_file = SimpleUploadedFile('test.csv', self.valid_csv_content, content_type='text/csv')
        response = self.client.post(self.url, {'file': csv_file})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_records'], 2)
        self.assertEqual(response.json()['successful_records'], 2)
        self.assertEqual(response.json()['failed_records'], 0)
        self.assertEqual(len(response.json()['errors']), 0)

    def test_invalid_csv_upload(self):
        csv_file = SimpleUploadedFile('test.csv', self.invalid_csv_content, content_type='text/csv')
        response = self.client.post(self.url, {'file': csv_file})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_records'], 2)
        self.assertEqual(response.json()['successful_records'], 0)
        self.assertEqual(response.json()['failed_records'], 2)
        self.assertEqual(len(response.json()['errors']), 2)

    def test_duplicate_email(self):
        # First upload
        csv_file1 = SimpleUploadedFile('test1.csv', self.valid_csv_content, content_type='text/csv')
        self.client.post(self.url, {'file': csv_file1})
        
        # Second upload with same email
        csv_file2 = SimpleUploadedFile('test2.csv', self.valid_csv_content, content_type='text/csv')
        response = self.client.post(self.url, {'file': csv_file2})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_records'], 2)
        self.assertEqual(response.json()['successful_records'], 0)
        self.assertEqual(response.json()['failed_records'], 2)
        self.assertEqual(len(response.json()['errors']), 2)

    def test_non_csv_file(self):
        file = SimpleUploadedFile('test.txt', b'not a csv file', content_type='text/plain')
        response = self.client.post(self.url, {'file': file})
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Only CSV files are allowed')
