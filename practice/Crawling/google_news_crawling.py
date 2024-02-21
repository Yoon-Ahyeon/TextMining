from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

word = input("검색하고자 하는 단어를 입력해주세요!")
url = 'https://www.google.com/search?q={}&newwindow=1&tbm=nws&ei=TUmuY5LlINeghwOfw7egDQ&start={}&sa=N&ved=2ahUKEwjSv42woqD8AhVX0GEKHZ_hDdQQ8tMDegQIBBAE&biw=763&bih=819&dpr=2.2'

import time
import random

page = 1

title_list = []
content_list = []
link_list = []

timesleep = random.randint(1, 10)

for i in range(0, 20, 10):
    new_url = url.format(word, i)
    driver.get(new_url)
    time.sleep(3)

    print("*" * 10 + str(page) + "*" * 10)
    page = page + 1
    
    # 제목 추출 안됨
    titles = driver.find_elements(By.CLASS_NAME, 'mCBkyc')

    for title in titles:
        title_list.append(title.text.replace(",", ""))

    contents = driver.find_elements(By.CLASS_NAME, 'GI74Re')

    for content in contents:
        content_list.append(content.text.replace(",", ""))

    links = driver.find_elements(By.CLASS_NAME, 'WlydOe')

    for link in links:
        link_list.append(link.get_attribute('href'))

print(title_list)
print(content_list)
print(link_list)