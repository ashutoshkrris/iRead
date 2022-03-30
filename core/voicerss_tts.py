import urllib.request
import urllib.parse
import urllib.error
import http.client


def speech(settings):
	__validate(settings)
	return __request(settings)


def __validate(settings):
	if not settings:
		raise RuntimeError('The settings are undefined')
	if 'key' not in settings or not settings['key']:
		raise RuntimeError('The API key is undefined')
	if 'src' not in settings or not settings['src']:
		raise RuntimeError('The text is undefined')
	if 'hl' not in settings or not settings['hl']:
		raise RuntimeError('The language is undefined')


def __request(settings):
	result = {'error': None, 'response': None}

	headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
	params = urllib.parse.urlencode(__buildRequest(settings))

	if 'ssl' in settings and settings['ssl']:
		conn = http.client.HTTPSConnection('api.voicerss.org:443')
	else:
		conn = http.client.HTTPConnection('api.voicerss.org:80')

	conn.request('POST', '/', params, headers)

	response = conn.getresponse()
	content = response.read()
	print(response.status)
	if response.status != 200:
		result['error'] = response.reason
	else:
		result['response'] = content

	conn.close()

	return result


def __buildRequest(settings):
	params = {'key': '', 'src': '', 'hl': '', 'v': '',
           'r': '', 'c': '', 'f': '', 'ssml': '', 'b64': ''}

	if 'key' in settings:
		params['key'] = settings['key']
	if 'src' in settings:
		params['src'] = settings['src']
	if 'hl' in settings:
		params['hl'] = settings['hl']
	if 'v' in settings:
		params['v'] = settings['v']
	if 'r' in settings:
		params['r'] = settings['r']
	if 'c' in settings:
		params['c'] = settings['c']
	if 'f' in settings:
		params['f'] = settings['f']
	if 'ssml' in settings:
		params['ssml'] = settings['ssml']
	if 'b64' in settings:
		params['b64'] = settings['b64']

	return params
