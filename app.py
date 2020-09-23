from multiprocessing import Process, Queue, Value
from multiprocessing import Manager
import multiprocessing as mp
import time
import random
from progressbar import ProgressBar

class FetchProcess(Process):
    def __init__(self, page_queue, record_queue, page_count):
        super(FetchProcess, self).__init__()
        self.page_queue = page_queue
        self.record_queue = record_queue
        self.page_count = page_count

    def run(self):
        while True:
            time.sleep(.2)
            page = self.page_queue.get()
            start = (50 * page) + 1
            end = start + 50

            for i in range(start, end):
                self.record_queue.put(i)


class FetchDbProcess(Process):
    def __init__(self, record_queue, proc_queue, record_count):
        super(FetchDbProcess, self).__init__()
        self.record_queue = record_queue
        self.proc_queue = proc_queue
        self.record_count = record_count

    def run(self):
        while True:
            time.sleep(.2)
            record = self.record_queue.get()
            self.proc_queue.put(record)


class ProcessingProcess(Process):
    def __init__(self, proc_queue, idx, record_count):
        super(ProcessingProcess, self).__init__()
        self.proc_queue = proc_queue
        self.idx = idx
        self.record_count = record_count

    def run(self):
        while True:
            time.sleep(.5)
            record = self.proc_queue.get()
            self.idx.value += 1


class ProgressBarProcess(Process):
    def __init__(self, idx, record_count):
        super(ProgressBarProcess, self).__init__()
        self.idx = idx
        self.record_count = record_count
        self.pbar = ProgressBar(max_value=record_count)

    def run(self):
        while self.idx.value < self.record_count:
            self.pbar.update(self.idx.value)

        self.pbar.update(self.record_count)


def main():
    mp.set_start_method('fork')

    NUMBER_OF_FETCH_PROCESSES = 10
    NUMBER_OF_DB_PROCESSES = 10
    NUMBER_OF_PROC_PROCESSES = 10

    fetch_processes = list()
    db_processes = list()
    proc_processes = list()

    # Get the number of pages we're going to be processing
    page_num = random.randint(4, 5)
    record_count = page_num * 50
    time.sleep(.5) # Wait for 500 milliseconds to simulate the fetch

    page_queue = Queue(page_num)
    record_queue = Queue(record_count)
    proc_queue = Queue(record_count)

    idx = Value('i', 0)
    pbar_proc = ProgressBarProcess(idx, record_count)
    pbar_proc.start()

    for i in range(0, page_num):
        page_queue.put(i)

    for i in range(0, NUMBER_OF_FETCH_PROCESSES):
        proc = FetchProcess(page_queue, record_queue, page_num)
        proc.start()
        fetch_processes.append(proc)

    for i in range(0, NUMBER_OF_DB_PROCESSES):
        proc = FetchDbProcess(record_queue, proc_queue, record_count)
        proc.start()
        db_processes.append(proc)

    for i in range(0, NUMBER_OF_PROC_PROCESSES):
        proc = ProcessingProcess(proc_queue, idx, record_count)
        proc.start()
        proc_processes.append(proc)

    [proc.join() for proc in fetch_processes]
    [proc.join() for proc in db_processes]
    [proc.join() for proc in proc_processes]

    [proc.kill() for proc in fetch_processes]
    [proc.kill() for proc in db_processes]
    [proc.kill() for proc in proc_processes]

    print("All done")

if __name__ == '__main__':
    main()
