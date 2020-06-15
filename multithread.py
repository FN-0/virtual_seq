import threading
import time

exitFlag = 0

class myThread (threading.Thread):
  def __init__(self, threadID, name, counter, lst=[]):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.counter = counter
    self.lst = lst
  def run(self):
    print("Starting " + self.name)
    self.lst = print_time(self.name, 2, self.counter)
    print("Exiting " + self.name)

def print_time(threadName, counter, delay):
  lst = []
  while counter:
    if exitFlag:
      threadName.exit()
    time.sleep(delay)
    lst.append("%s: %s" % (threadName, time.ctime(time.time())))
    counter -= 1
  return lst

threads = []

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 1)

# Start new Threads
thread1.start()
thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
  t.join()

print(thread1.lst, thread2.lst)
