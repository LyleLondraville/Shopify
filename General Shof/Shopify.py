import requests, time, json
from io import StringIO
from lxml import html, etree
from lxml.html import parse, open_in_browser
from threading import Thread
import datetime
import requests, json, time
from threading import Thread
import xml.etree.ElementTree as ET

class AntiCaptcha:

    def __init__(self, siteKey, url):
        self.antiKey = 'Key here'
        self.siteKey = siteKey
        self.url = url
        self.captchaList = []

    def makeCaptcha(self):

        passed = False

        data = json.dumps({
            "clientKey": self.antiKey,
            "task":
                {
                    "type": "NoCaptchaTaskProxyless",
                    "websiteURL": self.url,
                    "websiteKey": self.siteKey
                }
        })

        while passed == False :
            try :
                r = requests.post('http://api.anti-captcha.com/createTask', data=data)
                passed = True
            except:
                pass

        taskID = json.loads(r.text)['taskId']

        data2 = json.dumps({
            "clientKey": self.antiKey,
            "taskId": taskID})

        while True:
            try :
                r = requests.post('https://api.anti-captcha.com/getTaskResult', data=data2)
                j = json.loads(r.text)
                # print j['status']
                if j['status'] != 'processing':
                    statusJson = json.loads(json.dumps(j))
                    solution = json.loads(json.dumps(statusJson['solution']))['gRecaptchaResponse']
                    break
                else:
                    pass

            except :
                pass


            time.sleep(.5)

        self.captchaList.append(solution)

    def genCaptcha(self, number):
        for i in range(0, number):
            Thread(target=self.makeCaptcha, args=()).start()

    def getGenList(self):
        
        return self.captchaList

    def clearGenList(self):
       
        self.captchaList[:] = []


class shopify:

    def t(self):
        
        return time.strftime('%H:%M:%S', time.localtime())

    def findSitemap(self, keywordList):

        passed = False

        masterDict = {}

        while passed == False :
            
            print ('[{}] : Searching with keywords -  {}'.format(self.t(), keywordList))

            try :
                sitemap = requests.get('https://kith.com/sitemap_products_1.xml?')

                if sitemap.status_code == 200:
                    for p in ET.fromstring(sitemap.content):
                        child = p.getchildren()
                        link = child[0].text
                        try :
                            child2 = child[3].getchildren()
                            title = child2[1].text

                            if all(kw in '{}{}'.format(link.lower(), title.lower()) for kw in keywordList) :
                                productLink = link
                                productTitle = title
                                passed = True
                                print ("[{}] : Product found!".format(self.t()))
                                break

                            else :
                                pass

                        except :
                            pass

                else :
                    pass
            except :
                pass

        print ("[{}] : Loading json for {}, link - {}".format(self.t(), productTitle, productLink))

        productJson = json.loads((requests.get( productLink + '.json' )).text)['product']
        variantJson = json.loads(json.dumps(productJson))['variants']

        for v in variantJson:
            j = json.loads(json.dumps(v))
            size = float(j['option1'])
            var = j['id']
            masterDict.update({size:var})

        print ("[{}] : Dictonary created - {}".format(self.t(), masterDict))

        return masterDict








    def checkout(self, checkoutPreset, var, name, recaptchaToken):

        t1 = time.time()

        sesh = requests.Session()

        print ('[{}] : {} - Adding to cart with variant {}'.format( self.t(), name, var ))

        sesh.post('https://kith.com/cart/add.js?id={}'.format(var))

        print('[{}] : {} - Added to cart! Going to checkout...'.format(self.t(), name))

        checkoutInt = sesh.get('https://kith.com/checkout')

        print('[{}] : {} - Initiating chekout'.format(self.t(), name))

        checkoutData = checkoutPreset
        mainURL = checkoutInt.url
        passed = False

        if 'stock_problems' in mainURL:
            while passed == False:
                print('[{}] : {} - OOS error, refreshing {}'.format(self.t(), name, mainURL))
                ref = sesh.get(mainURL)
                if 'stock_problems' in ref.url:
                    pass
                else:
                    passed = True
                    print('[{}] : {} - Product back in stock, moving to checkout...'.format(self.t(), name))

        addyDoc = parse(StringIO(checkoutInt.text)).getroot()

        #print checkoutInt.text

        email = checkoutData['email']
        fName = checkoutData['First name']
        lName = checkoutData['Last name']
        comp = checkoutData['Company']
        addy1 = checkoutData['Address 1']
        addy2 = checkoutData['Address 2']
        city = checkoutData['City']
        stateInitals = checkoutData['State initals']
        state = checkoutData['State']
        countryInitals = checkoutData['Country initals']
        contrey = checkoutData['Country']
        zipCode = checkoutData['Zip']
        phone = checkoutData['Phone']
        cardNum = checkoutData['Card number']
        cardExpM = checkoutData['Card experation month']
        cardExpY = checkoutData['Card experation year']
        cvv = checkoutData['Card cvv']
        authToken = list(dict(addyDoc.forms[0].form_values()).values())[2]

        addyData = {
            '_method': 'patch',
            'authenticity_token': authToken,
            'previous_step': 'contact_information',
            'step': 'shipping_method',
            'checkout[email]': email,
            'checkout[buyer_accepts_marketing]': '0',
            'checkout[buyer_accepts_marketing]': '1',
            'checkout[shipping_address][first_name]': fName,
            'checkout[shipping_address][last_name]': lName,
            'checkout[shipping_address][company]': comp,
            'checkout[shipping_address][address1]': addy1,
            'checkout[shipping_address][address2]': addy2,
            'checkout[shipping_address][city]': city,
            'checkout[shipping_address][country]': countryInitals,
            'checkout[shipping_address][province]': stateInitals,
            'checkout[shipping_address][zip]': zipCode,
            'checkout[shipping_address][phone]': phone[1:len(phone)].replace(' ', '').replace('-', ''),
            'checkout[shipping_address][first_name]': fName,
            'checkout[shipping_address][last_name]': lName,
            'checkout[shipping_address][company]': comp,
            'checkout[shipping_address][address1]': addy1,
            'checkout[shipping_address][address2]': addy2,
            'checkout[shipping_address][city]': city,
            'checkout[shipping_address][country]': contrey,
            'checkout[shipping_address][province]': state,
            'checkout[shipping_address][zip]': zipCode,
            'checkout[shipping_address][phone]': phone,
            'checkout[remember_me]': '',
            'checkout[remember_me]': '0',
            'g-recaptcha-response:':recaptchaToken,
            'button': '',
            'checkout[client_details][browser_width]': '1348',
            'checkout[client_details][browser_height]': '293',
            'checkout[client_details][javascript_enabled]': '1'}

        passed = False

        print('[{}] : {} - Subbmiting address data....'.format(self.t(), name))

        try:
            addySubmit = sesh.post(mainURL, data=addyData)
        except:
            while passed == False:

                print('[{}] : {} - An unknow error has occured submitting the address data! Refreshing url {}'.format(self.t(), name,mainURL))

                try:
                    addySubmit = sesh.get(mainURL)
                    if 'shipping' in addySubmit.url:
                        passed = True
                    else:
                        print('[{}] : {} - Resubmitting address data....'.format(self.t(), name))
                        addyDoc = parse(StringIO(checkoutInt.text)).getroot()
                        addyData['authenticity_token'] = list(dict(addyDoc.forms[0].form_values()).values())[2]
                        addySubmit = sesh.post(mainURL, data=addyData)
                        passed = True
                except:
                    pass

        passed = False

        if ('stock_problems' in addySubmit.url):
            refURL = addySubmit.url

            while passed == False:
                print('[{}] : {} - OOS error refeshing url {}'.format(self.t(), name, mainURL))

                addySubmit = sesh.get(refURL)

                if 'stock_problems' not in addySubmit.url:
                    if 'shipping' in addySubmit.url:
                        passed = True
                        print('[{}] : {} - Product back in stock!'.format(self.t(), name))
                    else:
                        addyDoc = parse(StringIO(addySubmit.text)).getroot()
                        addyData['authenticity_token'] = list(dict(addyDoc.forms[0].form_values()).values())[2]
                        addySubmit = sesh.post(mainURL, data=addyData)
                        passed = True

                else:
                    pass
        else:
            pass

        print('[{}] : {} - Succsesfully submited address data'.format(self.t(), name))

        shipDoc = parse(StringIO(addySubmit.text)).getroot()

        passed = False

        shipData = {
            '_method': 'patch',
            'authenticity_token': list(dict(addyDoc.forms[0].form_values()).values())[2],
            'previous_step': 'shipping_method',
            'step': 'payment_method',
            'checkout[shipping_rate][id]': shipDoc.cssselect('div.radio-wrapper')[0].get('data-shipping-method'),
            'button': '',
            'checkout[client_details][browser_width]': '1348',
            'checkout[client_details][browser_height]': '293',
            'checkout[client_details][javascript_enabled]': '1'}

        print('[{}] : {} - Subbmiting shipping data...'.format(self.t(), name))

        try:
            shipSubmit = sesh.post(mainURL, data=shipData)

        except:
            while passed == False:
                print ('[{}] : {} - An unknown error has occured submitting the shipping data! Refreshing url {}'.format(self.t(), name, mainURL))

                try:
                    shipSubmit = sesh.get(mainURL + '?step=shipping_method')
                    if 'payment' in shipSubmit.url:
                        passed = True
                    else:
                        print ('[{}] : {} - Resubmitting shipping data...'.format(self.t(), name))
                        shipDoc = parse(StringIO(shipSubmit.text)).getroot()
                        shipData['autheticity_token'] = list(dict(shipDoc.forms[0].form_values()).values())[2]
                        shipSubmit = sesh.post(mainURL, data=shipData)
                        passed = True
                except:
                    pass

        passed = False

        if 'stock_problems' in shipSubmit.url:

            while passed == False:
                print ('[{}] : {} - OOS error refreshing url {}'.format(self.t(), name, mainURL))
                shipSubmit = sesh.get(mainURL + '?step=payment_method')

                if 'stock_probelms' not in shipSubmit.url:
                    print('[{}] : {} - Product back in stock'.format(self.t(), name))
                    passed = True
                else:
                    pass

        print('[{}] : {} - Succsesfully submited shipping data'.format(self.t(), name))

        payDoc = parse(StringIO(shipSubmit.text)).getroot()

        payData = {
            '_method': 'patch',
            'authenticity_token': list(dict(payDoc.forms[0].form_values()).values())[2],
            'previous_step': 'payment_method',
            'step': '',
            's': '',
            'checkout[payment_gateway]': str(payDoc.cssselect('input.input-radio')[0].get('value')),
            'hosted_fields_redirect': '1',
            'checkout[credit_card][vault]': 'false',
            'checkout[different_billing_address]': 'false',
            'checkout[billing_address][first_name]': '',
            'checkout[billing_address][first_name]': fName,
            'checkout[billing_address][last_name]': '',
            'checkout[billing_address][last_name]': lName,
            'checkout[billing_address][company]': '',
            'checkout[billing_address][company]': '',
            'checkout[billing_address][address1]': '',
            'checkout[billing_address][address1]': addy1,
            'checkout[billing_address][address2]': '',
            'checkout[billing_address][address2]': '',
            'checkout[billing_address][city]': '',
            'checkout[billing_address][city]': city,
            'checkout[billing_address][country]': '',
            'checkout[billing_address][country]': contrey,
            'checkout[billing_address][province]': '',
            'checkout[billing_address][province]': state,
            'checkout[billing_address][zip]': '',
            'checkout[billing_address][zip]': zipCode,
            'checkout[billing_address][phone]': '',
            'checkout[billing_address][phone]': phone,
            'checkout[total_price]': str(payDoc.cssselect('span.payment-due__price')[0].get('data-checkout-payment-due-target')),
            'complete': '1',
            'button': ''}


        print('[{}] : {} - Submiting data to go to no js checkout page...'.format(self.t(), name))

        pay = sesh.post(mainURL, data=payData)

        print('[{}] : {} - Reached no js page, moving to card page...'.format(self.t(), name))


        forwardDoc = parse(StringIO(pay.text)).getroot()


        card = sesh.post('https://checkout.shopifycs.com/pay', data=dict(forwardDoc.forms[2].form_values()))

        print('[{}] : {} - Reached card page, subbmiting card data...'.format(self.t(), name))

        cardDoc = parse(StringIO(card.text)).getroot()


        cardData = {
            'd': list(dict(cardDoc.forms[0].form_values()).values())[0],
            'checkout[credit_card][number]': cardNum.replace(' ', ''),
            'checkout[credit_card][name]': fName + ' ' + lName,
            'checkout[credit_card][month]': cardExpM,
            'checkout[credit_card][year]': cardExpY,
            'checkout[credit_card][verification_value]': cvv,
            'complete': '1'}

        cardHeaders = {
            'Host': 'elb.deposit.shopifycs.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://checkout.shopifycs.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://checkout.shopifycs.com/pay',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8'}

        cardSubmit = sesh.post('https://elb.deposit.shopifycs.com/sessions', data=cardData) #, headers = cardHeaders


        print('[{}] : {} - Subbmited card data, retreving url'.format(self.t(), name))

        sesh.get(cardSubmit.url)

        prossesing = cardSubmit.url[0:80] + 'processing'

        pros = sesh.get(prossesing)

        t2 = time.time()

        finalURL = pros.url


        if 'validate=true' in finalURL:
            print('[{}] : {} - Task complete, failed to submit order under url {}, total checkout time {}'.format(self.t(), name, finalURL, round(t2 - t1, 2)))

        elif 'thank_you' in finalURL:
            print('[{}] : {} - Task complete, Succsesfully submited order under url {}, total checkout time {}'.format(self.t(), name, finalURL, round(t2 - t1, 2)))

        else :
            print('[{}] : {} - Shit IDK, url {}, total checkout time {}'.format(self.t(), name, finalURL, round(t2 - t1, 2)))



data = {
    'email': 'SoleWing@gmail.com',
    'First name': 'Lyle',
    'Last name': 'Londraville',
    'Company': '',
    'Address 1': '3372 Brenner Road',
    'Address 2': '',
    'City': 'Norton',
    'State initals': 'OH',
    'State': 'Ohio',
    'Country initals': 'US',
    'Country': 'United States',
    'Zip': '44203',
    'Phone': '1 330-603-1362',
    'Card number': '4270 8290 3825 7603',
    'Card experation month': '9',
    'Card experation year': '2020',
    'Card cvv': '124'
}


i = AntiCaptcha("key here", "https://kith.com")
s = shopify()

now = datetime.datetime.now()
start = datetime.datetime(year = 2017, month = 4, day = 21, hour = 10, minute = 59)
timeElapsed = start - now
timeElapsedSec = timeElapsed.total_seconds()
time.sleep(timeElapsedSec)

print ('Done Sleeping, making captcha')

i.genCaptcha(5)
time.sleep(3)
i.genCaptcha(5)

print ('Done making captcha, searching for kw')

masterSizeDict = s.findSitemap([ 'kith', 'asic', 'volcano', 'gel', 'lyte'])

try :
    var = masterSizeDict[10.0]
except :
    var = masterSizeDict[(len(masterSizeDict.values())/2)]


print ('Starting {} threads...'.format(len(i.getGenList())))


for c in range(0,len(i.getGenList())):
    s.checkout(data, var, 'Kith volcano {}'.format(c), i.getGenList()[c])



