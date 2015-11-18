from bs4 import BeautifulSoup
import urllib.request
import datetime

__MENSA_URL = "http://www.maxmanager.de/daten-extern/sw-giessen/html/speiseplan-render.php"
__NO_IMAGE_URL = "http://www.maxmanager.de/daten-extern/sw-giessen/html/fotos/big/4r17s_bild_folgt_foto!.jpg"
available_locations = {
    "mensa-otto-behaghel-strasse": ["mensa.*?behaghel"],
    "otto-eger-heim": [],
    "mensa-thm-in-giessen": ["mensa.*?thm", "thm.*?mensa", "thmensa"],
    "mensa-thm-in-friedberg": [],
    "fulda": [],
    "cafe-kunstweg": [],
    "campustor": [["thm", "kleine", "mensa"],"thm.*?kleine.*?mensa", "campustor"],
    "care": [],
    "cafeteria-ifz": [],
    "juwi": []
}


class MenuItem:
    """

    """

    def __init__(self, name, price, description="", counter=None, image=None):
        self.name = name
        self.price = price
        self.description = description
        self.counter = counter
        self.image = image


    def to_markdown(self):
        return "**%s** %s\n*%s€*" % (self.name, self.description, "€ / ".join(self.price))


    def __str__(self):
        return "%s: %s\nprice: %s\ncounter: %s\nimage: %s" % (self.name, self.description, self.price[0], self.counter, self.image)


def parseMenuItems(html):
    """

    :param html: raw html from "http://www.maxmanager.de/daten-extern/sw-giessen/html/speiseplaene.php"
    :return: MenuItems list parsed from html
    """

    result=[]
    parsed = BeautifulSoup(html, "html.parser")
    current_counter = None

    for row in parsed.find_all("tr"):
        name = None
        description = ""

        counter_tag = row.find("td", attrs={"class":"color-pk-dark"})

        if counter_tag is not None:
            current_counter = counter_tag.text

        price_tag = row.find("td", attrs={"class":"cell3"})

        if(price_tag is None or price_tag.text == "\n\xa0"):
            continue

        for title in row.find_all("span", attrs={"class":"artikel"}):
            name = title.contents[0]
            description_tag = title.find_next_sibling("span")

            for s in description_tag.contents:
                if isinstance(s, str):
                    description += s

        image = row.find("td", attrs={"class": "cell0"}).find("img")["src"]
        image = image.replace("html/fotos", "html/fotos/big")

        if image == __NO_IMAGE_URL:
            image = None

        price = price_tag.text.strip()
        price = price.split(" / ")

        result.append(MenuItem(name, price, description=description, counter=current_counter, image=image))

    return result


def _create_request_data(data:dict):
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')

    return data


def _read_html(url:str, data):
    request = urllib.request.Request(url, data)

    with urllib.request.urlopen(request) as response:
        return response.read()


def parse(location:str="mensa-thm-in-giessen", date:str=str(datetime.date.today())):
    """

    :param location: one of
    "mensa-otto-behaghel-strasse",
    "otto-eger-heim",
    "mensa-thm-in-giessen",
    "mensa-thm-in-friedberg",
    "fulda",
    "cafe-kunstweg",
    "campustor",
    "care",
    "cafeteria-ifz",
    "juwi"
    :param date:
    :return:
    """
    data = _create_request_data({'func': 'make_spl',
            'locId': location,
            'lang': 'de',
            'date': date})
    return parseMenuItems(_read_html(__MENSA_URL, data))


if __name__ == "__main__":
    for location in available_locations:
        print(location)
        for item in parse(location):
            # print(item)
            print(item.to_markdown())
            print("----------------------------------------")
