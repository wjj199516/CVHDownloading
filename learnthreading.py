import time, multiprocessing, urllib2, threading
from threading import Thread
from threading import Lock
from threading import Condition
import random
from Queue import Queue

#balance = 0
#lock = threading.Lock()

def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()

#t1 = threading.Thread(target=run_thread, args=(5,))
#t2 = threading.Thread(target=run_thread, args=(8,))
#t1.start()
#t2.start()
#t1.join()
#t2.join()
#print balance

def loop():
    x = 0
    while True:
        x = x ^ 1

#print('cpu',multiprocessing.cpu_count())
#for i in range(multiprocessing.cpu_count()):
#    t = threading.Thread(target=loop)
#    t.start()

def print_time(thread_name,delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print('%s : %s' % (thread_name,time.ctime(time.time())))

#try:
#    thread.start_new_thread(print_time,('Thread-1',2,))
#    thread.start_new_thread(print_time,('Thread-2',4,))
#except:
#    print('Error: unable to start the thread')

#while True:
#    pass


class MyThread(threading.Thread):

    def __init__(self,target,args):
        super(MyThread,self).__init__()
        self.target = target
        self.args = args

    def run(self):
        self.target(self.args)

def print_time(counter):
    while counter:
        print("counter = %d" % counter)
        counter -= 1
        time.sleep(1)

def main():
    my_thread = MyThread(print_time,10)
    my_thread.start()
    my_thread.join()

#if __name__ == '__main__':
#    main()

class GetUrlThread(Thread):
    def __init__(self,url):
        self.url = url
        super(GetUrlThread,self).__init__()

    def run(self):
        resp = urllib2.urlopen(self.url)
        print (self.url,resp.getcode())

def get_responses():
    urls = [ 'http://www.ebay.com', 'http://www.alibaba.com']
    start = time.time()
    threads = []
    for url in urls:
        t = GetUrlThread(url)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print "Elapsed time: %s" % (time.time()-start)

some_var = 0

class IncrementThread(Thread):
    def run(self):
        #we want to read a global variable
        #and then increment it
        global some_var
        lock.acquire()
        read_value = some_var
        print "some_var in %s is %d" % (self.name, read_value)
        some_var = read_value + 1
        print "some_var in %s after increment is %d" % (self.name, some_var)
        lock.release()

def use_increment_thread():
    threads = []
    for i in range(50):
        t = IncrementThread()
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print "After 50 modifications, some_var should have become 50"
    print "After 50 modifications, some_var is %d" % (some_var,)

class CreateListThread(Thread):
    def run(self):
        self.entries = []
        for i in range(10):
            time.sleep(1)
            self.entries.append(i)
        lock.acquire()
        print self.entries
        lock.release()

def use_create_list_thread():
    for i in range(3):
        t = CreateListThread()
        t.start()

queue = Queue(10)


class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            num = queue.get()
            queue.task_done()
            print("Consumed", num)
            time.sleep(random.random())

class ProducerThread(Thread):
    def run(self):
        nums = range(5)
        global queue
        while True:
            num = random.choice(nums)
            queue.put(num)
            print ("Produced", num)
            time.sleep(random.random())

ProducerThread().start()
ConsumerThread().start()