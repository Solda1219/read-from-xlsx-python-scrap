from bs4 import BeautifulSoup
from xpath_soup import *
import re
import requests
class PostScraper():
    def start(self):
        with open("all.html", encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, "html.parser")
            
            
            renewItem = soup.find('div', attrs={'id': 'renew'})

            timeItems = list(renewItem.children)
            flag = "monthly"
            cnt = 1
            ScrapData = []
            while cnt < len(timeItems):
                newItem = timeItems[cnt]
                if newItem.find('div', attrs={'class':'home_form_title'}).text.strip() == "شهرية":
                    flag = "monthly"
                elif newItem.find('div', attrs={'class':'home_form_title'}).text.strip() == "اسبوعية":
                    flag = "weekly"
                elif newItem.find('div', attrs={'class':'home_form_title'}).text.strip() == "يومية":
                    flag = "daily"
                elif newItem.find('div', attrs={'class':'home_form_title'}).text.strip() == "خدمة مددها":
                    flag = "extend"
                elif newItem.find('div', attrs={'class':'home_form_title'}).text.strip() == "تجديد":
                    flag = "renew old bundle"
                newItemDivs = newItem.findAll('div', attrs={'id':'bundleList'})
                

                for item in newItemDivs:
                    try:
                        item_id = item.find('input', attrs={'name': 'bundleId'}).attrs['value']
                    except:
                        item_id = " "
                    try:
                        item_description = item.find('input', attrs={'name': 'bundleName'}).attrs['value']
                    except:
                        item_description = " "
                    try:
                        item_xpath = item.find('img')
                        item_url = item.find('img').attrs['src']
                        xPath = xpath_soup(item_xpath)
                    except:
                        item_description = " "

                    item_autorenew = "True"
                    
                    tempText = self.translate(item_description)
                    print(tempText)
                    if tempText[-4:-2] == " u":
                        tempText = tempText[:-4] + " shekels"
                    tempArray = []
                    tempArray = re.split(r'([-+]?\d*\.\d+|\d+)', tempText)
                    i = 0
                    time = ""
                    price = "0"
                    minutes = "0"
                    ItemGB = "0"
                    message = "0"
                    while i < len(tempArray):
                        if tempArray[i].find("shekels") >= 0 or tempArray[i].find("NIS") >= 0:
                            price = re.findall('[-+]?\d*\.\d+|\d+', tempArray[i-1])[0]
                        if tempArray[i].find("minute") >= 0:
                            minutes = tempArray[i-1]
                        if tempArray[i].find("message") >= 0:
                            message = tempArray[i-1]
                        if tempArray[i].find("GB") >= 0:
                            ItemGB = tempArray[i-1]
                        time = flag
                        i = i + 1
                
                    new = (item_id, item_description, xPath, item_url, item_autorenew, time, price, minutes, ItemGB, message)
                    ScrapData.append(new)
                cnt = cnt + 2



            nonrenewItem = soup.find('div', attrs={'id': 'nonrenew'})

            nontimeItems = list(nonrenewItem)
            nonflag = "monthly"
            noncnt = 1
            
            while noncnt < len(nontimeItems):
                nonnewtime = nontimeItems[noncnt]
                if nonnewtime.find('div', attrs={'class':'home_form_title'}).text.strip() == "شهرية":
                    nonflag = "monthly"
                elif nonnewtime.find('div', attrs={'class':'home_form_title'}).text.strip() == "اسبوعية":
                    nonflag = "weekly"
                elif nonnewtime.find('div', attrs={'class':'home_form_title'}).text.strip() == "يومية":
                    nonflag = "daily"
                elif nonnewtime.find('div', attrs={'class':'home_form_title'}).text.strip() == "خدمة مددها":
                    nonflag = "extend"
                elif nonnewtime.find('div', attrs={'class':'home_form_title'}).text.strip() == "تجديد":
                    nonflag = "renew old bundle"
                nonnewItemDivs = nonnewtime.findAll('div', attrs={'id':'bundleList'})
                for item in nonnewItemDivs: 
                    # start scrap
                    try:
                        item_id = item.find('input', attrs={'name': 'bundleId'}).attrs['value']
                    except:
                        item_id = " "
                    try:
                        item_description = item.find('input', attrs={'name': 'bundleName'}).attrs['value']
                    except:
                        item_description = " "
                    try:
                        item_xpath = item.find('img')
                        item_url = item.find('img').attrs['src']
                        xPath = xpath_soup(item_xpath)
                    except:
                        item_description = " "

                    item_autorenew = "False"
                    
                    tempText = self.translate(item_description)
                    print(tempText)
                    if tempText[-4:-2] == " u":
                        tempText = tempText[:-4] + " shekels"
                    tempArray = []
                    tempArray = re.split(r'([-+]?\d*\.\d+|\d+)', tempText)
                    i = 0
                    time = " "
                    price = "0"
                    minutes = "0"
                    ItemGB = "0"
                    message = "0"
                    while i < len(tempArray):
                        if tempArray[i].find("shekels") >= 0 or tempArray[i].find("NIS") >= 0:
                            price = re.findall('[-+]?\d*\.\d+|\d+', tempArray[i-1])[0]
                        if tempArray[i].find("minute") >= 0:
                            minutes = tempArray[i-1]
                        if tempArray[i].find("GB") >= 0:
                            ItemGB = tempArray[i-1]
                        time = nonflag
                        i = i + 1
                
                    new = (item_id, item_description, xPath, item_url, item_autorenew, time, price, minutes, ItemGB, message)
                    ScrapData.append(new)
                noncnt = noncnt + 2
            for item in ScrapData:
                print(item, '\n')

    def translate(self, text):
        url = "http://api.phoneplay.me/api/v1/resources/tmp_translate?text="+ text

        payload={}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text
if __name__ == '__main__':
    scraper = PostScraper()
    scraper.start()

# ش.ض.ق.