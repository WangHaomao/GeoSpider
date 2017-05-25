import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree

def get_soup_by_selenium(url):
    driver = webdriver.PhantomJS()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")

    driver.close()
    return soup

def get_soup_by_selenium_without_script(url):
    driver = webdriver.PhantomJS()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")
    [script.extract() for script in soup.findAll('script')]
    driver.close()
    return soup

def get_soup_by_request(url):

    req = requests.get(url)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text,"lxml")
    return soup

def get_soup_by_request_without_script(url):
    req = requests.get(url)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, "lxml")
    [script.extract() for script in soup.findAll('script')]
    return soup
def get_soup_by_html_source(html_source):
    return BeautifulSoup(html_source,"lxml")

def get_xpath_doc_by_request_by_url(url):
    req = requests.get(url)
    req.encoding = "utf-8"
    doc = etree.HTML(req)

    return doc

def get_xpath_doc_by_request_by_html_source(html_source):

    doc = etree.HTML(html_source)
    return doc