#coding:utf8
import threading
import time
import random

def workers():
	print 'start %s' %threading.current_thread()
	time.sleep(random.random())
	print 'end %s' %threading.current_thread()

def go_works():
	for i in range(10):
		threading.Thread(target=workers,).start()

def workers_lock(lock):
	lock.acquire()
	workers()
	lock.release()

def go_works_lock():
	lock = threading.Lock()
	for i in range(10):
		threading.Thread(target=workers_lock,args=[lock]).start()

if __name__ == '__main__':
	#go_works() #普通线程执行
	go_works_lock() #加锁线程执行
