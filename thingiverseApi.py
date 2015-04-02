from rauth import OAuth2Service
import json
import os
import sys
import webbrowser
import requests

class Thingiverse:
	def __init__(self, appinfo):
		self._appinfo = appinfo
		self._access_code = ''
		self._session = None
		self._auth = None

	def connect(self):
		if not self._auth:
			self._auth = OAuth2Service(
				name='AIOTEST',
				client_id=self._appinfo['client_id'],
				client_secret=self._appinfo['client_secret'],
				access_token_url='https://www.thingiverse.com/login/oauth/access_token',
				authorize_url='https://www.thingiverse.com/login/oauth/authorize',
				base_url='https://api.thingiverse.com')

		#self._get_access_code()
		self._access_code = 'cc3b8745dbaa5fab85f7d43d34b2877c'
		self._get_access_token()

	def _get_access_token(self):
		params = {'client_id':self._appinfo['client_id'], 'client_secret':self._appinfo['client_secret'], 'code':self._access_code}

		try:
			self._session = self._auth.get_auth_session(data=params)
		except KeyError as e:
			#self._get_access_code()
			#self._get_access_token()
			print e
			sys.exit(1)


	def _get_access_code(self):
		params = {'redirect_uri': self._appinfo['redirect_uri'],
				  'response_type': 'code'}
		url = self._auth.get_authorize_url(**params)
		#print 'url', url
		webbrowser.open_new(url)

	def _api_get(self, suffix_url, params):
		try:
			response = self._session.get(self._auth.base_url+suffix_url,params=params) 
			return response.json()
		except Exception as error:
			print error
			sys.exit()

	def search(self, keyword, data=None):
		suffix_url = '/search/' + keyword + '/'
		print 'keyword:',keyword
		return self._api_get(suffix_url, data)

	def file_List(self, thingID, data=None):
		suffix_url = '/things/' + thingID + '/files/'
		return self._api_get(suffix_url, data)

