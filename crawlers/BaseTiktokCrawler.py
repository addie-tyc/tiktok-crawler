import abc

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from util import convert_str_to_number

class BaseTiktokCrawler(metaclass=abc.ABCMeta):
    def __init__(self, driver=None):
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
