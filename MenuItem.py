from bs4 import BeautifulSoup
import string

class MenuItem:
    """

    """

    def __init__(self, name, price, description="", counter=None):
        self.name = name
        self.price = price
        self.description = description
        self.counter = counter


def parseMenuItems(html):
    """

    :param html: raw html from "http://www.maxmanager.de/daten-extern/sw-giessen/html/speiseplaene.php"
    :return: MenuItems list parsed from html
    """

    result=[]
    parsed = BeautifulSoup(html, "html.parser")

    for row in parsed.find_all("tr"):
        name = None
        description = ""

        price_tag = row.find("td", attrs={"class":"cell3"})

        if(price_tag is None or price_tag.text == "\n\xa0"):
            continue

        for title in row.find_all("span", attrs={"class":"artikel"}):
            name = title.contents[0]
            description_tag = title.find_next_sibling("span")

            for s in description_tag.contents:
                if isinstance(s, str):
                    description += s

        price = price_tag.text.strip()
        price = price.split(" / ")

        result.append(MenuItem(name, price, description))

    return result


if __name__ == "__main__":
    import urllib.request

    html=None

    url = "http://www.maxmanager.de/daten-extern/sw-giessen/html/speiseplan-render.php"
    data = {'func':'make_spl',
            'locId':'mensa-thm-in-giessen',
            'lang':'de', 'date':'2015-11-17'}

    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')

    request = urllib.request.Request(url, data)

    with urllib.request.urlopen(request) as response:
        html = response.read()

    print("thm-mensa")

    for item in parseMenuItems(html):
        print(vars(item))

    data = {'func':'make_spl',
            'locId':'campustor',
            'lang':'de', 'date':'2015-11-17'}

    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')

    request = urllib.request.Request(url, data)

    with urllib.request.urlopen(request) as response:
        html = response.read()

    print("campustor")

    for item in parseMenuItems(html):
        print(vars(item))
