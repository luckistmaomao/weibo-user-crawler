#coding:utf-8
"""
@author yuzt
created on 2014.8.8
"""

import storage
from storage import WeiboUser,WaitCrawlUser,MicroBlog
from task import crawl_one
import Queue
from multithreads import Threadpool
import time

user_list = ['2262603784','3732977714','5236447547']

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
    for i in user_list:
        pool.user_queue.put(i)
        time.sleep(600)

if __name__ == "__main__":
    main()
