import os
import uuid
import time
import Queue
import urllib2
from threading import Lock
from threading import Timer
from threading import Thread
from importlib import import_module
from geobricks_downloader.utils import log


# thread_manager_processes = {}
multi_progress_map = {}
# threads_map_key = 'FENIX'
# log = log.logger('download_threads_manager.py')
out_template = {
    'download_size': 0,
    'layer_name': 'unknown',
    'progress': 0,
    'total_size': 'unknown',
    'status': 'unknown',
    'thread': 'unknown',
    'key': None
}
exit_flags = {}


class DownloadsThreadManager(Thread):

    def __init__(self, uid, target_dir, file_paths_and_sizes):

        Thread.__init__(self)

        self.file_paths_and_sizes = file_paths_and_sizes
        self.target_dir = target_dir
        self.uid = uid
        self.log = log.logger(self.__class__.__name__)

    def run(self):
        t = Timer(1, self.start_manager)
        t.start()
        return self.target_dir

    def start_manager(self):

        exit_flags[self.uid] = 0

        self.log.info('Downloads Thread Manager started.')

        thread_list = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet']
        queue_lock = Lock()
        work_queue = Queue.Queue(len(self.file_paths_and_sizes))
        threads = []

        for thread_name in thread_list:
            thread = DownloadThread(self.uid, thread_name, work_queue, queue_lock, self.target_dir)
            thread.start()
            threads.append(thread)

        queue_lock.acquire()
        for word in self.file_paths_and_sizes:
            work_queue.put(word)
        queue_lock.release()

        while not work_queue.empty():
            pass

        exit_flags[self.uid] = 1

        for t in threads:
            t.join()

        self.log.info('Downloads Thread Manager done.')


class DownloadThread(Thread):

    file_obj = None
    file_name = None
    file_path = None
    total_size = 0
    download_size = 0

    def __init__(self, uid, thread_name, queue, queue_lock, target_dir, block_sz=16384):

        Thread.__init__(self)

        self.thread_name = thread_name
        self.queue = queue
        self.queue_lock = queue_lock
        self.block_sz = block_sz
        self.target_dir = target_dir
        self.uid = uid
        self.log = log.logger(self.__class__.__name__)

    def run(self):

        while not exit_flags[self.uid]:

            self.queue_lock.acquire()

            if not self.queue.empty():

                self.file_obj = self.queue.get()
                self.file_name = self.file_obj['file_name']
                self.file_path = self.file_obj['file_path']
                self.download_size = 0

                if self.uid not in multi_progress_map:
                    multi_progress_map[self.uid] = {}
                multi_progress_map[self.uid][self.file_name] = {}

                self.queue_lock.release()

                local_file = os.path.join(self.target_dir, self.file_name)

                u = urllib2.urlopen(self.file_path)
                meta = u.info()
                self.total_size = int(meta.getheaders('Content-Length')[0])

                # Download the file only if its size is different from the one on the FTP
                allow_layer_download = True
                try:
                    allow_layer_download = int(os.stat(local_file).st_size) < int(self.total_size)
                except OSError:
                    pass

                if allow_layer_download:

                    u = urllib2.urlopen(self.file_path)
                    f = open(local_file, 'wb')

                    multi_progress_map[self.uid][self.file_name]['total_size'] = self.total_size
                    multi_progress_map[self.uid][self.file_name]['download_size'] = 0

                    if not os.path.isfile(local_file) or os.stat(local_file).st_size < self.total_size:
                        self.log.info(self.file_name + ' download start.')
                        file_size_dl = 0
                        while self.download_size < self.total_size:
                            chunk = u.read(self.block_sz)
                            if not buffer:
                                break
                            file_size_dl += len(chunk)
                            f.write(chunk)
                            self.download_size += len(chunk)
                            self.update_progress_map()
                            self.log.info(self.thread_name + ' is downloading ' + self.file_name)
                            self.log.info('Download progress: ' + str(multi_progress_map[self.uid][self.file_name]['progress']) + '%')
                            if float(self.download_size) == float(self.total_size):
                                break

                    multi_progress_map[self.uid][self.file_name]['status'] = 'COMPLETE'
                    self.log.info(self.file_name + ' download complete.')
                    f.close()

                else:
                    multi_progress_map[self.uid][self.file_name]['download_size'] = self.total_size
                    multi_progress_map[self.uid][self.file_name]['progress'] = 100

            else:
                self.queue_lock.release()

            time.sleep(1)

    def percent_done(self):
        return float('{0:.2f}'.format(float(self.download_size) / float(self.total_size) * 100))

    def update_progress_map(self):
        multi_progress_map[self.uid][self.file_name]['download_size'] = self.download_size
        multi_progress_map[self.uid][self.file_name]['progress'] = self.percent_done()
        multi_progress_map[self.uid][self.file_name]['status'] = 'DOWNLOADING'
        multi_progress_map[self.uid][self.file_name]['key'] = self.uid