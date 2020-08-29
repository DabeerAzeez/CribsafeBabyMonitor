import threading


class MyThread(threading.Thread):
    '''Created a subclass of threads from the Threading module with an instance variable 'val' that can be updated and read'''
    def __init__(self, target):
        super().__init__(target=target)
        self.val = [0,0]
