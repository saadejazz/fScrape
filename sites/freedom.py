from bs4 import BeautifulSoup
from sites import Base
from datum import FREEDOM, returnStructure
from urllib.parse import quote

class Freedom(Base):
    BASE_URL = 'https://www.freedomfurniture.co.nz'
    VENDOR_NAME = "Freedom"
    CACHE = FREEDOM
    LISTING_URL = "[{}].htm"
    SEARCH_URL = "https://www.freedomfurniture.co.nz/default.aspx?q={}"
    SEARCH_APPEND = "&page={}"

    def searchOnce(self, keyword):
        url = self.get(self.SEARCH_URL.format(quote(keyword)), gain = "url")
        self.category = keyword
        if "default.aspx?" in url:
            url += self.SEARCH_APPEND
        else:
            url += self.LISTING_URL
        return self.getListingsFromUrl(url)
        
    def iterateListings(self, urls):
        links = []
        for url in urls:
            soup = BeautifulSoup(self.get(url), "html.parser").find_all("div", {'class': 'item'})
            if len(soup) == 0:
                break
            for a in soup:
                s = a.find("a")
                if s:
                    links.append(self.completeLink(s.get("href", "")))
        links = [a for a in links if a != ""]
        return links

    def scrapeOnce(self, listings):
        results = []
        for li in listings:
            url = li["link"]
            soup = BeautifulSoup(self.get(url), "html.parser")
            result = returnStructure()
            result["vendor_name"] = self.VENDOR_NAME
            result["product_category"] = li["category"]
            result["product_link"] = url
            a = soup.find_all("a", {'itemprop': 'url'})
            if a != []:
                a = a[-1]
                a = a.find("span")
                if a:
                    result["product_type"] = a.text.strip()
            a = soup.find("h1", {'itemprop': 'name'})
            if a:
                result["product_name"] = a.text.strip()
                if result["product_name"] == "":
                    continue
            a = soup.find("div", {'class': 'content long-description'})
            if a:
                result["description_and_specs"] = a.text.strip()
            a = soup.find("span", {'class': 'price-display'})
            if a:
                result["price"] = a.text.strip()
            a = soup.find("p", {'class': 'style-number'})
            if a:
                result["product_code"] = a.text.partition(":")[2].strip()
            a = soup.find("li", {'class': 'main top-product default'})
            if a:
                a = a.find("img")
                if a:
                    result["picture"] = self.completeLink(a.get('src', ""))
                    result["picture"] = self.downloadMedia(result["picture"], self.VENDOR_NAME, result["product_name"], result["product_code"])
            a = soup.find("dl")
            if a:
                w = soup.find("dt", text = "Dimension - Width:")
                if w:
                    w = w.findNext("dd").text
                d = soup.find("dt", text = "Dimension - Depth:")
                if d:
                    d = d.findNext("dd").text
                h = soup.find("dt", text = "Dimension - Height:")
                if h:
                    h = h.findNext("dd").text
                chk = [type(a) for a in [w, d, h]]
                if None not in chk:
                    result["dimensions"] = "W {} x D {} x H {}".format(w, d, h)
                w = soup.find("dt", text = "Material:")
                if w:
                    result["material"] = w.findNext("dd").text.strip()
            a = soup.find("div", {'class': 'stars-container'})
            if a:
                result["average_rating"] = a.get("title", "")
            results.append(result)
        print("Scraped {} product(s).".format(len(listings)))
        return results