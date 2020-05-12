from selenium import webdriver
from time import sleep as sl
import csv

driver = webdriver.Chrome()
driver.get("https://www.dcard.tw/forum/all")
sl(1)
r_list = driver.find_elements_by_xpath('//*[@id="__next"]/div[2]/div[2]/div/div/div/div/div/a')
forumList = []
hrefList = []

for i in r_list:
    forumList.append(i.text)
    hrefList.append(i.get_attribute('href'))
obj = open("forum.csv", "a+", encoding="utf-8")
writer = csv.writer(obj)

for a, b in zip(forumList, hrefList):
    writer.writerow([a.replace("追蹤","").replace("\n","").replace(" ",""),b])

driver.quit()