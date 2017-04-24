import pylibmc


class Queue:
    def __init__(self, address):
        self.client = pylibmc.Client(address)

    """
    Return head number.
    """
    def show_head(self):
        return self.client.get("head")

    """
    Return tail number.
    """
    def show_tail(self):
        return self.client.get("tail")


    """
    Return T/F depends on queue is empty or not.
    We are using try/except because pylibmc fires an exception
    if request index (head and tail) not exist.
    """
    def is_empty(self):

        try:
            head = self.client.get("head")
        except pylibmc.NotFound as e:
            head = None
        try:
            tail = self.client.get("tail")
        except pylibmc.NotFound as e:
            tail = None

        """
        If head or tail is None that means we haven't send task yet. Thus is_empty must return True because queue is empty.
        """
        if (head is None) or (tail is None) or (head >= tail):
            return True
        return False

    """
    Send a new number to the queue.
    """
    def enqueue(self, item):
        """
        If id not exist NotFound exception will be fired. Which means we are adding our first task.
        which means we gotta create tail and head indexes with initial value that is 1.
        """
        try:
            id = self.client.incr("tail")
        except pylibmc.NotFound as e:
            self.client.add("tail", 1)
            self.client.add("head", 1)
            id = 1

        """
        We are setting 1 to id above exception section because if we are adding tail & head
        that mean this is qoing to be the first task since memcache started.

        Otherwise we incrementing tail and using it as a index for new task.
        """
        self.client.add("task_{0}".format(id), item)

    """
    Take new task from queue.
    """
    def dequeue(self):
        """
        Checking queue status. We can't request a new task if it's empty
        """
        if self.is_empty():
            return False

        """
        Getting tail & head numbers from memcache. If head is <= to the tail that means there is a least one task
        """
        tail = self.client.get("tail")
        id = self.client.incr("head")
        if id <= tail:
            """
            Get task and then delete it from queue in order to block double calculation.
            And finally return task.
            """
            tmp = self.client.get("task_{0}".format(id-1))
            self.client.delete("task_{0}".format(id-1))
            return tmp

        """
        We have to decrement the head value if there is no task at queue.
        """
        self.client.decr("head")
        return False
