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

class WaitCrawlUserListManager(threading.Thread):
    def __init__(self,wait_user_queue):
        self.weibo_user_set = self.get_weibo_user_set()
        self.wait_user_queue = wait_user_queue

    def run(self):
        while True:
            for wait_crawl_user in WaitCrawlUser.objects:
                user = {}
                uid = wait_crawl_user.uid
                if uid in self.user_set:
                    continue
                self.user_set.add(uid)
                self.wait_user_queue.put(uid)
            time.sleep(60)

    def get_weibo_user_set(self):
        user_set = set()
        for weibo_user in WeiboUser.objects:
            user_set.add(weibo_user.uid)

            
def crawl_wait_users():
    wait_crawl_list = []
    for wait_crawl_user in WaitCrawlUser.objects:
        user = {}
        uid = wait_crawl_user.uid
        user['uid'] = uid
        user['is_crawling'] = False
        wait_crawl_list.append(user)


def main():
    pool = Threadpool(5,crawl_one)
    
    wait_crawl_user_list_manager = WaitCrawlUserListManager(pool.user_queue)
    wait_crawl_user_list_manager.start()

if __name__ == "__main__":
    main()
