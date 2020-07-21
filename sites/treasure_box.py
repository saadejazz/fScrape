from bs4 import BeautifulSoup
from sites import Base
from datum import TREASURE_BOX, returnStructure

class TreasureBox(Base):
    BASE_URL = 'https://www.treasurebox.co.nz'
    VENDOR_NAME = "Treasure Box"
    CACHE = TREASURE_BOX
    LISTING_URL = "?p={}"
    SEARCH_URL = "https://www.treasurebox.co.nz/catalogsearch/result/?q={}"
    SEARCH_APPEND = "&p={}"
    
    def iterateListings(self, urls):
        results = []
        for url in urls:
            data = BeautifulSoup(self.get(url), "html.parser").find_all("h2", {'class': "product-name"})
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
            result = returnStructure()
            a = soup.find("div", {'class': 'breadcrumbs'})
            if a:
                a = a.find_all('li')
                if len(a) > 1:
                    a = a[-2]
                    result["product_type"] = a.text.strip()
            a = soup.find("div", {'class': 'product-name'})
            if a:
                result["product_name"] = a.text.strip()
            a = soup.find("div", {'class': 'product_sku'})
            if a:
                result["product_code"] = a.text.partition("SKU:")[2].strip()
            a = soup.find("meta", {'itemprop': 'price'})
            if a:
                result["price"] = "$" + a.get("content", "")
            a = soup.find("img", {'class': 'product_image_zoom'})
            if a:
                result["picture"] = a.get("src", "")
                result["picture"] = self.downloadMedia(result["picture"], self.VENDOR_NAME, result["product_name"], result["product_code"])
            a = soup.find("span", {'class': 'review-numerical'})
            if a:
                result["average_rating"] = a.text.strip()
            a = soup.find("div", id = 'tab_description_tabbed_contents')
            if a:
                result["description_and_specs"] = "\n".join([x.text for x in a.find_all(lambda tag: tag.name in ["div", "p", "li"]) if x.text != ""]).replace("\xa0", "").strip()
                for k in ["product-specifications", 'product-features']:
                    a = soup.find('ul', {'class': k})
                    if a:
                        s = str.capitalize(k.split("-")[1])
                        result["description_and_specs"] += f"\n{s}: \n" 
                        result["description_and_specs"] += "\n".join([y.text for y in a.find_all(lambda tag: tag.name in ["div", "p", "li"]) if y.text != ""]).replace("\xa0", "").strip()
            data = ["Product Dimensions", "Material", "Brand:"]
            keys = ["dimensions", "material", "brand"]
            for i in range(2):
                a = soup.find(lambda tag: data[i] in tag.text and tag.name in ["p", "li"])
                if a:
                    result[keys[i]] = a.text.partition(":")[2].strip()
            results.append(result)
        print("Scraped {} product(s).".format(len(listings)))
        return results