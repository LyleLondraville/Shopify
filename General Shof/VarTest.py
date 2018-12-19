import requests, datetime, json

def test(url,start,stop):
	t1 = datetime.datetime.now()
	
	while start <= stop :
		r = requests.get('%s/cart/add.js?id=%s' % (url, str(start)))
		start += 1

	t2 = datetime.datetime.now()

	print t2-t1

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

def scrape(url, var):
	
        currentVarList = {}
        nameList = []
        cont = 1
	
        while 1==1 :
					
			ATC = requests.get('%s/cart/add.js?id=%s' % (url, str(var)))
			
			if ATC.status_code == 200 :

			
				JSONdict = json.loads(ATC.text)			
			
				PID = JSONdict['product_id'] 
				
				hasteData = parse(JSONdict, url)		

				index404 = 0	
			else :
				pass 


print ((((5*60)*60)*10)*64) 
print (((float(33858923463 - 33227006087)/5)/60)/60)/64



