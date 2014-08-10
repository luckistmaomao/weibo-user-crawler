"""
@author yuzt
created at 2014.8.10
"""

import time
from Queue import Queue
from time import ctime,sleep
import threading
from task import crawl_one

class Threadpool(threading.Thread):
    def __init__(self,max_workers,func,user_list = []):
        self.max_workers = max_workers
        self.user_queue = Queue()
        for user in user_list:
            self.user_queue.put(user)
        self.workers = []
        self.func = func
        self.createWorkers(max_workers)

    def createWorkers(self,num_workers):
        for i in range(num_workers):
            self.workers.append(WorkerThread(self.func,self.user_queue))
        for thread in self.workers:
            thread.start()
            

class WorkerThread(threading.Thread):
    '''
    A sub class of Thread
    '''
    def __init__(self, func,user_queue, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self._user_queue = user_queue

    def run(self):
        while True:
            try:
                uid = self._user_queue.get()
            except:
                pass
                continue

            args = [uid,]
            print '-starting', self.name, 'at:', ctime()
            apply(self.func,args )
            print self.name, 'finished at:', ctime()

def do_something(num):
    sleep(1)
    print num

def test():
    pool = Threadpool(5,do_something,range(10))

if __name__ == "__main__":
    pool = Threadpool(5,do_something,range(2))

    for i in range(10):
        sleep(3)
        pool.user_queue.put(i)
