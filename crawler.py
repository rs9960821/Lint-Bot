from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep as sl

class crawler:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.__driver = webdriver.Chrome(chrome_options = chrome_options)
        self.__information = """Dcard 看板搜尋小幫手，請輸入看板名稱，讓我幫您搜尋文章唷！"""

    @property   #回傳information
    def information(self):
        return self.__information

    def __close(self):
        self.__driver.quit()

    def get_forumList(self):
        forumList = []
        with open("forum.csv","r", encoding="utf-8") as f:
            for line in f.readlines():
                if line == "\n":
                    continue
                forumList.append(line)
        return forumList

    def crawl_specific_forum(self,name):
        L_list = ['你好','您好','妳好','hi','Hi','HI','早安','午安','晚安','安','安安','嗨嗨','嗨']
        forumList = self.get_forumList()
        userForumLink = ""
        for forum in forumList:
            if forum.split(",")[0] in name:
                userForumLink = forum.split(",")[1]
                break
            elif name in L_list:
                break
        else:
            self.__close()
            return "我找不到相關看板，再檢查看看名稱是不是錯了！"
        self.__driver.get(userForumLink)
        sl(1)
        if self.__driver.find_elements_by_xpath('/html/body/div[2]/div/div[2]/div/div/footer/div[2]/button'):
            button = self.__driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/footer/div[2]/button')
            button.click()
            sl(0.1)
        articleList = self.__driver.find_elements_by_xpath('//*[@id="__next"]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div')
        xStr = ""
        notArticleList = ["公告","版規","瀏覽此看板"]
        for article in articleList:
            try:
                title = "標題 :" + article.find_element_by_xpath('./article/h2/a/span').text
                if [i for i in notArticleList if i in title]:
                    continue
                hyperLink = "連結 : " + article.find_element_by_xpath('./article/h2/a').get_attribute('href')
                time = "日期 : " + article.find_element_by_xpath('./article/div[1]/div/div[2]/span[2]').text
                feel = "心情 : " + article.find_element_by_xpath('./article/div[3]/div[1]/div/div[2]').text
                answer = "留言 : " + article.find_element_by_xpath('./article/div[3]/div[2]/span[2]').text
                articleString = "\n".join([title,hyperLink,time,feel,answer])
                xStr += articleString + "\n" + ('-'*30)+"\n"
            except Exception as e:
                pass
        self.__close()
        return xStr

# L_list = ['你好','您好','妳好','hi','Hi','HI','早安','午安','晚安','安','安安','嗨嗨','嗨']
# name = "妳好"
# forumList = ['123', '331']
# for forum in forumList:
#     if forum in name:
#         print(forum)
#         break
#     elif name in L_list:
#         print(name)
#         break

# else:
#     print('no')

    # def crawl_hot(self):
    #     self.__driver.get("https://www.dcard.tw/f")
    #     articleList = self.__driver.find_elements_by_xpath('//*[@id="__next"]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div/article')
    #     xStr = ""
    #     for article in articleList:
    #         try:
    #             forum = "看板：" + article.find_element_by_xpath('./div[1]/div/div[2]/span[1]').text
    #             title = "標題：" + article.find_element_by_xpath('./div[2]/h2/a').text
    #             hyperLink = "連結：" + article.find_element_by_xpath('./div[2]/h2/a').get_attribute('href')
    #             feel = "心情：" + article.find_element_by_xpath('./div[3]/div[1]/div/div[2]').text
    #             answer = "回應：" + article.find_element_by_xpath('./div[3]/div[2]/span[2]').text
    #             articleString = "\n".join([forum,title,hyperLink,feel,answer]) 
    #             xStr += articleString + "\n" + ('-'*28) +"\n"
    #         except Exception as e:
    #             pass
    #     self.__close()
    #     return xStr

    # def crawl_popular(self):
    #     self.__driver.get("https://www.dcard.tw/forum/popular")
    #     sl(0.1)
    #     forumList = self.__driver.find_elements_by_xpath('//*[@id="__next"]/div[2]/div[2]/div/div/div/div/div/a/div[1]/div[2]')
    #     hrefList = self.__driver.find_elements_by_xpath('//*[@id="__next"]/div[2]/div[2]/div/div/div/div/div/a')
    #     xStr = ""
    #     for forum,href in zip(forumList,hrefList):
    #         xStr += forum.text + "\n" + href.get_attribute('href') + "\n"
    #     return xStr