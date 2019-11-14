from core.prototypes import AbstractScanner
from urllib.parse import urlencode
import requests
import re
STATS_SEARCHPATTERN = r'<div id="resultStats>([^>]+)'
LINK_SEARCHPATTERN = r'<div class="r"><a href="([^"]+)"'
RESULT_REGEXP = re.compile(LINK_SEARCHPATTERN)
class GoogleSearcher(AbstractScanner):
    def __init__(self:
        pass
    def scan_address(self, query:'google_search_query')->{"search_result_list"}:
        search_url = "http://google.com/search?%s"
        num_loaded_results = 100
        start = 0
        search_result_list = set()
        while num_loaded_results == 100:
            query_params = {
            "num":100,
            "q":query,
            "start":start,
            "filter":0
            }
            page = requests.get(search_url % urlencode(query_params))
            if page.status_code != 200:
                break
            start += 100
            result_page = set(RESULT_REGEXP.findall(page_text))
            num_loaded_results = len(result_page)
            


