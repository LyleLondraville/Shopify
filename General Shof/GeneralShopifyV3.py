import requests, json, datetime, time
from threading import Thread

def message(text):
	  message_link = 'telegram link here' + str(text)
	  send = requests.get(message_link)

def condenseURL(link):
	if link == 'null' :
		return 'null'
	else :
		tempUrl = link.replace("\/" , '/')
		url = tempUrl.replace('//', '/')

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

 	status_code = str((requests.get(url.replace('"' , ''))).status_code)

	tempdata = '*******THESE VARIANTS AND THE SOFTWARE USED TO SCRAPE THEM WERE DEVELOPED BY LYLE LONDRAVILLE / @SoleWingSneaks****** \n\nBrand : %s \n\nTitle : %s \n\nCategory : %s \n\nPrice : %s \n\nURL : %s \n\nStatus code : %s\n\nImage : %s \n\nDescription : %s \n\n---------------------Product Variations--------------------\n\n' % (vendor, title, category, price, url, status_code, image, desk)

	prodData = tempdata.replace('"' , '')

	return prodData

def haste(text):
	hast = requests.post('http://hastebin.com/documents', data = text)
	key = hast.json()['key']
	return 'http://hastebin.com/%s.txt' % key


def scrape(url, start, interval, thread, storeName):

	currentVarList = {}
	whileVarIndex = []
	goodVarIndex = []
	varIndex = []
	index404 = 0
	indexCont = 0
	cont = 1
	nameCont = 1


	stop = start + interval

	while start <= stop :
		varIndex.append(start)
		start += 64

	while len(varIndex) > 0 :

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
											currentVarList.update({varIndex[whileIndexCont] : json.dumps(JSONdata['variant_title'])})
											goodVarIndex.append(var)
											index404 = 0
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

						productTitle = (json.dumps(JSONdict['product_title'])).replace('"', '')
						message(((productTitle) + ' ' + (haste(hasteData))))
						print 'Found ' + productTitle

						#fileName = str(nameCont) + '.txt'
						#nameCont += 1

						#txtFile = open(fileName, 'w')
						#txtFile.write(hasteData)
						#txtFile.close()

						currentVarList.clear()

				except :
					print 'Error excpt2 sleeping for 200 seconds'
					time.sleep(200)

			else :
				pass


			indexCont += 1

		cont += 1

		goodVarIndex.sort(reverse = true)

		varIndex[:] = []

		refrancePnt = goodVarIndex[0]

		while refrancePnt <= refrancePnt + interval :
			varIndex.append(refrancePnt)
			refrancePnt += 64

		time2 = datetime.datetime.now()

		print 'Thread #%s : Compleated scraping %s for loop number %s in timeframe %s and found %s products, moving on to scrape %s through %s \n' % (thread, storeName, cont, (time2 - time1), str(len(goodVarIndex)), varIndex[0], varIndex[(len(varIndex)-1)])

		goodVarIndex[:] = []

def cook():
    t1 = Thread(target = scrape, args = ('https://shop.renarts.com', 000000000000000, 5760000, '1', 'Renarts'))
    t2 = Thread(target = scrape, args = ('https://www.solestop.com', 000000000000000, 5760000, '2', 'solestop'))
    t3 = Thread(target = scrape, args = ('http://shop.havenshop.ca', 000000000000000, 5760000, '3', 'havenshop'))
    t4 = Thread(target = scrape, args = ('https://offthehook.ca', 000000000000000, 5760000, '4', 'offthehook'))
    t5 = Thread(target = scrape, args = ('https://shop.bdgastore.com', 000000000000000, 5760000, '5', 'bdgastore'))
    t6 = Thread(target = scrape, args = ('http://www.deadstock.ca/', 000000000000000, 5760000, '6', 'deadstock'))
    t7 = Thread(target = scrape, args = ('https://www.blendsus.com/', 000000000000000, 5760000, '7', 'blendsus'))
    t8 = Thread(target = scrape, args = ('https://properlbc.com', 000000000000000, 5760000, '8', 'properlbc'))
    t9 = Thread(target = scrape, args = ('https://shop.exclucitylife.com', 000000000000000, 5760000, '9', 'exclucitylife'))
    t10 = Thread(target = scrape, args = ('http://shopnicekicks.com/', 000000000000000, 5760000, '10' , 'shopnicekicks'))
    t11 = Thread(target = scrape, args = ('https://www.featuresneakerboutique.com', 000000000000000, 5760000, '11', 'featuresneakerboutique'))
    t12 = Thread(target = scrape, args = ('http://rise45.com/', 000000000000000, 5760000, '12', 'rise45'))
    t13 = Thread(target = scrape, args = ('https://kithnyc.com/', 000000000000000, 5760000, '13', 'kithnyc'))
    t14 = Thread(target = scrape, args = ('http://packershoes.com/', 000000000000000, 5760000, '14', 'packershoes'))
    t15 = Thread(target = scrape, args = ('http://www.addictmiami.com/', 000000000000000, 5760000, '15', 'addictmiami'))
    t16 = Thread(target = scrape, args = ('http://www.xhibition.co/', 000000000000000, 5760000, '16' , 'xhibition'))


    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()

cook()
