import json
import urllib3
import requests
http = urllib3.PoolManager()
from urllib.parse import urlencode
answers = {
		"tableNumber": 1,
		"randomAuthKey": "algkeiafe",
		"done": 0,
		"boughtItems": [
			{
				"itemName": "Cola",
				"itemPriceOne": 2,
				"itemsBought": 2.50,
				"itemPriceAll": 5.00
			},
			{
				"itemName": "Salat",
				"itemPriceOne": 2,
				"itemsBought": 5.00,
				"itemPriceAll": 10.00
			},
			{
				"itemName": "Pizza",
				"itemPriceOne": 2,
				"itemsBought": 10,
				"itemPriceAll": 20.00
			}
		],
		"totalBill": 50
	}
encoded_args = urlencode({'auth': '1234'})
#encoded_data = json.dumps(answers).encode('utf-8')
#print(encoded_data)
#r = http.request(
#    'POST',
#    'http://localhost:3000/create-new?'+encoded_args,
#    body=encoded_data)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post("http://localhost:3000/create-new?"+encoded_args, data=json.dumps(answers), headers=headers)
