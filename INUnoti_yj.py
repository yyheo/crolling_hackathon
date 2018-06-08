from bs4 import BeautifulSoup
import requests

boundary = ('학사', '장학금', '모집채용', '일반')
base = "http://www.inu.ac.kr/user/"
def _parser() :
    url = "http://www.inu.ac.kr/user/boardList.do?boardId=48510&page=1&siteId=inu&id=inu_070201000000&column=&search="
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    return soup

def INUimFor() :
    imfor = [[],[],[],[]]
    soup = _parser()
    hidden = soup.find("div", {"id" : "contents"})
    lists = hidden.find_all("tr")
    for item in lists :
        category = item.find("span", {"class" : "tb_stress"})
        if category != None :
            cate = category.text[1:-1]
            find = item.find("td", {"class" : "textAL"}).find("a")
            title = find.text[10:].strip()
            link = base + item.find("a")['href']
            comp = link +'@' + title
            for i in range(4) :
                if cate == boundary[i] :
                    imfor[i].append(comp)
    result = dict()
    for i in range(4) :
        result[boundary[i]] = imfor[i]
    return result


def mostView() :
    most = 0
    comp = ''
    soup = _parser()
    hidden = soup.find("div", {"id": "contents"})
    lists = hidden.find_all("tr")
    for item in lists :
        category = item.find("span", {"class" : "tb_stress"})
        if category != None :
            num = int(item.find_all("td")[4].text.strip())
            if most < num :
                find = item.find("td", {"class": "textAL"}).find("a")
                title = find.text[10:].strip()
                most = num
                mostlink = base + item.find("a")['href']
    return mostlink, title

mostView = mostView()
mostView_title = mostView[1]
mostView_link = mostView[0]