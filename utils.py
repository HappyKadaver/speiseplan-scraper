from MenuItem import parseMenuItems
import urllib.request
import datetime

__MENSA_URL = "http://www.maxmanager.de/daten-extern/sw-giessen/html/speiseplan-render.php"


def _create_request_data(data:dict):
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')

    return data


def _read_html(url:str, data):
    request = urllib.request.Request(url, data)

    with urllib.request.urlopen(request) as response:
        return response.read()


def parse_mensa(date:str=str(datetime.date.today())):
    data = _create_request_data({'func': 'make_spl',
            'locId': 'mensa-thm-in-giessen',
            'lang': 'de',
            'date': date})
    return parseMenuItems(_read_html(__MENSA_URL, data))


def parse_campustor(date:str=str(datetime.date.today())):
    data = _create_request_data({'func': 'make_spl',
            'locId': 'campustor',
            'lang': 'de',
            'date': date})
    return parseMenuItems(_read_html(__MENSA_URL, data))


if __name__ == "__main__":
    print("campustor")

    for item in parse_campustor():
        print(vars(item))

    print("mensa")

    for item in parse_mensa(str(datetime.date(2015, 11, 18))):
        print(vars(item))
