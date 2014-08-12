#coding:utf-8
"""
@author yuzt
created on 2014.8.8
"""

import storage
from storage import WeiboUser,WaitCrawlUser,MicroBlog
from task import crawl_one,add_crawl
import Queue
from multithreads import Threadpool
import time
import threading
import random

class WaitCrawlUserListManager(threading.Thread):
    def __init__(self,wait_user_queue):
        threading.Thread.__init__(self)
        self.weibo_user_set = self.get_weibo_user_set()
        self.wait_user_queue = wait_user_queue

    def run(self):
        while True:
            for wait_crawl_user in WaitCrawlUser.objects:
                uid = wait_crawl_user.uid
                if uid in self.weibo_user_set:
                    continue
                self.weibo_user_set.add(uid)
                self.wait_user_queue.put(uid)
            time.sleep(60)

    def get_weibo_user_set(self):
        user_set = set()
        for weibo_user in WeiboUser.objects:
            user_set.add(weibo_user.uid)
        return user_set


class WeiboUserListManager(threading.Thread):
    def __init__(self,weibo_user_queue):
        threading.Thread.__init__(self)
        self.weibo_user_queue = weibo_user_queue

    def run(self):
        while True:
            for weibo_user in WeiboUser.objects:
                uid = weibo_user.uid
                self.weibo_user_queue.put(uid)
                sleep_time = random.randint(20,30) 
                time.sleep(sleep_time)


def main():
    wait_pool = Threadpool(5,crawl_one)
    add_pool = Threadpool(3,add_crawl) 
    wait_crawl_user_list_manager = WaitCrawlUserListManager(wait_pool.user_queue)
    wait_crawl_user_list_manager.start()
    
    weibo_user_list_manager = WeiboUserListManager(add_pool.user_queue)
    weibo_user_list_manager.start()

if __name__ == "__main__":
    main()
