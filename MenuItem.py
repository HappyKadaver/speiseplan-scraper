from bs4 import BeautifulSoup

class MenuItem:
    """

    """

    def __init__(self, name, price, description="", counter=None):
        self.name = name
        self.price = price
        self.subtext = description
        self.counter = counter


def parseMenuItems(html):
    """

    :param html: raw html from "http://www.maxmanager.de/daten-extern/sw-giessen/html/speiseplaene.php"
    :return: MenuItems list parsed from html
    """

    result=[]
    parsed = BeautifulSoup(html, "html.parser")

    for article in parsed.find_all("span", attrs={"class":"artikel"}):
        result.append(MenuItem(article.contents[0], -1))

    return result


if __name__ == "__main__":
    import urllib.request

    html=None

    url = "http://www.maxmanager.de/daten-extern/sw-giessen/html/speiseplan-render.php"
    data = {'func':'make_spl',
            'locId':'mensa-thm-in-giessen',
            'lang':'de', 'date':'2015-11-16'}

    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')

    request = urllib.request.Request(url, data)

    with urllib.request.urlopen(request) as response:
        html = response.read()

    for item in parseMenuItems(html):
        print(vars(item))
