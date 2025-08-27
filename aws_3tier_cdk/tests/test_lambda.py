import unittest
from unittest.mock import patch, MagicMock
import io
import json
from PIL import Image

from aws_3tier_cdk.lambdas import image_processor as ip

class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        # Create an in-memory image for testing
        self.img = Image.new('RGB', (100, 100), color='blue')
        self.buf = io.BytesIO()
        self.img.save(self.buf, format='JPEG')
        self.buf.seek(0)

    @patch('aws_3tier_cdk.lambdas.image_processor.s3')
    def test_handler(self, mock_s3):
        # Mock S3 get_object to return our in-memory image
        mock_s3.get_object.return_value = {'Body': self.buf}

        # Example Lambda event
        event = {'bucket': 'dummy-bucket', 'key': 'sample.jpg'}

        # Call handler
        response = ip.handler(event, None)

        # Parse JSON body
        body = json.loads(response['body'])

        # Assertions for keys
        self.assertIn('original_key', body)
        self.assertIn('resized_key', body)
        self.assertIn('thumbnail_key', body)
        self.assertIn('metadata', body)

        # Assertions for metadata
        metadata = body['metadata']
        self.assertIn('jfif', metadata)
        self.assertIn('jfif_version', metadata)
        self.assertIn('jfif_unit', metadata)
        self.assertIn('jfif_density', metadata)


if __name__ == '__main__':
    unittest.main()
