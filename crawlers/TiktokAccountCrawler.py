from datetime import datetime
import os

from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import pymysql.cursors

from crawlers.BaseTiktokCrawler import BaseTiktokCrawler
from logger import logger
from util import convert_str_to_number

load_dotenv()

class TiktokAccountCrawler(BaseTiktokCrawler):

    def __init__(self, account: str, driver):
        super().__init__(driver=driver)
        assert account[0] == '@', 'The account\'s format is invalid.'
        self.account = account
        self.url = f'https://www.tiktok.com/{self.account}'
        self.links = []
    
    def crawl(self, url=None) -> dict:
        self.driver.get(self.url)
        html = bs(self.driver.page_source, 'html.parser')
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
        self.links = self.get_latest_posts(html)
        logger.info(f'Get {len(self.links)} latest posts.')
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
        logger.info(f'`{data["user_title"]}` saved.')
        conn.commit()
        conn.close()

    def get_latest_posts(self, html, limit=5):
        posts = html.findAll('div', {'data-e2e': 'user-post-item'}, limit=limit)
        return [post.find('a')['href'] for post in posts]

    def run(self):
        res = self.crawl()
        self.save_to_db(res)
        return self.links
