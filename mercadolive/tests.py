from django.test import TestCase
from unittest import mock
from .services import request
import json

class MeliTestCase(TestCase):
    
    @mock.patch('mercadolive.services.request')
    # @patch.object(request, 'ook', Mock(return_value=None))
    def test_request(self, mock_get):
        # with patch('mercadolive.services.request') as mock_get:
        mock_response = mock.Mock()
        expected_dict = json.dumps({'site_id': 'MLA'})
        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # mock_get.return_value.status_code = 200
        # mock_get.return_value.json.return_value = fake_json

        # Define response for the fake API
        mock_get.return_value = mock_response

        response = request()
        print("text: ", response.json())
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_dict)