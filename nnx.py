import json
import requests
import random
import time


randomitems = ["bayreuther", "weizen", "limo", "cola", "sprite", "bionade", "desperados", "cocktail", "longdrink", "shot", "salat", "currywurst", "nachos", "wrap", "pizza"]

answers = {
		"tableNumber": random.randint(0,50),
		"randomAuthKey": str(round(time.time()* 100000)),
		"done": 0,
		"boughtItems": [
			{
				"itemName": randomitems[random.randint(0, 14)],
				"itemPriceOne": random.randint(0,10),
				"itemsBought": random.randint(0,10),
				"itemPriceAll": random.randint(0, 100)
			},
			{
				"itemName": randomitems[random.randint(0, 14)],
				"itemPriceOne": random.randint(0,10),
				"itemsBought": random.randint(0,10),
				"itemPriceAll": random.randint(0, 100)
			},
			{
				"itemName": randomitems[random.randint(0, 14)],
				"itemPriceOne": random.randint(0,10),
				"itemsBought": random.randint(0,10),
				"itemPriceAll": random.randint(0, 100)
			}
		],
		"totalBill": 50
	}
print(answers)

#encoded_data = json.dumps(answers).encode('utf-8')
#print(encoded_data)
#r = http.request(
#    'post',
#    'http://localhost:3000/create-new?'+encoded_args,
#    body=encoded_data)
headers = {'content-type': 'application/json', 'accept': 'text/plain'}
r = requests.post("http://localhost:3000/create-new?auth=1234",headers=headers, data=json.dumps(answers), )
