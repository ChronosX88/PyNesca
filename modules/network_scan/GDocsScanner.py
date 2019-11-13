import json
import requests
from urllib.parse import urlencode, urljoin
import lxml.html
from core.prototypes.AbstractScanner import AbstractScanner
class GDocsScanner(AbstractScanner):
    def __init__(self, timeout:"timeout"):
        pass
    def scan_address(self, prefix:"gdoc_prefix", ghash:"gdoc_hash") -> {"response",
    "gdoc_info", "gdoc_title"}:
        print("Scanning", prefix, ghash)
        response = requests.get(prefix+ghash)
        if response.status_code != 200:
            return {"response":response, "gdoc_info":None, "gdoc_title":None}
        print(response.status_code)
        response_tree = lxml.html.fromstring(response.text)
        (title,) = response_tree.xpath("//meta[@property='og:title']/@content")
        (token_container,) = response_tree.xpath('//script[contains(text(),"token")]')
        token_container = token_container.text
        token_container = token_container[token_container.find("{"):token_container.rfind("}") + 1]
        #print(json.dumps(json.loads(token_container), indent=4, sort_keys=True))
        try:
            info_params = json.loads(token_container)["info_params"]
        except json.JSONDecodeError:
            return {"response":response, "gdoc_info":None, "gdoc_title":None}
        #print(info_params)
        info = None
        if "token" in info_params.keys():
            info_params.update({"id":ghash})
            info_url = urljoin(prefix, ghash+"/docdetails/read?"+urlencode(info_params))
            print(info_url)
            info_text = requests.get(info_url).text
            info = json.loads(info_text[info_text.find("\n") + 1:])
            print(info)
        return {"response":response, "gdoc_info":info,
        "gdoc_title":title}
