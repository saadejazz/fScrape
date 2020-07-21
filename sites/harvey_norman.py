from bs4 import BeautifulSoup
from sites import Base
from datum import HARVEY_NORMAN, returnStructure

class HarveyNorman(Base):
    BASE_URL = 'https://www.harveynorman.co.nz'
    VENDOR_NAME = "Harvey Norman"
    CACHE = HARVEY_NORMAN
    LISTING_URL = "page-{}"
    SEARCH_URL = "https://www.harveynorman.co.nz/index.php?subcats=Y&status=A&pshort=N&pfull=N&pname=Y&pkeywords=Y&search_performed=Y&q={}&dispatch=products.search"
    SEARCH_APPEND = "&page={}"
    
    def iterateListings(self, urls):
        results = []
        for url in urls:
            data = [a.get("href", "") for a in BeautifulSoup(self.get(url), "html.parser").\
                        find_all("a", {'class': "product-title"})]
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
            a = soup.find("h1", {'class': 'product-title'})
            if a:
                result["product_name"] = a.text.strip()
            a = soup.find("small", {'class': 'product-id meta'})
            if a:
                result["product_code"] = a.text.strip()
            a = soup.find("img", {'class': 'pict'})
            if a:
                result["picture"] = a.get("src", "")
                result["picture"] = "https:" + result["picture"] if result["picture"].startswith("//") else result["picture"]
                result["picture"] = self.downloadMedia( result["picture"], self.VENDOR_NAME, result["product_name"], result["product_code"])
            a = soup.find("span", {'class': 'price'})
            if a:
                result["price"] = a.text.strip()
            a = soup.find("div", id = "content_description")
            if a:
                a = a.find("div", {'class': 'product-tab-wrapper'})
                if a:
                    result["description_and_specs"] = "\n".join([x.text for x in a.find_all(lambda tag: tag.name in ["div", "p", "li"]) if x.text != ""]).replace("\xa0", "").strip()
                    result["dimensions"] = result["description_and_specs"].partition("Dimensions: ")[2].partition("\n")[0]
            anchors = ["Brand", "Product Type", "Made in"] 
            keys = ["brand", "product_type", "made_in"]
            for i in range(3):
                a = soup.find("th", text = anchors[i])
                if a:
                    a = a.findNext("td")
                    result[keys[i]] = a.text.strip()
            a = soup.find(lambda tag: "subheader" in tag.get("class", "") and "Warranty" in tag.text)
            if a:
                a = a.findNext("td")
                if a:
                    result["warranty"] = a.text.strip()
            a = soup.find(lambda tag: "subheader" in tag.get("class", "") and "Material" in tag.text)
            if a:
                a = a.findNext("td")
                if a:
                    result["material"] = a.text.strip()
            if result["dimensions"] == "":
                anchors = ["Product Depth", "Product Height", "Product Length"]
                keys = ["", "", ""]
                for i in range(3):
                    a = soup.find("th", text = anchors[i])
                    if a:
                        a = a.findNext("td")
                        keys[i] = a.text.strip()
                        result["dimensions"] = "L {} x W {} x H {}".format(keys[2], keys[0], keys[1])
            a = soup.find("span", {'itemprop': 'ratingValue'})
            if a:
                result["average_rating"] = f"{a.text} out of 5.0"
            results.append(result)
        print("Scraped {} product(s).".format(len(listings)))
        return results