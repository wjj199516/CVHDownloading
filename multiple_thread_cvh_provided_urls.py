from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from threading import Thread
import queue
import os
import pymysql
import requests
import time




class ProducerThread(Thread):
    def __init__(self):
        super(ProducerThread, self).__init__()

    def run(self):
        global queue
        infile = open("/Users/Simon/Desktop/cvh测试100.txt", "rU")
        gottenUrlFileRead = open("/Users/Simon/Desktop/cvh测试gottenUrl.txt", "rU")
        gottenUrl = gottenUrlFileRead.read()
        gottenUrlFileRead.close()
        while True:
            line = infile.readline()
            if line:
                if line not in gottenUrl:
                    cvh_url = line[:-1]
                    queue.put(cvh_url)
                    print('Produced',cvh_url)
            else:
                break
        infile.close()

class ConsumerThread(Thread):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36(KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q = 0.9, image / webp, * / *;q = 0.8"}
    downloadDirectory = "/Users/Simon/Documents/CVH"
    baseUrl = "http://img.cvh.ac.cn/imgcvh"

    def __init__(self):
        super(ConsumerThread, self).__init__()
        self.conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='root', passwd='wjj199516',db='mysql',charset='utf8')
        self.cur = self.conn.cursor()
        self.cur.execute("USE cvh")

    def getDownloadPath(self,image_url):
        path = image_url.replace(ConsumerThread.baseUrl, "")
        path = ConsumerThread.downloadDirectory + path
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return path

    def getItem(self,url):
        req = ConsumerThread.session.get(url, headers=ConsumerThread.headers)
        bsObj = BeautifulSoup(req.text, "lxml")
        herbarium = bsObj.find("div", {"class": "fl spdiv4"}).findAll("div", {"class": "spdiv3"})[0].find("div", {
            "class": "fl spdiv2"}).get_text().strip()
        print("herbarium", herbarium)
        id_tag = bsObj.find("div", {"class": "fl spdiv4"}).findAll("div", {"class": "spdiv3"})[1].find("div", {
            "class": "fl spdiv2"}).get_text().strip()
        print("id_tag", id_tag)
        science_name = bsObj.find("div", {"class": "petitle_content"}).find("span", {"id": "splatin"}).find(
            "a").get_text().strip()
        print("science_name", science_name)
        chinese_name = bsObj.find("div", {"class": "petitle_content"}).find("div", {"id": "spcname"}).get_text().strip()
        print("chinese_name", chinese_name)
        spauthor = bsObj.find("div", {"class": "petitle_content"}).find("div", {"id": "spauthor"}).get_text()[
                   4:].strip()
        print("spauthor", spauthor)
        spadate = bsObj.find("div", {"class": "petitle_content"}).find("div", {"id": "spadate"}).get_text().strip()
        print("spadate", spadate)
        collector_no = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[0].find("div", {
            "class": "fl spdiv6"}).get_text().strip()
        print("collector_no", collector_no)
        collect_dat = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[1].find("div", {
            "class": "fl spdiv6"}).get_text().strip()
        print("collect_dat", collect_dat)
        collect_loc = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[2].find("div", {
            "class": "fl spdiv6"}).get_text().strip()
        print("collect_loc", collect_loc)
        habitat = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[3].find("div", {
            "class": "fl spdiv6"}).get_text().strip()
        print("habitat", habitat)
        altitude = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[4].find("div", {
            "class": "fl spdiv6"}).get_text().strip()
        print("altitude", altitude)
        xingzhuang = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[5].find("div", {
            "class": "fl spdiv6"}).get_text().strip()
        print("xingzhuang", xingzhuang)
        wuhouqi = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[6].find("div", {
            "class": "fl spdiv6"}).get_text().strip()
        print("wuhouqi", wuhouqi)
        description = bsObj.find("div", {"id": "pe_qianc_2"}).findAll("div", {"class": "spdiv3"})[7].find("div", {
            "class": "fl spdiv6"}).get_text().strip()
        print("description", description)
        try:
            image_url = bsObj.find("div",{"id":"peinfo"}).findAll("div",{"class":"fl"})[0].findAll("div")[2].find("a")["href"]
            print("image_url", image_url)
        except TypeError as e:
            image_url = None
            print("Image was not found")
        if image_url:
            image_path = self.getDownloadPath(image_url)
            urlretrieve(image_url, image_path)
            print("image_path", image_path)
        else:
            image_path = None
            print("Image_path did not exist")
        self.cur.execute(
            "INSERT INTO specimen16 (herbarium, id_tag,science_name,chinese_name,spauthor,spadate,collector_no,collect_dat,collect_loc,habitat,altitude,xingzhuang,wuhouqi,description,image_url,image_path,cvh_url) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")",
            (herbarium, id_tag, science_name, chinese_name, spauthor, spadate, collector_no, collect_dat, collect_loc,
             habitat, altitude, xingzhuang, wuhouqi, description, image_url, image_path, url))
        self.cur.connection.commit()

    def run(self):
        global queue
        while True:
            if  Producer.is_alive() or not queue.empty():
                url = queue.get()
                self.getItem(url)
                print('Consumed', url)
                gottenUrlFile = open("/Users/Simon/Desktop/cvh测试gottenUrl.txt", "a")
                gottenUrlFile.write(url + '\n')
                gottenUrlFile.close()
                queue.task_done()
            else:
                self.cur.close()
                self.conn.close()
                break

start = time.time()
queue = queue.Queue(10)
Producer = ProducerThread()
Producer.start()
threads = []
for i in range(10):
    t = ConsumerThread()
    threads.append(t)
    t.start()
Producer.join()
queue.join()
for i in threads:
    i.join()
stop = time.time()
print(stop-start)

#明天除了解决已下载的重复下载的问题,还要记得将程序与数据库的连接关闭
#finally:
#t.conn.close()
#t.cur.close()

