from datetime import datetime
from types import FunctionType
from typing import List, Tuple
import os

from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import pymysql.cursors
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from crawlers.BaseTiktokCrawler import BaseTiktokCrawler
from util import convert_str_to_number

load_dotenv()

options = Options() 
options.add_argument('--headless')  
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)

class TiktokAccountCrawler(BaseTiktokCrawler):

    def __init__(self, account: str, driver=driver):
        super().__init__(driver=driver)
        assert account[0] == '@', 'The account\'s format is invalid.'
        self.account = account
        self.url = f'https://www.tiktok.com/{self.account}'
    
    def crawl(self, url=None) -> dict:
        self.driver.get(self.url)
        html = bs(self.driver.page_source, 'html.parser')
        self.driver.close()
        targets = [
                ('h2', {'data-e2e': 'user-title'}),
                ('h1', {'data-e2e': 'user-subtitle'}),
                ('h2', {'data-e2e': 'user-bio'}),
            ]
        counts = [
            ('strong', {'data-e2e': 'following-count'}),
            ('strong', {'data-e2e': 'followers-count'}),
            ('strong', {'data-e2e': 'likes-count'})
        ]
        res = self.parse_targets(html, targets, {})
        self.parse_targets(html, counts, res, convert_str_to_number)
        return res

    def parse_targets(self, html: bs, targets: List[Tuple[str, dict]], res: dict, transform_fn: FunctionType=None) -> dict:
        for tag, cond in targets:
            key = list(cond.values())[0].replace('-', '_')
            res[key] = html.find(tag, cond).text
            if transform_fn:
                res[key] = transform_fn(res[key])
        return res
    
    def save_to_db(self, data: dict):
        conn = pymysql.connect(
            host=os.getenv('SQL_HOST'),
            port=int(os.getenv('SQL_PORT')),
            user=os.getenv('SQL_USER'), 
            password=os.getenv('SQL_PWD'),
            db=os.getenv('SQL_DB')
            )
        data['created'] = datetime.utcnow()
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        with conn.cursor() as cursor:
            sql = 'INSERT INTO `accounts_info` (%s) VALUES (%s)' % (columns, placeholders)
            cursor.execute(sql, list(data.values()))
        conn.commit()
    
    def run(self):
        res = self.crawl()
        print(res)
        self.save_to_db(res)
