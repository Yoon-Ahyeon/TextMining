# Crawling
# 참고 : https://wonhwa.tistory.com/46

# 크롤링시 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import sys

# 페이지 url 형식에 맞게 바꾸어 주는 함수
def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num + 1
    else:
        return num + 9 * (num - 1)

# 크롤링할 url 생성 함수
def makeUrl(search, start_pg, end_pg):
    urls = []
    for i in range(start_pg, end_pg + 1):
        page = makePgNum(i)
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={search}&start={page}"
        urls.append(url)
    print("생성url: ", urls)
    return urls

# html에서 원하는 속성 추출 함수
def news_attrs_crawler(articles, attrs):
    return [i.get(attrs, None) for i in articles]

# ConnectionError 방지를 위한 헤더 설정
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

# html 생성해서 기사 크롤링하는 함수
def articles_crawler(single_url):
    original_html = requests.get(single_url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")

    url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    urls = news_attrs_crawler(url_naver, 'href')
    return urls

# 검색어, 시작 페이지, 종료 페이지 입력받기
search = input("검색할 키워드를 입력해주세요:")
start_page = int(input("\n크롤링할 시작 페이지를 입력해주세요. ex)1(숫자만입력):"))
end_page = int(input("\n크롤링할 종료 페이지를 입력해주세요. ex)1(숫자만입력):"))

# naver url 생성
urls = makeUrl(search, start_page, end_page)

# 뉴스 크롤링 실행
final_urls = []
for single_url in urls:
    article_urls = articles_crawler(single_url)
    final_urls.extend([url for url in article_urls if "news.naver.com" in url])

# 뉴스 제목과 내용 크롤링
news_titles = []
news_contents = []
news_dates = []

for url in tqdm(final_urls):
    news_html = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

    title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2, #articleTitle")
    content = news_html.select_one("#dic_area, #articleBodyContents")

    title_text = title.get_text(strip=True) if title else "제목을 찾을 수 없음"
    content_text = content.get_text(strip=True, separator=' ') if content else "내용을 찾을 수 없음"

    news_titles.append(title_text)
    news_contents.append(content_text)

    # 날짜 정보 추출
    # date_selector = news_html.select_one("span.t11")
    # news_date = date_selector.get_text() if date_selector else "날짜 정보 없음"
    # news_dates.append(news_date)

# 데이터 프레임 생성 및 저장
import pandas as pd
import os

# 데이터 프레임 생성
news_df = pd.DataFrame({'title': news_titles, 'content': news_contents, 'link': final_urls})
news_df = news_df.drop_duplicates(keep='first', ignore_index=True)

# 현재 시간을 기반으로 파일 이름 생성
now = datetime.datetime.now()
filename = f'{search}_{now.strftime("%Y%m%d_%H%M%S")}.csv'

# 저장하고자 하는 경로 설정
save_path = 'C:/Users/ahyeo/OneDrive/문서/바탕 화면/Project2024/TextMining/Crawling'  # Windows 예시

# 전체 경로에 파일 이름 추가
full_path = os.path.join(save_path, filename)

# 데이터 프레임을 CSV 파일로 저장
news_df.to_csv(full_path, encoding='utf-8-sig', index=False)

print(f"데이터가 성공적으로 저장되었습니다: {full_path}")