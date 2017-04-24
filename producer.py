from lib.task_queue import Queue
from random import randint

MAX_TASK = 500
STAR_NUMBER = 2000000000000000
FINAL_NUMBER = 9999999999999999

q1 = Queue(["127.0.0.1:11211"])

for i in range(MAX_TASK):
    value = randint(STAR_NUMBER, FINAL_NUMBER)
    q1.enqueue(value)


q2 = Queue(["127.0.0.1:11212"])

for i in range(MAX_TASK):
    value = randint(STAR_NUMBER, FINAL_NUMBER)
    q2.enqueue(value)



