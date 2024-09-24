import unittest
from unittest.mock import patch, Mock
from io import BytesIO
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.file_service import FileService

class TestFileService(unittest.TestCase):
    def setUp(self):
        self.file_service = FileService()

    @patch('app.services.file_service.s3')
    async def test_upload_file(self, mock_s3):
        # Create a mock file object
        mock_file = Mock()
        mock_file.filename = 'test.csv'
        mock_file.file = BytesIO(b'test_content')

        # Call the upload_file method
        file_key = await self.file_service.upload_file(mock_file)

        # Assert that the upload_fileobj method of the s3 client was called
        mock_s3.upload_fileobj.assert_called_once()

        # Assert that the file key has the expected format
        self.assertRegex(file_key, r'^preview/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\.csv$')

    @patch('app.services.file_service.s3')
    @patch('app.services.file_service.pd.read_csv')
    async def test_preview_file(self, mock_read_csv, mock_s3):
        # Mock the S3 get_object response
        mock_s3_obj = {'Body': BytesIO(b'col1,col2\nvalue1,value2\nvalue3,value4')}
        mock_s3.get_object.return_value = mock_s3_obj

        # Mock the pandas DataFrame
        mock_df = pd.DataFrame({'col1': ['value1', 'value3'], 'col2': ['value2', 'value4']})
        mock_read_csv.return_value = mock_df

        # Call the preview_file method
        preview_data = await self.file_service.preview_file('test_key')

        # Assert that the get_object method of the s3 client was called
        mock_s3.get_object.assert_called_once_with(Bucket='XXXXXXXXXXXXXXXX', Key='test_key')

        # Assert that the read_csv method of pandas was called with the correct arguments
        mock_read_csv.assert_called_once_with(mock_s3_obj['Body'], nrows=10)

        # Assert that the preview_data matches the expected DataFrame
        self.assertTrue(preview_data.equals(mock_df))
    

    """unit test for upload file that is not csv, which should fail"""
    @patch('app.services.file_service.s3')
    async def test_upload_file_not_csv(self, mock_s3):
        # Create a mock file object
        mock_file = Mock()
        mock_file.filename = 'test.txt'
        mock_file.file = BytesIO(b'test_content')

        # Call the upload_file method
        with self.assertRaises(ValueError):
            await self.file_service.upload_file(mock_file)

        # Assert that the upload_fileobj method of the s3 client was not called
        mock_s3.upload_fileobj.assert_not_called()

    """unit test for preview file that is not csv, which should fail"""
if __name__ == '__main__':
    unittest.main()
