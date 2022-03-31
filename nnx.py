
import json
import requests
import random
import time

randomitems = ["Bayreuther", "Weizen", "Limo", "Cola", "Sprite", "Bionade", "Desperados", "Cocktail", "Longdrink", "Shot", "Salat", "Currywurst", "Nachos", "Wrap", "Pizza"]

#generate 10 bills
for x in range(10):
	arrayItems = []
	totalBill = 0
	
	#for each bill generate random amount of items bought
	usedItems = ["m"]
	for x in range(random.randint(1,9)):
		while (1):
			foundName = 0
			itemName = randomitems[random.randint(0,14)]
			for x in usedItems:
				if(x == itemName):
					foundName = 1
			
			if(foundName == 0):
				usedItems.append(itemName)
				break
		#make sure each itemName only appears once in 
		priceOne = random.randint(1,10)
		itemsBought = random.randint(0,10)
		priceAll = priceOne * itemsBought
		totalBill += priceAll
		oneItem = {
			"itemName": itemName,
			"itemPriceOne": priceOne,
			"itemsBought" : itemsBought,
			"itemPriceAll": priceAll
			}
		arrayItems.append(oneItem)
	answers = {
		"tableNumber": random.randint(0,50),
		"randomAuthKey": str(round(time.time()* 100000)),
		"done": 0,
		"boughtItems": arrayItems,
		"totalBill": totalBill,
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
