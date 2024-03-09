import requests,json,os
from bs4 import BeautifulSoup


class crawling:
    def __init__(self) -> None:
        pass
    def GetAllinks_set(url, urls_set, d):
        q=[(url,0)]
        aa,bb=1,1
        count=0
        try:
            while q :
                try:
                    
                    url,currDept=q.pop(0)
                    # add_row={'url':url}
                    if url in urls_set:
                        continue
                    urls_set.add(url)
                    count+=1
                    if count % 100==0:
                        print(count,"\t",url)
                    # print(currDept)
                    if currDept==d:
                        continue
                    reqs = requests.get(url)
                    soup = BeautifulSoup(reqs.text, 'html.parser')
                    for link in soup.find_all('a'):
                        try:
                            gotLink = link.get('href')
                            
                            if(gotLink !=None):
                                if 'http' in gotLink:
                                    if 'python' in gotLink:
                                        # if gotLink not in urls:
                                        q.append((gotLink,currDept+1))
                                
                                else:
                                    q.append((url+gotLink,currDept+1))
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
            return urls_set 
        return urls_set

    def store_json(content, path, file_name):
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

            print(f'Stored : {file_name}')
        except Exception as e:
            print(f'Error storing JSON content: {e}')
        print("File stored as : ",file_name)
