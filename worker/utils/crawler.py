import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin, parse_qsl, urlencode
from typing import List, Optional
from queue import Queue 
from typing import Iterable, Any

from utils.log import log, Color
from utils.keyword_matching import KEYWORD_MATCHING 

HEADERS = {"User-Agent": "PythonSearchEngine/3.0"}
REQUEST_TIMEOUT = 10    # max 10 second per url request 

class Crawler:
    def __init__(self, max_crawl_depth: int = None, max_crawl_time: int = None , verbose: bool= False, domain_lock: bool= False) -> None:
        self.max_crawl_depth , self.max_crawl_time, self.updated_metadata = max_crawl_depth, max_crawl_time, []
        self.verbose = verbose
        self.domain_lock = domain_lock

    def is_valid_page(self, response: requests.Response ) -> bool :
        if response.status_code >= 400: # discard round 1
            return False

        content_type = response.headers.get("Content-Type") # discard round 2

        if content_type is None or "text/html" not in content_type.lower():
            return False
        
        return True
    
    def collect_metadata(self, current_url: str, soup: BeautifulSoup) -> None:  ## changed (return type should be None)
        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
        log({"link": current_url ,"title": title}, verbose= self.verbose)
        self.updated_metadata.append({"link": current_url ,"title": title})

    def normalize_url(self, url: str, base_url: str = None) -> str:
        """
        Normalize a URL by:
        - Joining relative links to base URL (if provided)
        - Removing fragments (#...)
        - Removing trailing slashes
        - Sorting query parameters
        """
        if base_url:
            url = urljoin(base_url, url)

        parsed = urlparse(url)

        # Remove fragment and normalize path
        path = parsed.path or "/"
        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")

        # Sort query parameters
        query = urlencode(sorted(parse_qsl(parsed.query)))

        normalized = parsed._replace(
            path=path,
            params="",
            fragment="",
            query=query
        )
        return urlunparse(normalized)

    def collect_next_deeper_urls(self, current_url, soup: BeautifulSoup) -> List[str]:
        urls = []
        
        base_domain = urlparse(current_url).netloc if (current_url and self.domain_lock) else None
        
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            normalized = self.normalize_url(href, base_url= current_url)
            
            if self.domain_lock and base_domain: # Include same domain urls
                if urlparse(normalized).netloc != base_domain:
                    continue
            urls.append(normalized)

        return urls 
    
    def is_url_acceptable(self, url: str) -> bool: # discard round 3
        lower_url = url.lower()
        found_allow = False

        for _, (tag, _) in KEYWORD_MATCHING.iter(lower_url):  # unpacking 
            if tag == "block":
                return False
            elif tag == "allow":
                found_allow = True

        return found_allow

    def crawl_url_bfs(self, seed_url: str, max_crawl_depth: int = None, max_crawl_time: int= None) -> None:
        max_crawl_depth = max(max_crawl_depth or self.max_crawl_depth or 0, 0)
        max_crawl_time = max(max_crawl_time or self.max_crawl_time or 60, 0)

        # Main implementation using queue for breath first approach
        visited_urls = set()
        pending_urls = Queue()
        self.current_base_url = self.normalize_url(seed_url)
        pending_urls.put((self.normalize_url(seed_url), 0))

        start_crawl_time = time.time()
        
        while not pending_urls.empty():
            if time.time() - start_crawl_time > max_crawl_time:
                log("Time limit reached. Stopping crawl.", verbose=self.verbose, color=Color.YELLOW)
                break

            current_url, current_depth= pending_urls.get()
            if current_url in visited_urls:
                continue
            visited_urls.add(current_url)

            # Get response
            try:
                response = requests.get(current_url, headers=HEADERS, timeout= REQUEST_TIMEOUT)
            except requests.RequestException as e:
                log(f"Failed to fetch {current_url}: {e}", verbose = self.verbose, color= Color.RED)
                continue

            if not self.is_valid_page(response):
                continue

            # build soup
            soup = BeautifulSoup(response.text, "html.parser")
            self.collect_metadata(current_url= current_url,soup= soup)

            if current_depth < max_crawl_depth: # dig & collect additional urls
                new_urls= self.collect_next_deeper_urls(current_url= current_url, soup= soup) # getting urls form current page
                # 1. generalize the url 
                # 2. check for acceptable key using ahocorasick in linear time
                # 3. if found and new add to queue
                for new_url in new_urls:
                    if new_url and new_url not in visited_urls and self.is_url_acceptable(new_url):
                        pending_urls.put((new_url, current_depth+1))

    def crawl(self, seed_url: str, max_crawl_depth: int = None, max_crawl_time: int= None) -> List[Any]:
        try:
            self.crawl_url_bfs(seed_url= seed_url, max_crawl_depth= max_crawl_depth, max_crawl_time= max_crawl_time)
            log("Task Completed Successfully", verbose=self.verbose, color=Color.GREEN)
            return self.updated_metadata if self.updated_metadata else []
        except KeyboardInterrupt:
            log("Exiting With Error: KeyboardInterrupt", verbose=self.verbose, color=Color.RED)
            return self.updated_metadata if self.updated_metadata else []
        except Exception as e:
            log(f"Exiting With Error: {type(e).__name__}", verbose=self.verbose, color=Color.RED)
            return self.updated_metadata if self.updated_metadata else []

if __name__== "__main__":
    cwl= Crawler(max_crawl_depth= 1, max_crawl_time= 6, verbose= True, domain_lock= False)
    data= cwl.crawl(seed_url= "https://python.org")
    print("Got Data: ",len(data))
