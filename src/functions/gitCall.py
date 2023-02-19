from lib.octokitpy.octokit import Octokit
import json

# Api-Key Configuration
token = open(r"..\auth\token.txt", "r")
api_key = token.read()
token.close()
octokit = Octokit(api_key)

# Data saving
def data_saving(file_name, data):
    with open(".\data\\retrieved\{}".format(file_name), "w") as file:
        for line in data:
            file.write(line)

# Api call       
def api_call(url):
    data = octokit.request(url,{})
    data_json = json.dumps(data, indent=4)
    data_dict = json.loads(data_json)
    return [data,data_json,data_dict]

# Retrieve repository data
url = "GET /repos/{}/{}".format('laurolmer', 'Acme-L3-D01')
_,repo_json,repo_dict = api_call(url)
data_saving('repo_json.txt',repo_json)

# Retrieve contributors data
url_contributors = str(repo_dict["contributors_url"]).replace("https://api.github.com", "GET ")
_,contributors_json,_ = api_call(url_contributors)
data_saving('contributors.txt',contributors_json)