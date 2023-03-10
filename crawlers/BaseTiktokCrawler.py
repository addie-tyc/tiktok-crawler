import abc
from types import FunctionType
from typing import List, Tuple

from bs4 import BeautifulSoup as bs

from logger import logger

class BaseTiktokCrawler(metaclass=abc.ABCMeta):
    def __init__(self, account, driver=None):
        assert account[0] == '@', 'The account\'s format is invalid.'
        self.account = account
        assert driver, 'The driver has not be assigned.'  
        self.driver = driver
    
    @abc.abstractmethod
    def crawl(self, url=None):
        return NotImplemented

    @abc.abstractmethod
    def save_to_db(self, data: dict):
        return NotImplemented

    @abc.abstractmethod
    def run(self):
        return NotImplemented

    def parse_targets(self, html: bs, targets: List[Tuple[str, dict]], res: dict, transform_fn: FunctionType=None) -> dict:
        for tag, cond in targets:
            key = list(cond.values())[0].replace('-', '_')
            try:
                res[key] = html.find(tag, cond).text.strip()
                if transform_fn:
                    res[key] = transform_fn(res[key])
            except AttributeError:
                logger.warn("'NoneType' object has no attribute 'text.' The post may be deleted.")
                res[key] = None
        return res
