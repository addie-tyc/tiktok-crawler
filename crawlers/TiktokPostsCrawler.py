from datetime import datetime
import os
from typing import List

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
options.add_argument('--no-sandbox') # for error: DevToolsActivePort file doesn't exist
options.add_argument('--headless')  
options.add_argument('--disable-gpu')

class TiktokPostsCrawler(BaseTiktokCrawler):

    def __init__(self, links, driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)):
        super().__init__(driver=driver)
        assert links, 'There is no any link. Something went wrong.'
        self.links = links
        self.conn = pymysql.connect(
            host=os.getenv('SQL_HOST'),
            port=int(os.getenv('SQL_PORT')),
            user=os.getenv('SQL_USER'), 
            password=os.getenv('SQL_PWD'),
            db=os.getenv('SQL_DB')
            )
    
    def batch_crawl(self, watching_links) -> List[dict]:
        results = []
        self.links = list(set(self.links).union(set(watching_links)))
        for link in self.links:
            res = self.crawl(link)
            res['link'] = link
            res['post_id'] = int(link.split('/')[-1])
            results.append(res)
        self.driver.close()
        return results
    
    def crawl(self, url=None):
        self.driver.get(url)
        html = bs(self.driver.page_source, 'html.parser')
        targets = [
            ('div', {'data-e2e': 'browse-video-desc'})
        ]
        counts = [
            ('strong', {'data-e2e': 'like-count'}),
            ('strong', {'data-e2e': 'comment-count'}),
            ]
        res = self.parse_targets(html, targets, {})
        self.parse_targets(html, counts, res, convert_str_to_number)
        res['description'] = res.pop('browse_video_desc')
        return res
    
    def get_watching_links(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
            SELECT `link` FROM `posts` 
             WHERE `created` = (SELECT MAX(`created`) FROM `posts`);
            ''')
            links = [tup[0] for tup in cursor.fetchall()]
        return links

    def save_to_db(self, data: List[dict]):
        now = datetime.utcnow()
        for d in data:
            d['created'] = now
        columns = ', '.join(data[0].keys())
        placeholders = ')s, %('.join(data[0].keys())
        with self.conn.cursor() as cursor:
            sql = f"INSERT INTO `posts` ({columns}) VALUES (%({placeholders})s)"
            cursor.executemany(sql, data)
        self.conn.commit()
        self.conn.close()

    def run(self):
        watching_links = self.get_watching_links()
        res = self.batch_crawl(watching_links)
        self.save_to_db(res)
        return res
