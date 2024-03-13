import threading
from datetime import datetime
global myfun
class MyCustomThread(threading.Thread):
    thread_id_counter = 1  # Class variable to generate unique thread IDs

    def __init__(self):
        super(MyCustomThread, self).__init__()
        self.val=0
        self.is_running=True
        self.thread_id = MyCustomThread.thread_id_counter
        MyCustomThread.thread_id_counter += 1
    def initialize(self, val):
        self.val=val
    def run(self):
        timestamp1 = datetime.now()
        print(f"Thread : {self.thread_id}  | start ",f"  your function ({self.val})")
        #PROGRAME
        global myfun
        myfun(self.val)
        # print(self.funct,self.val)

        time_difference = (datetime.now() - timestamp1).total_seconds()
        print(f"Thread : {self.thread_id}  | ended in ",time_difference,"s",f"  your function ({self.val})")

class multi_threading_controller:
    def __init__(self,fun) -> None:
        global myfun
        myfun =fun
        self.number,self.task_count,self.done,self.threads_set=0,0,0,[]
    def create_threads(self,number):
        self.number=number
        new_thread=[]
        create_new=min((self.number-len(self.threads_set)),(self.task_count-self.done))
        for i in range(create_new): # creating remaining threads
            self.threads_set.append(MyCustomThread())                  # total - active
            new_thread.append(MyCustomThread())
        # if create_new:
        #     print("                 created : ",create_new)
        return new_thread

    def strart_bulk_task(self,total_task_array,no_threds):
        self.task_count=len(total_task_array)
        threds=self.create_threads(no_threds)
        # handle threds here
        task=0
        while task<self.task_count:
            for th in threds:
                if not task<self.task_count:continue
                th.initialize(total_task_array[task])
                th.start()
                task+=1
            threds=self.replace_dead_threads()
    def replace_dead_threads(self): # clear max
        for thread in self.threads_set:
            if not thread.is_alive(): # if dead
                self.threads_set.remove(thread)
                self.done+=1
                print("Done : ",self.done,"/",self.task_count)
        return self.create_threads(self.number)

        