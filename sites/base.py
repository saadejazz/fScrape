import requests
from utils import MyPool
from time import sleep
from conf import MAX_CONCURRENT_REQUESTS, MAX_PAGES_LISTING, RETRY_ATTEMPTS, RETRY_DELAY, DUMP
from urllib.parse import quote
import mimetypes
import random
import string
import os

class Base():
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    MAX_RETIRES = RETRY_ATTEMPTS
    RETRY_SLEEP = RETRY_DELAY
    MAX_WORKERS = MAX_CONCURRENT_REQUESTS
    MAX_PAGES = MAX_PAGES_LISTING
    START_PAGE = 1
    LISTING_URL = ""
    SEARCH_URL = ""
    SEARCH_APPEND = ""
    BASE_URL = ""
    CACHE = {}
    VENDOR_NAME = "No Vendor"
    category = ""
    DATA_DUMP = DUMP
    
    def get(self, url, gain = "text"):
        try:
            r = requests.get(url, headers = self.HEADERS)
            if r.status_code == 200:
                if gain == "text":
                    return r.text
                elif gain == "url":
                    return r.url
            else:
                return ''
        except requests.exceptions.RequestException as err:
            # retry once
            i = 1
            while(i <= self.MAX_RETIRES):
                print(err, f" Retrying (Attempt:{i})...")
                i += 1
                sleep(self.RETRY_SLEEP)
                try:
                    r = requests.get(url, headers = self.HEADERS)
                    if r.status_code == 200:
                        if gain == "text":
                            return r.text
                        elif gain == "url":
                            return r.url
                except requests.exceptions.RequestException as e:
                    print("Retrying did not work: ", e)
        return ""
        
    def getListings(self, category): 
        print("Extracting listings for {}".format(self.VENDOR_NAME))
        if type(category) == list:
            if len(category) == 0:
                return []
            pool = MyPool(processes = len(category))
            data = pool.map(self.listOnce, category)
            pool.close()
            res = [d for dat in data for d in dat]
        elif type(category) == str: 
            res = self.listOnce(category)
        links = []
        final = []
        for d in res:
            if d["link"] not in links:
                final.append(d)
                links.append(d["link"])
        print(f"Found {len(final)} products")
        return final
    
    def scrapeAll(self, listings):
        print("Scraping products for {}".format(self.VENDOR_NAME))
        chunks = self.chunk(listings, self.MAX_WORKERS)
        chunks = [a for a in chunks if a != []]
        if len(chunks) == 0:
            return []
        pool = MyPool(processes = len(chunks))
        data = pool.map(self.scrapeOnce, chunks)
        pool.close()
        return [d for dat in data for d in dat]              
        
    def listOnce(self, category):
        self.category = category
        category = category.split(":")
        try:
            assert(len(category) == 2)
        except AssertionError:
            print("Error encountered")
            return []
        
        if category[0] in self.CACHE:
            if category[1].strip() in self.CACHE[category[0]]:
                url = self.completeLink(self.CACHE[category[0]][category[1].strip()]) + self.LISTING_URL
                return self.getListingsFromUrl(url)
        
        self.categoryUndefinedError()
        return []
    
    def getListingsFromUrl(self, url):
        x = self.distWork(url)
        if len(x) == 0:
            return []
        pool = MyPool(processes = len(x))
        data = pool.map(self.iterateListings, x)
        pool.close()
        res = [d for dat in data for d in dat]
        res = list(set(res))
        res = ["https:" + d if d.startswith("//") else d for d in res]
        print("Scraped listings for category -> {}".format(self.category))
        return [{"category": self.category, "link": a} for a in res]
    
    def searchOnce(self, keyword):
        self.category = keyword
        print(f"Searching ----> {keyword}....")
        return self.getListingsFromUrl(self.SEARCH_URL.format(quote(keyword)) + self.SEARCH_APPEND)
    
    def search(self, category): 
        print("Extracting listings for {}".format(self.VENDOR_NAME))
        if type(category) == list:
            if len(category) == 0:
                return []
            pool = MyPool(processes = len(category))
            data = pool.map(self.searchOnce, category)
            pool.close()
            res = [d for dat in data for d in dat]
        elif type(category) == str: 
            res = self.searchOnce(category)
        links = []
        final = []
        for d in res:
            if d["link"] not in links:
                final.append(d)
                links.append(d["link"])
        print(f"Found {len(final)} products")
        return final
    
    def categoryUndefinedError(self):
        print("Category Not Found")
    
    @staticmethod
    def chunk(seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out
    
    def completeLink(self, link):
        if link.startswith("/"):
             link = self.BASE_URL + link
        return link
    
    @staticmethod
    def generate_random_code(N = 5):
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))
    
    def downloadMedia(self, url, vendor, name, code):
        try:
            try:
                os.makedirs(self.DATA_DUMP, exist_ok = True)
            except:
                pass
            r = requests.get(url)
            ext = mimetypes.guess_extension(r.headers['content-type'])
            filename = f"{self.DATA_DUMP}/{self.generate_random_code(10)}{ext}"
            while(os.path.exists(filename)):
                name = f"{self.DATA_DUMP}/{self.generate_random_code(10)}{ext}"
            with open(filename, "wb") as filex:
                filex.write(r.content)
            return filename
        except Exception as e:
            print("Exception: ", e)
            return ""

    @staticmethod
    def getFileNameFromUrl(url):
        return ".".join(url.split(".")[:-1]).split("/")[-1]
    
    def distWork(self, url):
        b = []
        for i in range(self.START_PAGE, self.MAX_WORKERS + 1):
            b.append([url.format(str(a)) for a in list(range(i, self.MAX_PAGES, self.MAX_WORKERS))])
        return b

    def scrapeOnce(self, url):
        raise NotImplementedError

    def iterateListings(self, url):
        raise NotImplementedError
