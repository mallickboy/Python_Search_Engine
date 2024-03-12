from get_links_old import crawling as bot
import threading,time
import pandas as pd
global all_links
all_links=set()
# bot.GetAllinks_set(url="https://www.w3schools.com/python/",urls_set=links,d=3)
# print("total links : ",len(links))
# bot.store_json(content=links,path='file',file_name='w3schools.json')

class MyCustomThread(threading.Thread):
    thread_id_counter = 1  # Class variable to generate unique thread IDs

    def __init__(self):
        super(MyCustomThread, self).__init__()
        self.is_running=True
        self.thread_id = MyCustomThread.thread_id_counter
        MyCustomThread.thread_id_counter += 1
    def initialize(self, url,d):
        self.start_url=url
        self.depth=d
    def run(self):
        print(f"Thread : {self.thread_id}  | start ")
        global all_links
        bot.GetAllinks_set(url=self.start_url,urls_set=all_links,d=self.depth)
        # print("total links : ",len(all_links))
        print(f"Thread : {self.thread_id}  | end")
        # return True # done

l1="https://www.w3schools.com/python/"
th1=MyCustomThread()
th1.initialize(l1,1)
# th1.start()

l2="https://www.programiz.com/python-programming"
th2=MyCustomThread()
th2.initialize(l2,1)
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
    
    def handle_all_threads(self,starting_links):
        global all_links
        if len(self.thread_list)==0 or self.no_of_threads==0:
            return "Please create threads first"
        i=0
        len_strting_links=len(starting_links)
        while i<len_strting_links:
            try:
                print("\nCount : ",i+1," Remaining :",len(starting_links)-i ," Collected urls : ",len(all_links),"\n\n")
                self.get_n_threads(18)
                for j in range(self.no_of_threads):
                    if i<len(starting_links):
                        x=self.thread_list[j]

                        x.initialize(starting_links[i],1)
                            
                        x.start()
                        i+=1

                for j in range(self.no_of_threads):
                    if i<len(starting_links):
                        x=self.thread_list[j]
                        x.join()
                
            except KeyboardInterrupt as e:
                print("Exitting : ",e)
                break
        print("Final url collected : ",len(all_links))
        bot.store_json(content=all_links,path='files_bot',file_name='all_links_old.json')


            


bc=batch_crawling()
surl=bc.get_starting_urls('./new_data/starting_urls/python_tutorial.json','link')
# print(surl)
th=bc.get_n_threads(5)
print(th)
bc.handle_all_threads(surl)
print(len(all_links))