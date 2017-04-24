from math import sqrt
from itertools import count, islice
from lib.task_queue import Queue
import threading



"""
We created a new class that inherited from built-in Treading class of python
"""

NUMBER_OF_THREAD = 2


class myThread(threading.Thread):

    def __init__(self, threadID, name, socket):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = Queue(socket)

    """
    That is automatically called by start() function of super class.
    """
    def run(self):

        print("Starting Thread {0}".format(self.threadID))

        """
        Create a loop and check queue forever.
        """
        while True:
            if self.q.is_empty() is False:

                """
                A new task taken from Memcache.
                """
                value = self.q.dequeue()
                print("[{0}] Calculating for {1}".format(self.name, value))

                """
                Calculate is it prime or not. That may take some time depends on given number.
                """
                result = self.is_prime(value)
                print("[{0}] Result = {1}".format(self.name, bool(result)))

    """
    A function that decides prime numbers by using functions
    from math and itertools libraries.
    """
    def is_prime(self, n):
        if n < 2: return False
        for number in islice(count(2), int(sqrt(n)-1)):
            if not n%number:
                return False
        return True

"""
Create a NUMBER_OF_THREAD and start them immediately.
"""
for i in range(NUMBER_OF_THREAD):
    thread = myThread(i, "Q1-Thread-{0}", ["127.0.0.1:11211"])
    thread.start()

for i in range(NUMBER_OF_THREAD):
    thread = myThread(i, "Q2-Thread-{0}", ["127.0.0.1:11212"])
    thread.start()

print("Exiting Main Thread")