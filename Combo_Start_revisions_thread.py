#Start Eye Tracker & Head Tracker with multiprocessing

from threading import thread

def worker_e():
	import GUItest_tk_revisions

def worker_h():
	import berryIMU_TK_tofile_revisions


if __name__=='__main__':
	eye_work = threading.Thread(target=worker_e)
	head_work = threading.Thread(target=worker_h)

	eye_work.start()
	head_work.start()


