import requests
import json
import mysql.connector
from mysql.connector import Error
from requests.auth import HTTPBasicAuth

def set_database(order_id, fulfilled):
	sql = "INSERT INTO orders (order_id, fulfilled) VALUES (%s, %s)"
        val = (order_id, fulfilled)
        mycursor.execute(sql, val)
        mydb.commit()
	print('executed')

def get_database(select_value, column ,value):
	try:
		mycursor.execute('SELECT {} FROM orders WHERE {} = \'{}\''.format(select_value,column,value))
                result = mycursor.fetchall()
                return result
	except Error as e:
		print("The error {} occurred".format(e))

def get_info(city,country,line1,line2,state,addressee,postalCode):
	counter = 0
	for todo_item in resp.json():
		order = resp.json()
		order_id = ((order[counter])['orderId'])
    		totals = ((order[counter])['totals'])
		extras = totals['extras']
		shipping_prio = extras[0]['name']
		print("{}".format(shipping_prio))

		address_info = ((order[counter])['allAddresses'])
		name = address_info[1]['addressee']
    		city = address_info[1]['city']
		country = address_info[1]['country']
		line1 = address_info[1]['line1']
		state = address_info[1]['state']
		addressee = address_info[1]['addressee']
		postalCode = address_info[1]['postalCode']
		print("Addresse: {}".format(addressee))
		print("line1: {}".format(line1))
		print("city: {}".format(city))
		print("state: {}".format(state))
		print("country: {}".format(country))


		Units = ((order[counter])['purchasedItems'])
		SKU = Units[0]['variantSKU']
		amount = Units[0]['count']
		product_Name = Units[0]['productName']
		print('SKU: {}'.format(SKU))
		print('amount: {}'.format(amount))
		print(product_Name)

		fulfilled = 0
		print("order_id: {}".format(order_id))
		print(" ")
    		counter+=1

		if not get_database('order_id', 'order_id', order_id):
			set_database(order_id, fulfilled)
  			data =  {
  					"SiteOrderID": '{}'.format(order_id),
  					"Site": "Manual",
  					"OrderStatus": "Unshipped",
  					"DateOrdered": "",
  					"Name": '{}'.format(addressee),
  					"Address1": '{}'.format(line1),
  					"Address2": "",
  					"Address3": "",
  					"City": '{}'.format(city),
  					"StateOrRegion": '{}'.format(state),
  					"Country": "US",
  					"PostalCode": '{}'.format(postalCode),
  					"Phone": "",
  					"Email": "",
  					"Note": "",
  					"OrderDetails": [
    						{
      							"SiteItemID": '{}'.format(SKU),
      							"OrderStatus": "Unshipped",
      							"DateShipped": "",
      							"SKU": '{}'.format(SKU),
      							"Title": '{}'.format(product_Name),
      							"QuantityOrdered": amount,
      							"QuantityShipped": 0,
      							"QuantityUnfillable": 0,
      							"CurrencyISO": "Default",
      							"UnitPrice": 0,
      							"UnitTax": 0,
      							"ShippingPrice": 0,
      							"ShippingTax": 0,
      							"ShippingDiscount": 0,
      							"GiftMessage": "",
      							"GiftWrapPrice": 0,
      							"GiftWrapTax": 0,
      							"ProductOptions": "",
      							"ShippingServiceOrdered": '{}'.format(shipping_prio),
      							"ShippingServiceActual": "",
      							"ShippingTracking": "",
      							"ShippingTrackingUrl": "",
      							"ShippingActualWeight": "",
      							"ShippingActualCharge": 0,
      							"ShippingCarrier": ""
    						}
  					]
				}

			createOrder = requests.post('https://rest.selleractive.com/api/Order', auth=HTTPBasicAuth('', ''), json=data)
			print(createOrder)

def fulfill_order():
	print("Works!")
	counter = 0
        for todo_item in resp.json():
		order = resp.json()
		order_id = ((order[counter])['orderId'])
		print('order_fulfill order_id: {}'.format(order_id))
		payload = {'req.siteOrderID': order_id}
		getOrder = requests.get('https://rest.selleractive.com/api/Order', auth=HTTPBasicAuth('', ''), params=payload)
		#print(getOrder.json())
		retrieved_order = getOrder.json()
		Tracking = retrieved_order[0]['OrderDetails'][0]['ShippingTracking']
		TrackingUrl = retrieved_order[0]['OrderDetails'][0]['ShippingTrackingUrl']
		print(Tracking)
		if Tracking == '':
			print("Empty")
		else:
			fields ={
				"comment": "Tracking URL: {}".format(TrackingUrl),
        			"shippingProvider": "",
        			"shippingTracking": "{}".format(Tracking)
    				}
			fulfill_webflow_order = requests.patch(''.format(order_id), headers = {'accept-version':'1.0.0', 'Authorization': 'Bearer '}, json=fields)
			print(fulfill_webflow_order)

		counter+=1

mydb = mysql.connector.connect(
	host="",
	user="",
	passwd="",
	database=""
)
mycursor = mydb.cursor()

resp = requests.get('', headers = {'accept-version':'1.0.0', 'Authorization': 'Bearer '})
if resp.status_code != 200:
    print('something went wrong')
    # This means something went wrong.
    #raise ApiError('GET /tasks/ {}'.format(resp.status_code))

get_info('city','country','line1','line2','state', 'addressee', 'postalCode')
fulfill_order()
