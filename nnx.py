
import json
import requests
import random
import time

randomitems = ["Bayreuther", "Weizen", "Limo", "Cola", "Sprite", "Bionade", "Desperados", "Cocktail", "Longdrink", "Shot", "Salat", "Currywurst", "Nachos", "Wrap", "Pizza"]

#generate 10 bills
for x in range(10):
	arrayItems = []
	#for each bill generate random amount of items bought
	for x in range(random.randint(1,9)):
		priceOne = random.randint(1,10)
		itemsBought = random.randint(0,10)
		oneItem = {
			"itemName": randomitems[random.randint(0,14)],
			"itemPriceOne": priceOne,
			"itemsBought" : itemsBought,
			"itemPriceAll": priceOne * itemsBought
			}
		arrayItems.append(oneItem)
	answers = {
		"tableNumber": random.randint(0,50),
		"randomAuthKey": str(round(time.time()* 100000)),
		"done": 0,
		"boughtItems": arrayItems,
		"totalBill": 50,
	}
	headers = {'content-type': 'application/json', 'accept': 'text/plain'}
	r = requests.post("https://billgatesprojekt.herokuapp.com/create-new?auth=1234",headers=headers, data=json.dumps(answers), )
	print("########################################################################")
	print(answers)



#print(answers)

#encoded_data = json.dumps(answers).encode('utf-8')
#print(encoded_data)
#r = http.request(
#    'post',
#    'https://billgatesprojekt.herokuapp.com/create-new?auth=1234'+encoded_args,
#    body=encoded_data)
#headers = {'content-type': 'application/json', 'accept': 'text/plain'}
#r = requests.post("https://billgatesprojekt.herokuapp.com/create-new?auth=1234",headers=headers, data=json.dumps(answers), )
