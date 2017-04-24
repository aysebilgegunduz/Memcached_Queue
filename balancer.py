from lib.task_queue import Queue

q1 = Queue(["127.0.0.1:11211"])
q2 = Queue(["127.0.0.1:11212"])

while True:
    q1_task_num = q1.show_tail() - q1.show_head()
    q2_task_num = q2.show_tail() - q2.show_head()
    if (q1_task_num - q2_task_num) > 1:
        """
        Q1 has much more task then Q2
        """
        print("Balancing..! Q1 = {0} | Q2 = {1}".format(q1_task_num, q2_task_num))
        q = q1.dequeue()
        q2.enqueue(q)
        continue
    if (q2_task_num - q1_task_num) > 1:
        """
        Q2 has much more task then Q1
        """
        print("Balancing..! Q2 = {0} | Q1 = {1}".format(q2_task_num, q1_task_num))
        q = q2.dequeue()
        q1.enqueue(q)