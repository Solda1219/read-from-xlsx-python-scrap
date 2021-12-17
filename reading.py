import json
import requests
from bs4 import BeautifulSoup
#import pandas as pd
import os
import math
import xlrd
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import time
import mysql.connector
import re

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gamepass"
)

mycursor = mydb.cursor()


def insertIntoDB(items):
    sql = "INSERT INTO articles (title, app_name, short_intro, description, old_price, price, published_by, developed_by, released_date, main_image, site_url, IDValue, dis_percentage, langValue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # sql = "INSERT INTO articles (title) VALUES (%s)"
    mycursor.execute(sql, items)
    # mycursor.execute(sql, items)

    mydb.commit()
    # columns=['title', 'app_name', 'short_intro', 'description', 'old_price', 'price', 'published_by', 'developed_by', 'released_date', 'main_image', 'site_url', 'IDValue', 'dis_percentage', 'langValue']
    #df = pd.DataFrame(items, columns = columns)
    #df.to_csv('result.csv', mode='a', header=False, index=False, encoding='utf-8')

class PostScraper():
    def __init__(self):
        self.base_url = "https://www.theice.com/products/197/EUA-Futures/data?marketId=5474735"   

    def start_scrape(self):
           # Open the Workbook
        workbook = xlrd.open_workbook("test.xls")
        language = xlrd.open_workbook("lang.xls")
        # Open the worksheet
        worksheet = workbook.sheet_by_index(0)
        lang = language.sheet_by_index(0)
        newValue = []
        newLang = []
        for i in range(8005, 8506): #count of ID
            newValue.append(worksheet.cell_value(i, 0))
        
        for i in range(0, 48): #language
            newLang.append(lang.cell_value(i, 0))
        
        # print(newLang)
        self.runs(newValue, newLang)
        # for line in lines:
        #     count += 1
        #     print(f'line {count}: {line}')

    # def headlessDriver(self):
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument("--window-size=1920, 900")
    #     chrome_options.add_argument("--hide-scrollbars")
    #     driver = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\FUTURE-2021\AppData\Local\Temp\BNZ.617848fb268f884\chromedriver.exe")
    #     return driver
    
    def runs(self, worksheet, language):
        url_list = []
        for valuedata in worksheet:
            for valuelang in language:
                # site_url = "https://www.microsoft.com/"+ valuelang +"/p/q/" + valuedata + "/?activetab=pivot:overviewtab"
                
                new = (site_url, valuedata, valuelang)
                url_list.append(new)
        self.select_scrap(url_list)

    def select_scrap(self, url_list):
        print('now scrape categorys... and inserting into sql database')
        print('this takes long time, maybe 8+hours..')
        print('after getting all categorys, will be returned all deepset urls and will scrape all products!')
        print('please wait!')
        # driver= self.headlessDriver()
        print('Please pass driver')
        items = []
        total_count = len(url_list)
        cnt = 0;
        b = "% performance"
        print(total_count)
        for value in url_list:
            # driver.get(value)
            # print(value)
            print(str(round(int(cnt)/int(total_count)*100, 2)) + b)
            response = requests.get(value[0])
            soup= BeautifulSoup(response.text, 'html.parser')
            # time.sleep(15)ss
            # soup = BeautifulSoup(driver.page_source, 'html.parser')
            title = soup.title.text
            
            try:
                app_name = soup.find('h1', attrs={'class': 'typography-module__xdsH1___zrXla'}).text.strip()
            except:
                app_name = " "
            try:
                site_url = "https://www.xbox.com/"+ valuelang +"/games/store/Forza-Horizon-4-Standard-Edition/" + valuedata
            except:
                site_url = " "
            try:
                short_intro = soup.find('div', attrs={'class': 'ProductDetailsHeader-module__productInfoLine___2pgrC'}).find('span', recursive=False).text
            except:
                short_intro = " "

            try:
                description = soup.find('p', attrs={'class':'typography-module__xdsBody2___1XDyq'}).text.strip()
            except:
                description = " "

            try:
                old_price = soup.find('span', attrs={'class':'Price-module__strikeThrough___WaylD'}).text.strip()
            except:
                old_price = " " 
            x = re.findall('[0-9]+', old_price)
            if len(x) > 1:
                oPrice = x[0]+""+x[1]
            else:
                oPrice = ""
            # print(oPrice)
            try:
                price = soup.find('span', attrs={'class':'Price-module__boldText___34T2w'}).text.strip()
            except:
                price = " "
            y = re.findall('[0-9]+', price)
            if len(y) > 1:
                nPrice = y[0]+""+y[1]
            else:
                nPrice = ""
            # print(nPrice)
            try:
                published_by = soup.find('div', attrs={'class':'Description-module__details___1w_c0'}).findAll('div', attrs={'class':'typography-module__xdsBody2___1XDyq'})[0].text
            except:
                published_by = " "

            try:
                developed_by = soup.find('div', attrs={'class':'Description-module__details___1w_c0'}).findAll('div', attrs={'class':'typography-module__xdsBody2___1XDyq'})[1].text
            except:
                developed_by = " "

            try:
                released_date = soup.find('div', attrs={'class':'Description-module__details___1w_c0'}).findAll('div', attrs={'class':'typography-module__xdsBody2___1XDyq'})[2].text
            except:
                released_date = " "

            try:
                main_image = soup.find('img', {'class':'ProductDetailsHeader-module__productImage___tT14m'}).attrs['src']
            except:
                main_image = " "
            try:
                site_url = value[0];
            except:
                site_url = " "
            try:
                IDValue = value[1];
            except:
                IDValue = " "
            try:
                LangValue = value[2];
            except:
                LangValue = " "
            dicsount_percentage = 0
            if oPrice.isdigit() == True and nPrice.isdigit() == True:
                dicsount_percentage = round((float(oPrice) - float(nPrice))/float(oPrice), 4) * 100
            # print(gallery_image)
            new = (title, app_name, short_intro, description, old_price, price, published_by, developed_by, released_date, main_image, site_url, IDValue, dicsount_percentage, LangValue)
            # new = (title)
            insertIntoDB(new)
            cnt = cnt + 1
        
        # insertIntoDB(items)
        # print(title, short)


    
    
    def import_data(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)

if __name__ == '__main__':
    scraper = PostScraper()
    scraper.start_scrape()