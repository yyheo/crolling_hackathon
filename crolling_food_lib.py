import requests
from bs4 import BeautifulSoup
import time

def foodData() :
    result = ''
    uri = "http://www.uicoop.ac.kr/shop/shop.php?w=3"
    now = time.localtime()

    response = requests.get(uri)
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    root = soup.find("div", {"class" : "smid"}).find("div", {"class" : "detail_left"})
    hidden = root.find("table")
    day = hidden.find("td", {"class" : "menu-mn2t"})
    every_food = hidden.find_all("tr")
    for item in every_food :
        try :
            title = item.find("div", {"style" :"float:left;padding:2px 0 8px 10px;"})
            result += '\n['+title.text+ ']\n'
        except :
            pass
        try :
            corner = item.find_all("td", {"class" : "menu-list-corn"})
            result += '(' + corner[len(corner)-1].text + ')\n'
        except :
            pass
        try :
            food = item.find_all("td", {"class" : "menu-list"})[now.tm_wday]
            mainMenu = food.find("span", {"style" : "font-weight:bold;color:#0B555B;"})
            result += mainMenu.text + '\n'
        except :
            pass
    return result

tmp = foodData()
print(tmp)

def LibData():
    result = ''
    lib = []
    for i in range(1,5):
        uri = "http://117.16.225.193:8080/seatmate/SeatMate.php?classInfo="+str(i)
        response = requests.get(uri)
        soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
        root = soup.find("div", {"id": "location_box1"}).find("li", {"class" : "txt4"}).text
        lib.append(root)

    return "1열람실 : " + lib[0] + "석\n2열람실 : " + lib[1] + "석\n3열람실 : " + lib[2] + "석\n노트북실 : " + lib[3] + "석"


libseat = LibData()