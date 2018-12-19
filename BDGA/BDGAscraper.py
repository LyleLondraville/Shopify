import requests, json, datetime
from threading import Thread 

def message(text):
	  message_link = 'telegram link here' + str(text)
	  send = requests.get(message_link) 

def photo(imageURL):
	url = imageURL.replace("\/" , '/')
	ln = len(url)-1
	
	while ln >=0:
		if url[ln] == '?':
			index = ln
			break
		else :
			pass
		ln -= 1 
	finalURL = url[0:index]
	message_link = 'telegram link here' + str(finalURL)
import requests, json, datetime
from threading import Thread 

def message(text):
	  message_link = 'telegram link here' + str(text)
	  send = requests.get(message_link) 

def parsePhoto(imageURL):
	url = imageURL.replace("\/" , '/')
	ln = len(url)-1
	
	while ln >=0:
		if url[ln] == '?':
			index = ln
			break
		else :
			pass
		ln -= 1 
	return url[0:index] 
	
def parse(dict):

	rawPrice = json.dumps(dict['price'])
	rawPriceLen = len(rawPrice)
	price = ' $' + rawPrice[0:rawPriceLen-2] + '.' + rawPrice[rawPriceLen-2:rawPriceLen]
	prodData = dict['vendor'] + ' ' +dict['product_title'] + price 

	return prodData

def haste(text):
	hast = requests.post('http://hastebin.com/documents', data = text)
	key = hast.json()['key']
	return 'http://hastebin.com/%s.txt' % key


def scrape(url, start, stop, thread, storeName):

	varIndex = []
	goodVarIndex = []
	prodDataIndex = []
	currentVarList = {}
	cont = 1

	while start <= stop :
		varIndex.append(start)
		start += 64

	tmp = requests.get('%s/cart/add.js?id=%s' % (url, str(varIndex[0])))
	JSONdic = json.loads(tmp.text)

	currentProdTitle = JSONdic['product_title']
	productTitleData = parse(JSONdic)
	photoURL = parsePhoto(JSONdic['image'])
	
	while len(varIndex) > 0 :

		time1 = datetime.datetime.now()

		for var in varIndex:
			try :
				
				r = requests.get('%s/cart/add.js?id=%s' % (url, str(var)))
				
				JSONdata = json.loads(r.content)
				
				if r.status_code == 200 :
						
					if JSONdata['product_title'] == currentProdTitle:
						
						currentVarList.update({str(var):JSONdata['variant_title']})
						goodVarIndex.append(var)

					else :
						
						varSTR = ''
						for var, title in currentVarList.iteritems():
							varSTR += (title +'-'+str(var))
							varSTR += ', '
						
						prodData = productTitleData + varSTR
						message(prodData)
						sendPhoto(photoURL)
						prodDataIndex.append(prodData)

						currentProdTitle = JSONdata['product_title']
						productTitleData = parse(JSONdata)
						photoURL = parsePhoto(JSONdata['image'])

						goodVarIndex.append(var)
			except :	
				message('Thread %s reached an error in scraping %s, pausing for 200 seconds and resuming scraping.' % (thread, storeName))
				time.sleep(200)
		
		for var in goodVarIndex :
			varIndex.remove(var)

		txt = open(('%s_T%sL%s' % (storeName, thread, cont)), 'w')
		for data in prodDataIndex:
			txt.write(data + '\n')
		txt.close()

		time2 = datetime.datetime.now()

		print 'Thread #%s : Compleated scraping %s for loop number %s in timeframe %s and found %s products' % (thread, storeName, cont, (time2 - time1), str(len(goodVarIndex)))
		
		cont += 1
		goodVarIndex[:] = []

scrape('https://shop.bdgastore.com', 26257760968, 26257761672, '1', 'Boudega')
						prodDataIndex.append(prodData)
			except :	
				message('Thread %s reached an error in scraping %s, pausing for 200 seconds and resuming scraping.' % (thread, storeName))
		
		for var in goodVarIndex :
			varIndex.remove(var)

		txt = open(('%s_T%sL%s' % (storeName, thread, cont)), 'w')
		for data in prodDataIndex:
			txt.write(data + '\n')
		txt.close()

		time2 = datetime.datetime.now()

		print 'Thread #%s : Compleated scraping %s for loop number %s in timeframe %s and found %s products' % (thread, storeName, cont, (time2 - time1), str(len(goodVarIndex)))
		cont += 1


scrape('https://shop.bdgastore.com', 26257760968, 26257761608, '1', 'Boudega')