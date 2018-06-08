import requests
from bs4 import BeautifulSoup
from textRank import *

base = "http://www.inu.ac.kr/user/"
def newsInTheWorld() :
    from selenium import webdriver
    news = []
    driver = webdriver.Firefox()
    url = "http://www.inu.ac.kr/mbshome/mbs/inu/subview.do?id=inu_070102000000"
    driver.get(url)
    html = driver.page_source
    urlsoup = BeautifulSoup(html)
    boundary = urlsoup.find_all("tr")
    # print(boundary)
    # for list in lists :
    #     link = base + list.find("a")['href']
    #     response = link.get(link)
    #     linkedsoup = BeautifulSoup(response.content.decode('utf-8', 'replace'), "")
    #     hidden = linkedsoup.find("section", {"id" : "user-container"})
    #     tmp = hidden.find("div", {"class" : "article-view-banners"}).text.strip()
    #     print(tmp)

def newsContents() :
    title = []
    link_list = []
    news = []
    url= requests.get('http://www.inu.ac.kr/user/boardList.do?boardId=48494&siteId=inu&id=inu_070101000000')

    soup = BeautifulSoup(url.content.decode('utf-8', 'replace'), "lxml")
    boundary = soup.find("div", {"class" : "tbList"}).find("tbody")
    lists = boundary.find_all("tr")
    for list in lists :
        t = list.find("td", {"class" : "textAL"}).text.strip().replace("\n","").replace("\t","")
        title.append(t)
        link = base + list.find("a")['href']
        response = requests.get(link)
        linkedsoup = BeautifulSoup(response.content.decode('utf-8', 'replace'), "html.parser")
        find = linkedsoup.find("div", {"class" : "bdViewCont cf"}).text.strip().replace("\n", "").replace("\t","")
        news.append(find)
        link_list.append(link)

    return news, link_list, title

def saveNews(list) :
    global count
    count = 0
    try :
        for i in range(len(list)) :
            with open('C:\\Users\\Honeyoon\\PycharmProjects\\crollinghackathon\\textfile\\text{0}.txt'.format(count), 'w', encoding='utf-8') as f :
                f.write(list[i])
            count+=1
        return True
    except(IOError) :
        return False


news, links, title = newsContents()
inunews = []
if saveNews(news) :
    print("Data saves successfully")
else :
    print("Data cannot save")
for i in range(0, 7):
    tr = TextRank()
    # print('Load...')
    from konlpy.tag import Komoran

    tagger = Komoran()
    stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('【서울=뉴시스】', 'VV'), ('이에 따라', 'VV'), ('그러나', 'VV')])
    tr.loadSents(RawSentenceReader("C:\\Users\\Honeyoon\\PycharmProjects\\crollinghackathon\\textfile\\text{0}.txt".format(i)),
                 lambda sent: filter(lambda x: x not in stopword and x[1] in ('NNG', 'NNP', 'VV', 'VA'),
                                     tagger.pos(sent)))
    # print('Build...')
    tr.build()
    ranks = tr.rank()
    # for k in sorted(ranks, key=ranks.get, reverse=True)[:100]:
    #      print("\t".join([str(k), str(ranks[k]), str(tr.dictCount[k])]))
    result = tr.summarize(0.2)
    trans = links[i] + '@' + title[i] + '\n' + result.strip()+''
    inunews.append(trans)
