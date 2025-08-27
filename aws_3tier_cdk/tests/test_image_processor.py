# aws_3tier_cdk/tests/test_image_processor.py
import unittest
from unittest.mock import patch, MagicMock
import image_processor

class TestImageProcessor(unittest.TestCase):

    @patch("image_processor.boto3_client")
    def test_valid_image(self, mock_client):
        mock_response = {'Body': MagicMock(read=lambda: b"fake image bytes")}
        mock_client.get_object.return_value = mock_response

        result = image_processor.download_image("mybucket", "image.jpg")
        self.assertEqual(result, b"fake image bytes")

    @patch("image_processor.boto3_client")
    def test_no_such_key(self, mock_client):
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Code': 'NoSuchKey'}}
        mock_client.get_object.side_effect = ClientError(error_response, "GetObject")

        with self.assertRaises(FileNotFoundError):
            image_processor.download_image("mybucket", "missing.jpg")

    @patch("image_processor.boto3_client")
    def test_access_denied(self, mock_client):
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Code': 'AccessDenied'}}
        mock_client.get_object.side_effect = ClientError(error_response, "GetObject")

        with self.assertRaises(PermissionError):
            image_processor.download_image("mybucket", "private.jpg")

    @patch("image_processor.boto3_client")
    def test_missing_bucket_or_key(self, mock_client):
        with self.assertRaises(ValueError):
            image_processor.download_image("", "image.jpg")
        with self.assertRaises(ValueError):
            image_processor.download_image("mybucket", "")

    @patch("image_processor.boto3_client")
    def test_invalid_image_data(self, mock_client):
        # Simulate S3 returning something invalid
        mock_response = {'Body': MagicMock(read=lambda: None)}
        mock_client.get_object.return_value = mock_response

        result = image_processor.download_image("mybucket", "image.jpg")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
