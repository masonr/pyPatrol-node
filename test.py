from app import app
import json
import unittest

class UnitTests(unittest.TestCase):
	# Unit Tests for REST APIs

	def test_status(self):
		# Test pyPatrol node status json response
		# Expected result: status = online
		request, response = app.test_client.get('/status')
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')

	def test_ping(self):
		# Test real IPv4 address (Google DNS)
		# Expected result: status = online
		params = {'ip': '8.8.8.8'}
		request, response = app.test_client.post('/ping', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')

		# Test a bad IPv4 address (no existant local network)
		# Expected result: status = offline
		params = {'ip': '192.168.10.1'}
		request, response = app.test_client.post('/ping', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'offline')
		
		# Test an IPv6 address
		# Expected result: status = error
		params = {'ip': 'ipv6.google.com'}
		request, response = app.test_client.post('/ping', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'error')

	def test_ping6(self):
		# Test real IPv6 address (Google DNS)
		# Expected result: status = online
		params = {'ip': '2001:4860:4860::8888'}
		request, response = app.test_client.post('/ping6', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')

		# Test a bad IPv6 address (blackhole)
		# Expected result: status = offline
		params = {'ip': '100::'}
		request, response = app.test_client.post('/ping6', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'offline')

		# Test real IPv6 hostname (Google)
		# Expected result: status = online
		params = {'ip': 'ipv6.google.com'}
		request, response = app.test_client.post('/ping6', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')

		# Test an IPv4 address
		# Expected result: status = error
		params = {'ip': '8.8.8.8'}
		request, response = app.test_client.post('/ping6', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'error')

if __name__ == '__main__':
	unittest.main()
