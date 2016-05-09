from bs4 import BeautifulSoup
import requests
import json

finalList = []
urlList = []
finish = 0
baseURL = "http://www.lonelyplanet.com"
subURL = "/india/sights?page=1"
urlFile = open("urls","w")
dataFile = open("data1.json", "w")
errorFile = open("errror", "w")

while finish == 0:

    url = baseURL + subURL
    print url
    r  = requests.get(url)

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    for link in soup.find_all("a", class_=''):
        if link.get('href') != "http://www.lonelyplanet.com/asia":
            urlFile.write("%s\n" %(link.get('href')))                           #writes sub url in a file
            urlList.append(link.get('href'))

    if soup.find("a", class_='js-next-page') == None:
        finish = 1
        print 'Bye'
    else:
        subURL = soup.find("a", class_='js-next-page').get('href')

#print urlList
print len(urlList)
urlFile.close()

for poiURL in urlList:
    title_arr = []
    content_arr = []
    obj = {}
    url1 = baseURL + poiURL
    # url1 = "http://www.lonelyplanet.com/india/sights/religious/kapaleeshwarar-temple/item-a-460359-id"
    print url1
    r1  = requests.get(url1)

    data1 = r1.text

    soup1 = BeautifulSoup(data1, "html.parser")

    for link in soup1.find_all("dt"):                                           # this get all the side headings
        title_arr.append(link.get_text())

    for link in soup1.find_all("dd"):                                           # this get all the side headings' values
        content_arr.append(link.get_text())

    print len(title_arr)
    print len(content_arr)
    print (title_arr)
    print (content_arr)
    if len(content_arr)<= len(title_arr):
        for i in range(0, len(content_arr)):
            if title_arr[i].replace('\n','') != "Something wrong?Submit a correction":
                obj[title_arr[i].replace('\n','')] = content_arr[i].replace('\n','')
    else:
        for i in range(0, len(content_arr)):
            if i<len(title_arr):
                obj[title_arr[i].replace('\n','')] = content_arr[i].replace('\n','')
            else:
                obj['extra'] = content_arr[i].replace('\n','')
        errorFile.write(url1)
        errorFile.write('\n')
        print 'error in URL'

    obj['title'] = soup1.find("title").get_text().replace('\n','').replace(' - Lonely Planet','')

    if soup1.find("div", class_="poi-map__container mv--inline js-poi-map-container")!= None :
        obj['latitude'] = soup1.find("div", class_="poi-map__container mv--inline js-poi-map-container").get('data-latitude')
        obj['longitude'] = soup1.find("div", class_="poi-map__container mv--inline js-poi-map-container").get('data-longitude')

    if soup1.find("div", class_="ttd__section ttd__section--description")!= None :
        obj['description'] = soup1.find("div", class_="ttd__section ttd__section--description").get_text().replace('\n','')

    obj['tag'] = soup1.find("a", class_='card--page__breadcrumb__link').get_text()

    json.dump(obj, dataFile)                                                    # write each object in file
    dataFile.write("\n")

dataFile.close()
