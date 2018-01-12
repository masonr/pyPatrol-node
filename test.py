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

		# Test real IPv6 hostname (Google)
		# Expected result: status = online
		params = {'ip': 'google.com'}
		request, response = app.test_client.post('/ping', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')
		
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

	def test_cert(self):
		# Test a (hopefully) valid cert
		# Expected result: valid = true, reason = valid
		params = {'hostname': 'sha256.badssl.com', 'buffer': '14'}
		request, response = app.test_client.post('/cert', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['valid'], 'true')
		self.assertEqual(data['reason'], 'valid')

		# Test a (hopefully) valid cert that expires within threshold
		# Expected result: valid = true, reason = expires soon
		params = {'hostname': 'sha256.badssl.com', 'buffer': '10000'}
		request, response = app.test_client.post('/cert', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['valid'], 'true')
		self.assertEqual(data['reason'], 'expires soon')

		# Test an expired cert
		# Expected result: valid = false, reason = expired
		params = {'hostname': 'expired.badssl.com', 'buffer': '14'}
		request, response = app.test_client.post('/cert', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['valid'], 'false')
		self.assertEqual(data['reason'], 'expired')

		# Test an invalid domain
		# Expected result: valid = false, reason = error
		params = {'hostname': 'thisserverdoesnotexist.com', 'buffer': '14'}
		request, response = app.test_client.post('/cert', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['valid'], 'false')
		self.assertEqual(data['reason'], 'error')

	def test_http_response(self):
		# Test a valid website (200)
		# Expected result: status = online, code = 200
		params = {'hostname': 'https://httpstat.us/200', 'redirects': 'true'}
		request, response = app.test_client.post('/http_response', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')
		self.assertEqual(data['code'], '200')

		# Test a valid redirected website (301)	and follow redirect (200)
		# Expected result: status = online, code = 200
		params = {'hostname': 'https://httpstat.us/301', 'redirects': 'true'}
		request, response = app.test_client.post('/http_response', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')
		self.assertEqual(data['code'], '200')

		# Test a valid redirected website (301) and don't follow redirect (200)
		# Expected result: status = offline, code = 301
		params = {'hostname': 'https://httpstat.us/301', 'redirects': 'false'}
		request, response = app.test_client.post('/http_response', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'offline')
		self.assertEqual(data['code'], '301')

		# Test a non-existent domain
		# Expected result: status = offline, code = 404
		params = {'hostname': 'http://thisserverdoesnotexist.com', 'redirects': 'true'}
		request, response = app.test_client.post('/http_response', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'offline')
		self.assertEqual(data['code'], '404')

		# Test an invalid webpage (404)
		# Expected result: status = offline, code = 404
		params = {'hostname': 'https://httpstat.us/404', 'redirects': 'true'}
		request, response = app.test_client.post('/http_response', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'offline')
		self.assertEqual(data['code'], '404')

	def test_tcp_socket(self):
		# Test a valid TCP socket (Google DNS)
		# Expected result: status = online
		params = {'ip': '8.8.8.8', 'port': '53'}
		request, response = app.test_client.post('/tcp_socket', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'online')

		# Test an invalid TCP socket (hopefully a random port with nothing listening)
		# Expected result: status = offline
		params = {'ip': '8.8.8.8', 'port': '65500'}
		request, response = app.test_client.post('/tcp_socket', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'offline')

		# Test a bad port number
		# Expected result: status = error
		params = {'ip': '8.8.8.8', 'port': '70000'}
		request, response = app.test_client.post('/tcp_socket', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'error')

		# Test a bad hostname/ip
		# Expected result: status = error
		params = {'ip': 'thisserverdoesnotexist.com', 'port': '8080'}
		request, response = app.test_client.post('/tcp_socket', data=json.dumps(params))
		self.assertEqual(response.status, 200)
		data = json.loads(response.text)
		self.assertEqual(data['status'], 'error')

if __name__ == '__main__':
	unittest.main()
