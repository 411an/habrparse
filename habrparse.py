import requests
from bs4 import BeautifulSoup
import csv

def get_article(pid):
#    fname = r'files/' + str(pid) + '.csv'
    fname = r'files/' + 'habrbase' + '.csv'
    with open(fname, "a", newline="") as file:
        try:
            writer = csv.writer(file)
            r = requests.head('https://habr.com/ru/post/' +str(pid) + '/')
            if r.status_code == 404: # проверка на существование
                pass
            else:
                r = requests.get('https://habr.com/ru/post/' +str(pid) + '/')
                soup = BeautifulSoup(r.text, 'html5lib') # instead of html.parser
                if not soup.find("span", {"class": "post__title-text"}):
                    pass
                else:
                    doc = []
                    cmt = []
                    doc.append(pid) #номер
                    doc.append(soup.find("span", {"class": "user-info__nickname"}).text) #ник

                    if not soup.find("span", {"class": "voting-wjt__counter"}):
                        doc.append('0')
                    else:
                        doc.append(soup.find("span", {"class": "voting-wjt__counter"}).text) # счетчик

                    writer.writerow(doc)
                    comments = soup.find_all("div", {"class": "comment"})
                    for x in comments:
                        if not x.find("div", {"class": "comment__message_banned"}) and not x['id']=="comment_":
                            cmt.append(x['id'][8:]) #номер
                            cmt.append(x.find("span", {"class": "user-info__nickname"}).text) #ник
                            cmt.append(x.find("span", {"class": "voting-wjt__counter"}).text) #счётчик
                            writer.writerow(cmt)
                            cmt = []
        except requests.exceptions.ConnectionError:
            pass

x = int(input())
y = int(input())+1

for i in range(x, y):
    get_article(i)
    print(i)