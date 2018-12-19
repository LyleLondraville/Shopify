import requests, json, datetime, time 
from threading import Thread 

def message(text):
	  message_link = 'telegram link here' + str(text)
	  send = requests.get(message_link) 

def condenseURL(link):
	url = link.replace("\/" , '/')
	ln = len(url)-1
	
	while ln >=0:
		if url[ln] == '?':
			index = ln
			break
		else :
			pass
		ln -= 1 
	return url[0:index] 
 
	
def parse(dict, site):

	rawPrice = json.dumps(dict['price'])
	rawPriceLen = len(rawPrice)
	price = ' $' + rawPrice[0:rawPriceLen-2] + '.' + rawPrice[rawPriceLen-2:rawPriceLen]
	
	vendor = json.dumps(dict['vendor'])

	title = json.dumps(dict['product_title'])

	category = json.dumps(dict['product_type'])
	
	url = site + condenseURL(json.dumps(dict['url']))

	image = condenseURL(json.dumps(dict['image']))

	desk = json.dumps(dict['product_description'])

 	status_code = str((requests.get(url)).status_code)
	
	tempdata = '*******THESE VARIANTS AND THE SOFTWARE USED TO SCRAPE THEM WERE DEVELOPED BY LYLE LONDRAVILLE / @SoleWingSneaks****** \n\nBrand : %s \n\nTitle : %s \n\nCategory : %s \n\nPrice : %s \n\nURL : %s \n\nStatus code : %s\n\nImage : %s \n\nDescription : %s \n\n---------------------Product Variations--------------------\n\n' % (vendor, title, category, price, url, status_code, image, desk)

	prodData = tempdata.replace('"' , '')

	return prodData

def haste(text):
	hast = requests.post('http://hastebin.com/documents', data = text)
	key = hast.json()['key']
	return 'http://hastebin.com/%s.txt' % key


def scrape(url, start, stop, thread, storeName):

	currentVarList = {}
	whileVarIndex = []
	goodVarIndex = []
	varIndex = []
	index404 = 0
	indexCont = 0
	cont = 1


	while start <= stop :
		varIndex.append(start)
		start += 64

	while len(varIndex) > 0 :
		
		goodVarIndex[:] = []
		
		time1 = datetime.datetime.now()

		for var in varIndex:
			
			if var not in whileVarIndex:
				
				try :
					ATC = requests.get('%s/cart/add.js?id=%s' % (url, str(var)))

					if ATC.status_code == 200 :

						JSONdict = json.loads(ATC.text)
							
						PID = JSONdict['product_id'] 
						hasteData = parse(JSONdict, url)
						
						index404 = 0	
						
						whileIndexCont = indexCont
						
						while index404 < 450 :
							
							if whileIndexCont < len(varIndex) :
								
								try :
									
									whileATC = requests.get('%s/cart/add.js?id=%s' % (url, str(varIndex[whileIndexCont])))

									whileVarIndex.append(varIndex[whileIndexCont])

									if whileATC.status_code == 200 :

										JSONdata = json.loads(whileATC.text)
												
										if JSONdata['product_id'] == PID :
											currentVarList.update({varIndex[whileIndexCont]:JSONdata['variant_title']})
											goodVarIndex.append(var)
										else :
											index404 += 450
											whileVarIndex.remove(varIndex[whileIndexCont])
											break 
									else :
										index404 += 1

									whileIndexCont += 1
							
								except :
									print 'Error excpt2 sleeping for 200 seconds'
									time.sleep(200)
							
							else :
								index404 += 450

						for var, title in currentVarList.iteritems():
							hasteData += (str(var) + ' - ' + title + "\n\n")

						hasteData += '-----------------------------------------------------------'

						message(json.dumps(JSONdict['product_title']) + ' ' + (haste(hasteData)))

				except :	
					print 'Error excpt2 sleeping for 200 seconds'
					time.sleep(200)
			
			else :
				pass
				

			indexCont += 1

		time2 = datetime.datetime.now()

		cont += 1
		
		print 'Thread #%s : Compleated scraping %s for loop number %s in timeframe %s and found %s products' % (thread, storeName, cont, (time2 - time1), str(len(goodVarIndex)))


def cook():

	t1 = Thread(target = scrape, args = ('http://us.bape.com/', 21598624709, 21600467973, '1', 'Bape'))
	t2 = Thread(target = scrape, args = ('http://us.bape.com/', 21600467973, 21602311173, '2', 'Bape'))
	t3 = Thread(target = scrape, args = ('http://us.bape.com/', 21602311173, 21604154373, '3', 'Bape'))
	t4 = Thread(target = scrape, args = ('http://us.bape.com/', 21604154373, 21605997573, '4', 'Bape'))
	t5 = Thread(target = scrape, args = ('http://us.bape.com/', 0, 0, '1', 'Bape'))
	t6 = Thread(target = scrape, args = ('http://us.bape.com/', 0, 0, '1', 'Bape'))
	t7 = Thread(target = scrape, args = ('http://us.bape.com/', 0, 0, '1', 'Bape'))
	t8 = Thread(target = scrape, args = ('http://us.bape.com/', 0, 0, '1', 'Bape'))


	t1.start()
	t2.start()
	t3.start()
	t4.start()


cook()