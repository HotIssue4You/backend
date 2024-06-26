import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup as bs
from preproccesing import process, process_and_merge, print_title_dataFrame

"""
below imports from django 
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotissue4you.settings")
import django
import logging
from django.utils import timezone
django.setup()
from mainpage.models import Article

logger = logging.getLogger(__name__)

def get_news_data(url, user_agent, df):
    """
    네이버 뉴스 페이지의 최신 뉴스 10개를 스크래핑하여 df에 저장
    :param url: 네이버 뉴스 최신순 정렬 url
    :param user_agent:
    :param df: pandas dataframe
    :return: None
    """
    res = requests.get(url, user_agent)
    soup = bs(res.text, "lxml")
    news_list = soup.find("ul", "list_news _infinite_list").find_all("li", "bx")
    for news in news_list:
        news_contents = news.find("a", "news_tit")
        news_info = news.find_all("span", "info")
        time_info = news_info[-1]
        minutes = int(time_info.text[:-3])
        current = timezone.now()
        created_at = current - datetime.timedelta(minutes=minutes)
        df.loc[len(df)] = [news_contents['title'], created_at, news_contents['href'], time_info.text]


def save_page_rows_to_article(data):
    for idx, row in data.iterrows():
        Article(title=row['title'], noun_title=row['noun_title'], created_at=row['created_at']).save()


def main():
    url = ("https://search.naver.com/search.naver?where=news&query=%EB%89%B4%EC%8A%A4&sm=tab_opt&sort=1&photo=0&field"
           "=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so"
           "%3Add%2Cp%3Aall&is_sug_officeid=0&office_category=0&service_area=0")
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36"}
    df = pd.DataFrame(columns=['title', 'created_at', 'link_url', 'time_offset'])
    try:
        get_news_data(url, user_agent, df)
    except (KeyError, ValueError):
        logger.error("HTML 문서로부터 원하는 데이터를 가져오지 못 했습니다.")

        return
    processed = process(data=df)
    # processed = process_and_merge(data=df, now=timezone.now())
    save_page_rows_to_article(processed)
    print_title_dataFrame(processed)


if __name__ == "__main__":
    main()
