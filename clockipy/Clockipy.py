import requests
import json

class Clockipy:
    """this object represents the clockify api as a python object"""

    def __init__(self, token):
        self.headers = {"X-Api-Key": "%s" % token}
        self.base_url = "https://api.clockify.me/api/v1"
    
    def request(self, url, options):
        method, path = url.split(" ")

        for key in options:
            path.replace("{%s}" % key, options.get(key))

        result = requests.request(method, "%s%s" % (options.get("base_url") or self.base_url, path), headers={**self.headers, **(options.get("headers") or {})}, json=options.get("body"), params=options.get("query"))
        
        try:
            response = json.loads(result.text)
        except ValueError:
            return result.text

        return response