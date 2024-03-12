from get_links import crawling as bot2
import threading,time
import pandas as pd
global all_links
all_links=set()
# bot.GetAllinks_set(url="https://www.w3schools.com/python/",urls_set=links,d=3)
# print("total links : ",len(links))
# bot.store_json(content=links,path='file',file_name='w3schools.json')
bot=bot2()
class MyCustomThread(threading.Thread):
    thread_id_counter = 1  # Class variable to generate unique thread IDs

    def __init__(self):
        super(MyCustomThread, self).__init__()
        self.is_running=True
        self.thread_id = MyCustomThread.thread_id_counter
        MyCustomThread.thread_id_counter += 1
    def initialize(self, url,storage_set,d):
        self.storage=storage_set
        self.start_url=url
        self.depth=d
    def run(self):
        print(f"Thread : {self.thread_id}  | start ")
        bot.GetAllinks_set(url=self.start_url,urls_set=self.storage,d=self.depth)
        # print("total links : ",len(all_links))
        print(f"Thread : {self.thread_id}  | end")
        # return True # done

l1="https://www.w3schools.com/python/"
th1=MyCustomThread()
# th1.initialize(l1,1)
# th1.start()

l2="https://www.programiz.com/python-programming"
th2=MyCustomThread()
# th2.initialize(l2,1)
# th2.start()

# print("total links : ",len(all_links))
# bot.store_json(content=all_links,path='files_bot',file_name='w3schools.json')

class batch_crawling:
    def __init__(self) -> None:
        pass
    def get_starting_urls(self,file,get_label):
        res=set()
        data=pd.read_json(file)
        # print(data['link'])
        for index,row in data.iterrows():
            res.add(row[get_label])
            # print(row[get_label])
        return list(res)
    def get_n_threads(self,n):
        self.thread_list=[]
        self.no_of_threads=n
        for i in range(n):
            new_thread=MyCustomThread()
            self.thread_list.append(new_thread)
        return self.thread_list
        
    def handle_all_threads(self, starting_links, crawl_depth, total_threads):
        global all_links
        self.links=set()
        self.store_all = []
        i = 0
        len_starting_links = len(starting_links)
        all_links = set()  # Initialize all_links as an empty set

        while i < len_starting_links:
            try:
                print("\nCount : ", i + 1, " Remaining :", len(starting_links) - i, " Collected urls : ", len(all_links), "\n\n")
                self.get_n_threads(total_threads)
                started_threads = []  # List to keep track of started threads
                for j in range(self.no_of_threads):
                    if i+j < len(starting_links):
                        storage_set = set()  # Create a new empty set for each thread
                        x = self.thread_list[j]
                        self.store_all.append(storage_set)
                        x.initialize(starting_links[i+j], storage_set, crawl_depth)  # Pass the storage set to the thread
                        x.start()  # Start the thread
                        started_threads.append(x)  # Add the started thread to the list
                        # i += 1

                # Join only the started threads and collect links
                for j,thread in enumerate(started_threads):  # Loop over the started threads
                    
                    thread.join()  # Wait for each started thread to complete
                    all_links.update(self.store_all[j])  # Update all_links with the links from the current thread's storage_set
                    i+=1
                    if i+j > len(starting_links):break

            except KeyboardInterrupt as e:
                print("Exiting:", e)
                break

        print("Final url collected : ", len(all_links))
        bot.store_json(content=all_links, path='files_bot', file_name='all_links.json')


            
from datetime import datetime
timestamp1 = datetime(2022, 3, 1, 10, 30, 0)

bc=batch_crawling()
surl=bc.get_starting_urls('./new_data/starting_urls/python_tutorial.json','link')
# print(surl)
th=bc.get_n_threads(5)
print(th)
bc.handle_all_threads(surl,2,16)

print(len(all_links))
timestamp2 = datetime(2022, 3, 1, 11, 15, 0)

# Calculate the time difference
time_difference = timestamp2 - timestamp1
print("Time difference:", time_difference)