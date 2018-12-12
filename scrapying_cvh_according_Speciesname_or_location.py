from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import os
import pymysql
import requests
import time
import re

def getSinglePage(n,name):
    #下载地名
    #url = "http://www.cvh.ac.cn/search/" + name + "?page=" +str(n) + "&searchtype=1&n=4"
    #下载属和种
    url = "http://www.cvh.ac.cn/search/" + name + "?page=" + str(n) + "&searchtype=1&n=1"
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36(KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q = 0.9, image / webp, * / *;q = 0.8"}
    req = session.get(url, headers=headers)
    bsObj = BeautifulSoup(req.text, "html.parser")
    nextUrls = bsObj.findAll("a",{"href":re.compile("^(/spm/).*")})
    nextlinks = [Url['href'] for Url in nextUrls]
    nextlinksSet = set(nextlinks)
    print(nextlinksSet)
    print(len(nextlinksSet))
    return nextlinksSet

#def getDownloadPath(baseUrl, image_url, downloadDirectory):
def getDownloadPath(image_url):
    #global baseUrl
    #global downloadDirectory
    path = image_url.replace(baseUrl, "")
    path = downloadDirectory+path
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return path

def getSingleUrl(url,file):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36(KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q = 0.9, image / webp, * / *;q = 0.8"}
    CVHurl = "http://www.cvh.ac.cn" + url
    print(CVHurl)
    req = session.get(CVHurl, headers=headers)
    bsObj = BeautifulSoup(req.text, "lxml")
    try:
        herbarium = bsObj.find("div", {"class": "fl spdiv4"}).findAll("div", {"class": "spdiv3"})[0].find("div", {
        "class": "fl spdiv2"}).get_text().strip()
    except AttributeError:
        print('No herbarium')
#    print('herbarium'.herbarium)
    try:
        id_tag = bsObj.find("div", {"class": "fl spdiv4"}).findAll("div", {"class": "spdiv3"})[1].find("div", {
        "class": "fl spdiv2"}).get_text().strip()
    except AttributeError:
        print('No id_tag')
#    print("id_tag", id_tag)
    try:
        science_name = bsObj.find("div", {"class": "petitle_content"}).find("span", {"id": "splatin"}).find(
        "a").get_text().strip()
    except AttributeError:
        print('No science_name')
        science_name = 'None'
#    print("science_name", science_name)
    try:
        chinese_name = bsObj.find("div", {"class": "petitle_content"}).find("div", {"id": "spcname"}).get_text().strip()
    except AttributeError:
        print('No chinese_name')
        chinese_name = 'None'
#    print("chinese_name", chinese_name)
    try:
        spauthor = bsObj.find("div", {"class": "petitle_content"}).find("div", {"id": "spauthor"}).get_text()[4:].strip()
    except AttributeError:
        print('No spauthor')
        spauthor = 'None'
#    print("spauthor", spauthor)
    try:
        spadate = bsObj.find("div", {"class": "petitle_content"}).find("div", {"id": "spadate"}).get_text().strip()
    except AttributeError:
        print('No spadate')
        spadate = 'None'
#    print("spadate", spadate)
    try:
        collector_no = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[0].find("div", {
        "class": "fl spdiv6"}).get_text().strip()
    except AttributeError:
        print('No collector_no')
#    print("collector_no", collector_no)
    try:
        collect_dat = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[1].find("div", {
        "class": "fl spdiv6"}).get_text().strip()
    except AttributeError:
        print('No collect_dat')
#    print("collect_dat", collect_dat)
    try:
        collect_loc = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[2].find("div", {
        "class": "fl spdiv6"}).get_text().strip()
    except AttributeError:
        print('No collect_loc')
#    print("collect_loc", collect_loc)
    try:
        habitat = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[3].find("div", {
        "class": "fl spdiv6"}).get_text().strip()
    except AttributeError:
        print('No habitat')
#    print("habitat", habitat)
    try:
        altitude = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[4].find("div", {
        "class": "fl spdiv6"}).get_text().strip()
    except AttributeError:
        print('No altitude')
#    print("altitude", altitude)
    try:
        xingzhuang = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[5].find("div", {
        "class": "fl spdiv6"}).get_text().strip()
    except AttributeError:
        print('No xingzhuang')
#    print("xingzhuang", xingzhuang)
    try:
        wuhouqi = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[6].find("div", {
        "class": "fl spdiv6"}).get_text().strip()
    except AttributeError:
        print('No wuhouqi')
#    print("wuhouqi", wuhouqi)
    try:
        description = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[7].find("div", {
        "class": "fl spdiv6"}).get_text().strip()
    except AttributeError:
        print('No description')
#    print("description", description)
    try:
        image_url = bsObj.find("div", {"id": "peinfo"}).findAll("div", {"class": "fl"})[0].findAll("div")[1].find("a")[
            "href"]
#        print("image_url", image_url)
        #image_path = getDownloadPath(baseUrl, image_url, downloadDirectory)
        image_path = getDownloadPath(image_url)
        try:
            urlretrieve(image_url, image_path)
        except HTTPError:
            image_url = 'None'
            image_path = 'None'
    except TypeError as e:
        image_url = 'None'
        image_path = 'None'
#        print("Image_path did not exist")
    file.write(herbarium + '\t' + id_tag + '\t' + science_name + '\t' + chinese_name + '\t' + spauthor + '\t' +spadate + '\t' +collector_no +'\t' + collect_dat + '\t' + collect_loc + '\t' + habitat +'\t' +altitude + '\t' +xingzhuang +'\t' + wuhouqi +'\t' + description +'\t'+image_path +'\t' +CVHurl + '\n')
#修改文件名
speciesfile = open("/Users/Simon/Desktop/高黎贡山/县名.txt","rU")
#修改下载目标文件名
downloadDirectory = "/Users/Simon/Desktop/高黎贡山"
baseUrl = "http://img.cvh.ac.cn/imgcvh/l"


while True:
    line = speciesfile.readline()
    if line:
        name = line.strip()
        print(name)
#修改文件名
        file = open("/Users/Simon/Desktop/高黎贡山/" + name ,"a")
        #下载种
        #speciesname = name.split(" ")[0] + "%20" + name.split(" ")[1]
        #下载地名
        speciesname = name
        #下载属
        #speciesname = name
        #print(speciesname)
        print(speciesname)
        #下载种
        #url = "http://www.cvh.ac.cn/search/" + speciesname + "?page=1&searchtype=1&n=1"
        #下载地名
        #url = "http://www.cvh.ac.cn/search/" + speciesname + "?page=1&searchtype=1&n=4"
        #下载属
        url = "http://www.cvh.ac.cn/search/" + speciesname + "?page=1&searchtype=1&n=1"
        print(url)
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36(KHTML, like Gecko) Chrome",
            "Accept": "text/html,application/xhtml+xml,application/xml;q = 0.9, image / webp, * / *;q = 0.8"}
        req = session.get(url, headers=headers)
        bsObj = BeautifulSoup(req.text, "html.parser")
        try:
            pagenumber = int(bsObj.find("div",{"id":"divpage"}).findAll("a")[-2].get_text())
            print(pagenumber)
        except IndexError:
            pagenumber = 1
        for n in range(1,pagenumber+1):
            print(n)
            urls = getSinglePage(n,speciesname)
            for url in urls:
                #file.write('http://www.cvh.ac.cn' + url + '\n')
                getSingleUrl(url, file)
        file.close()
    else:
        break


