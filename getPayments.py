import requests
import json
import mysql.connector
from mysql.connector import Error
from requests.auth import HTTPBasicAuth
from datetime import date

def sendToYuki(fileName):
	headers = {
	'Accept': "application/pdf",
	'Content-Type': "multipart/form-data",
	'Cache-Control': "no-cache",
	}

	files = {
	'fileupload1': open(fileName, 'rb')
	}

	resp = requests.post('https://api.yukiworks.nl/docs/Upload.aspx?WebServiceAccessKey=&Domain=regius-products&Administration=3d8308ba-1dd9-4030-b797-ff07a322b435&FileName={}&Folder=7'.format(fileName), files=files, headers=headers)
	if resp.status_code != 200:
        	print('something went wrong')
	else:
        	print(resp)

def getTransferwise(currency):

	today = date.today()
	day = today.strftime("%d")
	month = today.strftime("%m")
	year = today.strftime("%Y")

	resp = requests.get('https://api.transferwise.com/v3/profiles/11871469/borderless-accounts/4582022/statement.pdf?currency={}&intervalStart={}-{}-{}T00:00:00.000Z&intervalEnd={}-{}-{}T23:59:59.999Z&type=FLAT'.format(currency,year,month,day,year,month,day), headers = {'Authorization': 'Bearer '})
	if resp.status_code != 200:
		print('something went wrong')
	else:
		fileName = 'Transferwise-' + today.strftime("%d%m%Y") + '-' + currency + '.pdf'
		f = open(fileName,'wb')
		f.write(resp.content)
		f.close()
		sendToYuki(fileName)


getTransferwise('USD')
getTransferwise('EUR')
