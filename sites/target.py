from bs4 import BeautifulSoup
from sites import Base
from datum import TARGET, returnStructure

class Target(Base):
    BASE_URL = 'https://www.targetfurniture.co.nz'
    VENDOR_NAME = "Target Furniture"
    CACHE = TARGET
    LISTING_URL = "?p={}"
    SEARCH_URL = "https://www.targetfurniture.co.nz/catalogsearch/result/index/?q={}"
    SEARCH_APPEND = "&p={}"

    def iterateListings(self, urls):
        results = []
        for url in urls:
            data = [self.completeLink(a.get("href", "")) for a in BeautifulSoup(self.get(url), "html.parser").\
                        find_all("a", {'class': "product-item-link"})]
            if len(data) == 0:
                break
            data = [a for a in data if a!= ""]
            results += data
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
            a = soup.find("span", {'itemprop': 'name'})
            if a:
                result["product_name"] = a.text.strip()
            a = soup.find("div", {'itemprop': 'sku'})
            if a:
                result["product_code"] = a.text.strip()
            a = soup.find("span", {'data-price-type': 'minPrice'})
            b = soup.find("span", {'data-price-type': 'maxPrice'})
            if a and b:
                result["price"] = a.text.strip() + " - " + b.text.strip()
            else:
                a = soup.find("span", {'data-price-type': 'finalPrice'})
                if a:
                    result["price"] = a.text.strip()
            a = soup.find("meta", {'itemprop': 'image'})
            if a:
                result["picture"] = a.get("content", "")
                result["picture"] = self.downloadMedia(result["picture"], self.VENDOR_NAME, result["product_name"], result["product_code"])
            a = soup.find("div", id = "dimensions_description_content")
            if a:
                result["dimensions"] = a.text.replace("\xa0", "").strip()
            a = soup.find("div", id = "details_description_content")
            if a:
                a = a.find("a", {'href': '/warranty'})
                if a:
                    result["warranty"] = a.text
            a = soup.find("div", id = "short_description_content")
            if a:
                result["description_and_specs"] = a.text.replace("\xa0", "")
            results.append(result)
        print("Scraped {} product(s).".format(len(listings)))
        return results