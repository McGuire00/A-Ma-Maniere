from datetime import datetime
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import string

# keeps track of how many accounts created
entries = 0


def clock():
    current = datetime.now()
    clock_format = current.strftime('%Y/%m/%d %I:%M:%S:%f')
    return str(clock_format) + " CST"


# list of names script will use to create account
names = [
'JAMES',
'JOHN',
'ROBERT',
'MICHAEL',
'WILLIAM',
'DAVID',
'RICHARD',
'CHARLES',
'JOSEPH',
'THOMAS',
'CHRISTOPHER',
'DANIEL',
'PAUL',
'MARK',
'DONALD',
'GEORGE',
'KENNETH',
'STEVEN',
'EDWARD',
'BRIAN',
'RONALD',
'ANTHONY',
'KEVIN',
'JASON'
]

print(clock(), 'Welcome')


def create():
    global entries
    s = requests.session()

    name = random.choice(names).title()
    name_extra = ''.join(random.choice(string.digits))
    rando_email = random.choice(string.digits) + name + name_extra + random.choice(string.digits) + '0@gmail.com'
    random_number = random.randint(1000, 9999)
    random_num = random.randint(100, 999)

    # example of email
    # John7John0@gmail.com

    # path to chromedriver
    path = '/Users/something/something/something/'


    options = Options()
    #options.headless = True
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(path, options=options)

    driver.get('https://www.a-ma-maniere.com/account/register')

    # params used to create account with
    first = driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(name)
    last = driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(name)
    mail = driver.find_element_by_xpath('//*[@id="email"]').send_keys(rando_email)

    # insert the password you would like created accounts to have
    password = driver.find_element_by_xpath('//*[@id="password"]').send_keys('Qweradsaf12')

    register = driver.find_element_by_xpath('//*[@id="create_customer"]/div[2]/div[2]/button').click()

    # 2captcha to automatically complete recaptcha
    # sitekey to A Ma Maniere
    site_key = "6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF"
    # insert your 2captcha API key here
    api_key = ''

    form = {"method": "userrecaptcha",
            "googlekey": site_key,
            "key": api_key,
            "pageurl": 'https://www.a-ma-maniere.com/challenge',
            "json": 1}

    response = requests.post('http://2captcha.com/in.php', data=form)
    request_id = response.json()['request']


    url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"

    # continously check if captcha has been solved
    status = 0
    while not status:
        res = requests.get(url)
        if res.json()['status'] == 0:
            print(clock(), ':: sleeping for 3 seconds')
            time.sleep(3)
        else:
            print(clock(), ':: captcha solved')
            requ = res.json()['request']  # this is the token
            js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'  # submits token
            driver.execute_script(js)
            driver.find_element_by_xpath('/html/body/main/div/form/input[2]').submit()
            status = 1

    # this part of the script handles submitting raffle entries
    # insert link here to fill out raffle
    driver.get('https://www.a-ma-maniere.com/collections/releases/products/air-jordan-1-neutral-grey')
    time.sleep(3)

    size_select = driver.find_element_by_xpath('//*[@id="shopify-section-product-releases-template"]/section/div[2]/div/div[3]/h4').click()
    driver.execute_script("window.scrollTo(1000, 800)")
    size = driver.find_element_by_xpath('//*[@id="size_options"]/div[12]/label')
    driver.execute_script("arguments[0].click();", size)
    driver.implicitly_wait(5)


    # size 8 xpath //*[@id="size_options"]/div[10]/label
    # size 9 xpath //*[@id="size_options"]/div[12]/label
    # size 9.5 //*[@id="size_options"]/div[13]/label
    # size 10 xpath //*[@id="size_options"]/div[14]/label

    driver.execute_script("window.scrollTo(50,document.body.scrollHeight)")
    time.sleep(2)
    select_address = driver.find_element_by_xpath('//*[@id="form-shipping"]').click()
    driver.implicitly_wait(5)
    country = driver.find_element_by_xpath('//*[@id="shipping__country"]').find_element_by_xpath('//*[@id="shipping__country"]/option[237]').click()

    # you can change area code prefix if you like
    phone_number = driver.find_element_by_xpath('//*[@id="shipping__phone"]').send_keys('832{}{}'.format(random_num,random_number))

    # insert shipping city
    city = driver.find_element_by_xpath('//*[@id="shipping__city"]').send_keys('New York')

    # insert shipping address
    address = driver.find_element_by_xpath('//*[@id="shipping__address"]').send_keys('123 Main St')

    # insert state
    state = driver.find_element_by_xpath('//*[@id="shipping__state"]').send_keys('New York')

    # insert zip code
    zip = driver.find_element_by_xpath('//*[@id="shipping__postcode"]').send_keys('12345')

    submit_addy = driver.find_element_by_xpath('//*[@id="form-shipping"]/div/div[4]/button').submit()
    time.sleep(3)

    iframe = driver.find_element_by_xpath("//*[@id='card_number']/div/iframe")
    driver.switch_to.frame(iframe)
    # this is where your credit card number goes
    card = "1234567891232456"
    credit = driver.find_element_by_xpath('//*[@id="root"]/form/span[2]/div/div[2]/span/input').send_keys(card)
    driver.switch_to.default_content()
    driver.implicitly_wait(5)

    driver.switch_to.frame(driver.find_element_by_css_selector('#card_expires > div > iframe'))
    # exp date
    exp = driver.find_element_by_xpath('//*[@id="root"]/form/span[2]/span/input').send_keys('12/21')
    driver.switch_to.default_content()


    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="card_code"]/div/iframe'))
    # security code on card
    cvv = driver.find_element_by_xpath('//*[@id="root"]/form/span[2]/span/input').send_keys('123')
    driver.switch_to.default_content()


    submit_info = driver.find_element_by_css_selector('#form-release > button').click()
    time.sleep(5)
    # this is to check button after click
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    button = soup.find('button', attrs={'class':'btn btn-primary btn-entry'}).text
    print(clock(), ':: {}'.format(button))
    # sometimes the site jumbles credit card number and idk why
    # in the case of this event the code below runs and it simply quits the browser
    # if you want you can insert a sleep function under the submit button which buys time for you to correct the jumbled mistake
    if button == 'ENTRY DRAW':
        driver.quit()

    if button == 'Entry Created!':
        entries += 1
        print(clock(), ':: {} entries submitted'.format(entries))
        driver.quit()
        # insert file path here to save the emails of accounts created
        with open('/Users/something/something/something.txt', 'a') as file:
            file.write('\n')
            file.write(rando_email)


while True:
    create()

# if raffle == 'live':
#     eat

