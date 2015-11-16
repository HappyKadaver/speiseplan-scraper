from MenuItem import MenuItem
from MenuItem import parseMenuItems


class Menu:
    """

    """

    def __init__(self, cafeteria, menuItems):
        self.menuItems = menuItems
        self.cafeteria = cafeteria


def parseMenu(html, cafeteria=None):
    """

    :param html: raw html from "http://www.maxmanager.de/daten-extern/sw-giessen/html/speiseplaene.php"
    :return: Menu for that cafeteria
    """

    return Menu(cafeteria, parseMenuItems(html))


m = MenuItem("Schnitzel", 3.10)

print(vars(m))
