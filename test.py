from app import app, ipv4_capable, ipv6_capable
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
		if (ipv4_capable): # only run tests if IPv4 capable
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

			# Test real IPv4 hostname (Google)
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
		else:
			print('This node is not IPv4 capable, skipping IPv4 ping tests...')

	def test_ping6(self):
		if (ipv6_capable): # only run tests if IPv6 capable
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
		else:
			print('This node is not IPv6 capable, skipping IPv6 ping tests...')

	def test_cert(self):
		if (ipv4_capable): # only run tests if IPv4 capable
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
		else:
			print('This node is not IPv4 capable, skipping certificate tests...')

	def test_http_response(self):
		if (ipv4_capable):
			# Test a valid website (200)
			# Expected result: status = online, code = 200
			params = {'hostname': 'https://httpstat.us/200', 'redirects': 'true', 'check_string': 'false', 'keywords': ''}
			request, response = app.test_client.post('/http_response', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'online')
			self.assertEqual(data['code'], '200')

			# Test a valid redirected website (301)	and follow redirect (200)
			# Expected result: status = online, code = 200
			params = {'hostname': 'https://httpstat.us/301', 'redirects': 'true', 'check_string': 'false', 'keywords': ''}
			request, response = app.test_client.post('/http_response', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'online')
			self.assertEqual(data['code'], '200')

			# Test a valid redirected website (301) and don't follow redirect (200)
			# Expected result: status = offline, code = 301
			params = {'hostname': 'https://httpstat.us/301', 'redirects': 'false', 'check_string': 'false', 'keywords': ''}
			request, response = app.test_client.post('/http_response', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'offline')
			self.assertEqual(data['code'], '301')

			# Test a non-existent domain
			# Expected result: status = offline, code = 404
			params = {'hostname': 'http://thisserverdoesnotexist.com', 'redirects': 'true', 'check_string': 'false', 'keywords': ''}
			request, response = app.test_client.post('/http_response', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'offline')
			self.assertEqual(data['code'], '404')

			# Test an invalid webpage (404)
			# Expected result: status = offline, code = 404
			params = {'hostname': 'https://httpstat.us/404', 'redirects': 'true', 'check_string': 'false', 'keywords': ''}
			request, response = app.test_client.post('/http_response', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'offline')
			self.assertEqual(data['code'], '404')

			# Test a valid website (200) and match text that's present
			# Expected result: status = online, code = 200
			params = {'hostname': 'https://httpstat.us/200', 'redirects': 'true', 'check_string': 'true', 'keywords': '200 OK'}
			request, response = app.test_client.post('/http_response', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'online')
			self.assertEqual(data['code'], '200')

			# Test a valid website (200) and match text that doesn't exist
			# Expected result: status = offline, code = 200
			params = {'hostname': 'https://httpstat.us/200', 'redirects': 'true', 'check_string': 'true', 'keywords': 'Dinosaur'}
			request, response = app.test_client.post('/http_response', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'offline')
			self.assertEqual(data['code'], '200')
		else:
			print('This node is not IPv4 capable, skipping HTTP response tests...')

	def test_tcp_socket(self):
		if (ipv4_capable):
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
		else:
			print('This node is not IPv4 capable, skipping TCP port tests...')

	def test_steam_server(self):
		if (ipv4_capable):
			# Test a (hopefully) valid Steam server (pulled one from gametracker.com -- may go offline)
			# Expected result: status = online
			params = {'ip': '46.188.102.34', 'port': '27030'}
			request, response = app.test_client.post('/steam_server', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'online')

			# Test an invalid Steam server (random ip and port)
			# Expected result: status = offline
			params = {'ip': '123.122.121.120', 'port': '8787'}
			request, response = app.test_client.post('/steam_server', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'offline')

			# Test a bad port number
			# Expected result: status = error
			params = {'ip': '8.8.8.8', 'port': '70000'}
			request, response = app.test_client.post('/steam_server', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'error')

			# Test a bad hostname/ip
			# Expected result: status = error
			params = {'ip': 'thisserverdoesnotexist.com', 'port': '8080'}
			request, response = app.test_client.post('/steam_server', data=json.dumps(params))
			self.assertEqual(response.status, 200)
			data = json.loads(response.text)
			self.assertEqual(data['status'], 'error')
		else:
			print('This node is not IPv4 capable, skipping Steam server tests...')

if __name__ == '__main__':
	unittest.main()
