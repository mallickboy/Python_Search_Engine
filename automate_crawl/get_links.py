import requests,json,os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

def check_page_validity(reqs,url):
    if  (400 <= reqs.status_code < 500):
            # print(f"HTTP Error {reqs.status_code}: {url}") 
        return False
    else:
        error_keywords = ["not found"]  # Customize based on your needs

        for keyword in error_keywords:
            if keyword in reqs.text.lower():
                    # print(f"Potential error detected: {keyword}")
                return False
    return True

class crawling:
    def __init__(self) -> None:
        pass
    def store_json(self,content, path, file_name):
        def add_url_tag(myset):
            # mylist=list(myset)
            save=[]
            for link in myset:
                save.append({'link':link})
            return save
        content=add_url_tag(content)
        try:
            # Ensure the specified directory exists
            os.makedirs(path, exist_ok=True)

            # Store the content in a JSON file
            with open(os.path.join(path, file_name), 'w') as json_file:
                json.dump(content, json_file)

            # print(f'Stored : {file_name}')
        except Exception as e:
            print(f'Error storing JSON content: {e}')
        print("File stored as : ",file_name,"\t length : ",len(content))


    def GetAllinks_set(self,url, urls_set, d):
        time_limit=2500
        starting=url
        SameDomain=True
        start_time = datetime.now() 
        q=[(url,0)]
        aa,bb=1,1
        count=0
        domain= urlparse(url).netloc
        try:
            while q :
                end_time = datetime.now()
                # if (end_time - start_time).total_seconds()>time_limit:
                #             print("time limit exceeded :",starting)
                #             # self.store_json([starting],'files_bot',f"aaaaaaa_time90s{domain}.json")
                #             self.store_json(urls_set,'files_bot',f"{domain}_{len(urls_set)}.json")
                #             return urls_set
                try:
                    # print(count)
                    url,currDept=q.pop(0)
                    # add_row={'url':url}
                    
                    count+=1
                    # if count % 100==0:
                    #     print(count,"\t",url)
                    # print(currDept)
                    if currDept==d:continue
                    reqs = requests.get(url)
                    if not check_page_validity(reqs,url):continue
                    soup = BeautifulSoup(reqs.text, 'html.parser')

                    for link in soup.find_all('a'):
                        end_time = datetime.now() 
                        if (end_time - start_time).total_seconds()>time_limit:
                            print("time limit exceeded :",starting)
                            # self.store_json([starting],'files_bot',f"aaaaaaa_time90s{domain}.json")
                            self.store_json(urls_set,'files_bot',f"{domain}_{len(urls_set)}.json")
                            return urls_set
                        try:
                                
                                gotLink = link.get('href')
                                if(gotLink !=None):
                                    absLink=urljoin(url,gotLink)
                                    if(SameDomain):
                                        parsed_url = urlparse(absLink)
                                        if parsed_url.netloc != domain:
                                            continue
                                    if 'python' in absLink and absLink not in urls_set:  
                                        q.append((absLink,currDept+1))
                                        urls_set.add(absLink)  
                                        # print("getting links",absLink)
                                
                        except KeyboardInterrupt:
                            print("Inner for loop error :",aa)
                            aa+=1
                            continue
                except (requests.exceptions.RequestException) as e:
                    print("outer while loop error : ",bb," : ",e)
                    bb+=1
                    continue
        except (requests.exceptions.RequestException,KeyboardInterrupt) as e:
            print("outer most error : "," : ",e)
            c=crawling 
        if(len(urls_set)>0):
            print(starting)  
            self.store_json(urls_set,'files_bot',f"{domain}_{len(urls_set)}.json")
        return urls_set


