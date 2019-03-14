#load webdriver function from selenium
from selenium import webdriver
from time import sleep
import csv, sys

app_name = sys.argv[1] #'pl.bzwbk.bzwbk24'
max_showmore_iterations = 2

#Setting up Chrome webdriver Options
chrome_options = webdriver.ChromeOptions()

#setting  up local path of chrome binary file 
chrome_options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

#creating Chrome webdriver instance with the set chrome_options
driver = webdriver.Chrome(chrome_options=chrome_options)
link = "https://play.google.com/store/apps/details?id={}".format(app_name)
driver.get(link)

#MAIN BODY
maindiv = driver.find_element_by_xpath('//body/div/div[@jsname]/c-wiz/div[1]/div[2]/div[1]/div[1]/div[1]')
# print(maindiv.get_attribute('class'))

#APP TITLE
Ptitle = driver.find_element_by_xpath('//body/div/div[@jsname]/c-wiz/div[1]/div[2]/div[1]/div[1]/div[1]/c-wiz/c-wiz/div[1]/div[2]/div[1]/div[1]/c-wiz/h1/span')
print(Ptitle.get_attribute('innerHTML'))

#Read All reviews
maindiv = driver.find_element_by_xpath('//body/div/div[@jsname]/c-wiz/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[@jsaction]').click()
sleep(0.5)

#SORT BY NEWEST
driver.find_element_by_xpath('//*/body/div/div[last()]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div/div[2]/c-wiz/div/div').click()
sleep(1)
driver.find_element_by_xpath('//*/body/div/div[last()]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div/div[2]/c-wiz/div/div/div[2]/div[1]').click()
# maindiv = driver.find_element_by_xpath('//body/div/div[last()]/c-wiz[2]/div[1]/div[2]/div/div/div/div[@jscontroller]/div/div[@jsname]/div[1]')
# print (maindiv.get_attribute('class'))

for z in range(max_showmore_iterations):
    print ('proceeding iteration ', z)
    #scroll - atleast 3 times needed
    for i in range(5):
        maindiv = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[2]/c-wiz[1]/c-wiz/c-wiz/div/div[1]/div[1]/a/h2')
        #driver.find_element_by_xpath('//body/div/div[last()]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div/div[3]')
        driver.execute_script("arguments[0].scrollIntoView();", maindiv)
        print ("scrolled")
        sleep(2) #This could potentially be increased on very large iteration numbers
        driver.execute_script("window.scrollTo(0, 0)")
    #clicking - show more
    try:

        maindiv = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div').click()
        #'//body/div/div[last()]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div').click()
    except:
        break

reviews_list = []
reviews = driver.find_elements_by_xpath('//body/div/div[last()]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div/*')   
#Works slowly as hell - possibly BS4 equivalent based on class name could be faster
for element in reviews:
    try:
        user = element.find_element_by_xpath('.//div/div[2]/div[1]/div[1]/span').get_attribute('innerHTML')
        stars = element.find_element_by_xpath('.//div/div[2]/div[1]/div[1]/div/span[1]/div/div').get_attribute('aria-label')
        # text is 'Rated 4 stars out of five stars'
        stars = stars[6:7]
        date = element.find_element_by_xpath('.//div/div[2]/div[1]/div[1]/div/span[2]').text
        text = element.find_element_by_xpath('.//div/div[2]/div[@jscontroller]/span').text 
        lat_date = None
        print (date)

        for x in text:
            try:
                x = x.encode('utf-8')
            except UnicodeEncodeError:
                x = ''
        reviews_list.append([user,stars,date,text.replace(',','')])
    except:
        print ('processing error')
        continue
    # print (stars.encode('utf-8'), date.encode('utf-8'), text.encode('utf-8'))

with open('{}_android_reviews.csv'.format(app_name), 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    for x in reviews_list:
        try:
            writer.writerow([s for s in x])
        except UnicodeEncodeError:
            continue

driver.close()
    
