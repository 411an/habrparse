import requests
from bs4 import BeautifulSoup
import csv
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
import pandas
import datetime

def len_checker():
    fname = r'files/' + 'habrdata' + '.csv'
    with open(fname, "r") as file:
        try:
            authorsList = len(file.readlines()) #получаем длину файла даты
        except:
            authorsList = 0
        return authorsList

def date_change(d):
    monthList = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']

    if d.find('позавчера') != -1:
        datetimeDate = datetime.date(2019,8,24)
        return datetimeDate
    if d.find('вчера') != -1:
        datetimeDate = datetime.date(2019,8,25)
        return datetimeDate

    tempDate = d
    tempDate = tempDate.replace('Зарегистрирована','')
    tempDate = tempDate.replace('Зарегистрирован','')
    tempDate = tempDate.strip()
    tempDate = tempDate.replace('  ',' ')
    tempDateList = tempDate.split(' ')
    idx = monthList.index(tempDateList[1])
    tempDateList[0] = int(tempDateList[0])
    tempDateList[1] = idx+1
    if len(tempDateList) == 2:
        tempDateList.append(2019)
    else:
        tempDateList[2] = int(tempDateList[2])
    datetimeDate = datetime.date(tempDateList[2],tempDateList[1],tempDateList[0])
    return datetimeDate


def profile_check(nname):
    try:
        r = requests.head('https://m.habr.com/ru/users/' +nname + '/')
        if r.status_code == 404: # проверка на существование
            ValUsers = [0,0,0,datetime.date(2001,1,1)]
            #pass
        else:
            ValUsers = []
            r = requests.get('https://m.habr.com/ru/users/' +nname + '/')
            soup = BeautifulSoup(r.text, 'html5lib') # instead of html.parser
            if not soup.find("div", {"class": "tm-user-card"}):
                valKarma = 0
                valComments = 0
                valArticles = 0
                valDate = datetime.date(2001,1,1)
            else:
                valKarma = soup.find("span", {"class": "tm-votes-score"}).text #карма
                valKarma = valKarma.replace(',','.').strip()
                valKarma = float(valKarma)

                tempDate = soup.find_all("div", {"class": "tm-profile__subtitle"}) #.text.replace('\n', '')
                for t in tempDate:
                    if t.text.strip() == 'Зарегистрирован' or t.text.strip() == 'Зарегистрирована':
                       a = t.previous.text
                valDate = date_change(a) #Дата регистрации

                tempDataBlock = soup.find("div", {"class": "tm-tabs-list__scroll-area"}).text.replace('\n', '') #показатели активности
                mainDataBlock = tempDataBlock.split(' ')
                valArticles = mainDataBlock[mainDataBlock.index('Публикации')+1]
                if valArticles.isdigit() == True:
                    valArticles = int(valArticles)
                else:
                    valArticles = 0
                valComments = mainDataBlock[mainDataBlock.index('Комментарии')+1]
                if valComments.isdigit() == True:
                    valComments = int(valComments)
                else:    
                    valComments = 0
            ValUsers.append(valKarma)
            ValUsers.append(valComments)
            ValUsers.append(valArticles)
            ValUsers.append(valDate)
    except requests.exceptions.ConnectionError:
        ValUsers = [0,0,0,datetime.date(2001,1,1)]
    return ValUsers


def get_author_by_nick(x):
    finalRow = []
    df = pandas.DataFrame
    colnames=['nick', 'scores']
    df = pandas.read_csv(r'files\habrauthors.csv', encoding="ANSI", names = colnames, header = None)
    df1 = df.loc[x:]

    fname = r'files/' + 'habrdata' + '.csv'
    
    with open(fname, "a", newline="") as file:
        try:
            x = 1
            writer = csv.writer(file)
            for row in df1.itertuples(index=True, name='Pandas'):
                valName = getattr(row, "nick")
                valScore = getattr(row, "scores")
                valAll = profile_check(valName)
                finalRow.append(valName)
                finalRow.append(valScore)
                finalRow.append(valAll[0])
                finalRow.append(valAll[1])
                finalRow.append(valAll[2])
                finalRow.append(valAll[3])
                writer.writerow(finalRow)
                print(valName)
                finalRow = []
                if x == 50:
                    file.flush()
                    x = 1
                else:
                    x += 1
            file.close()
        except Exception as e:
            file.close()
            print(e)

n = len_checker()
get_author_by_nick(n)