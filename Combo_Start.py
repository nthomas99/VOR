#Start Eye Tracker & Head Tracker with multiprocessing

import multiprocessing
import time

def worker_e():
	import GUItest_tk

def worker_h():
	import berryIMU_TK_tofile


if __name__=='__main__':
	eye_work = multiprocessing.Process(target=worker_e)
	head_work = multiprocessing.Process(target=worker_h)

	eye_work.start()
	head_work.start()

time.sleep(5)
