import os
import sys
from thingiverseApi import *

class Driver():
	def __init__(self, thingObj):
		self._thingObj = thingObj

	def execute(self):
		i = 1
		print 'Please enter your search keyword'
		keyword = raw_input()
		searchList = []
		fileList = []
		raw_search = self._thingObj.search(keyword)
		for item in raw_search:
			searchList.append((item['id'],item['name']))

		
		for item in searchList:
			print i,'.',item[1]
			if i==6:
				i=1
				break
			i = i+1
		if len(searchList):
			print 'Please Choose One Object'
			model = int(raw_input())
		else:
			return 0
		raw_model_info = self._thingObj.file_List(searchList[model-1][0])

		for item in raw_model_info:
			fileList.append((item['id'], item['name'], item['public_url']))

		for item in fileList:
			print i,'.',item[1]
			if i==6:
				break
			i = i+1
		if len(fileList):
			print 'Please Select STL to Download'
			stlNo = int(raw_input())

			#print fileList[stlNo-1]
			request = requests.get(fileList[stlNo-1][2], stream=True)
			print 'Downloading ', fileList[stlNo-1][1]
			with open(fileList[stlNo-1][1], 'w') as f:
				fileLength = 0
				for chunk in request.iter_content(chunk_size=1024):
					if chunk:
						fileLength += len(chunk)
						f.write(chunk)
						f.flush()	
				print (fileLength/1024), 'KB Downloaded'
		else:
			print ' No files to download!!'



def main():
	appinfo = {'client_id': '57b2f80245f6f6d91b86',
				'client_secret': 'e426c4a0e107a43f94c2c25264a8caa8',
				'redirect_uri': ''}

	thingObj = Thingiverse(appinfo)
	thingObj.connect()
	driverObj = Driver(thingObj)
	res = 'yes'
	while res=='Yes' or res=='yes':
		driverObj.execute()
		print 'Do you want to continue search(yes/no):'
		res = raw_input()


if __name__=="__main__":
	main()
