from bs4 import BeautifulSoup
from sites import Base
from datum import TSB_LIVING, returnStructure

class TsbLiving(Base):
    BASE_URL = 'https://www.tsbliving.co.nz'
    VENDOR_NAME = "TSB Living"
    CACHE = TSB_LIVING
    LISTING_URL = "?page={}"
    SEARCH_URL = "https://www.tsbliving.co.nz/search?type=product&q={}"
    SEARCH_APPEND = "&page={}"
    
    def iterateListings(self, urls):
        results = []
        for url in urls:
            data = BeautifulSoup(self.get(url), "html.parser").find_all("div", {'class': "product-title"})
            if len(data) == 0:
                break
            data = [a for a in data if a!= ""]
            for dat in data:
                a = dat.find("a")
                if a:
                    results.append(self.completeLink(a.get("href", "")))
        return results 
    
    def scrapeOnce(self, listings):
        results = []
        for li in listings:
            url = li["link"]
            soup = BeautifulSoup(self.get(url), "html.parser")
            result = returnStructure()
            result["vendor_name"] = self.VENDOR_NAME
            result["product_category"] = li["category"]
            result["product_link"] = url
            a = soup.find("h1", {'class': 'title'})
            if a:
                result["product_name"] = a.text.strip()
            a = soup.find(lambda tag: "/products/" in tag.get("src", ""))
            if a:
                result["picture"] = a.get('src', "")
                if result["picture"].startswith("//"):
                    result["picture"] = "https:" + result["picture"]
                    result["picture"] = self.downloadMedia(result["picture"], self.VENDOR_NAME, result["product_name"], result["product_code"])
            a = soup.find(lambda tag: tag.get("data-average-rating"))
            if a:
                result["average_rating"] = a.get("data-average-rating", "")
                if result["average_rating"] != "":
                    result["average_rating"] += " out of 5.00"
            a = soup.find(True, id = "price-preview")
            if a:
                result["price"] = a.text.strip()
            a = soup.find("div", id = "desc")
            if a:
                result["description_and_specs"] = BeautifulSoup(str(a).replace("<br/>", "\n"), "html.parser").text
            a = soup.find(True, id = "warranty")
            if a:
                result["warranty"] = BeautifulSoup(str(a).replace("<br/>", "\n"), "html.parser").text
            if result["description_and_specs"] != "":
                result["dimensions"] = result["description_and_specs"].partition("Dimension:")[2].partition("\n")[0].strip()
            a = soup.find("li", {'class': 'tags'})
            if a:
                a = a.find_all("a")
                if len(a) > 0:
                    a = a[-1]
                    result["product_type"] = a.text.strip()
            results.append(result)
        print("Scraped {} product(s).".format(len(listings)))
        return results