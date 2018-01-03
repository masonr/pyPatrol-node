from app import app
import json
import unittest

class UnitTests(unittest.TestCase):
	# Unit Tests for REST APIs

	def test_status(self):
		request, response = app.test_client.get('/status')
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')

	def test_ping(self):
		params = {'ip': '8.8.8.8'}
		request, response = app.test_client.post('/ping', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')
		

if __name__ == '__main__':
	unittest.main()
