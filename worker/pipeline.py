from utils.thread import ThreadPool
import time
from mallickboy import runtime

@runtime
def check_multi_threading():
    def my_task(val):
        time.sleep(1)
        # print(f"Processed: {val}", end="\t")
        return {val: val**2}

    pool = ThreadPool(task_function=my_task, num_workers=2, verbose=True)
    pool.add_tasks(list(range(3)))  # 10 tasks
    pool.start()
    results = pool.wait_completion()
    print("Results:", results)


from utils.crawler import Crawler

@runtime
def check_crawler():
    spider= Crawler(max_crawl_depth= 0, max_crawl_time= 6, verbose= False, domain_lock= False)
    data= spider.crawl(seed_url= "https://python.org")
    print("Got Data: ",len(data))

if __name__ == "__main__":
    check_multi_threading()
    
    check_crawler()

    pass