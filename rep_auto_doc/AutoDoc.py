from typing import List, TypeVar
import json

class AutoDoc:
    
    def __init__(self, repo_url, token, octokit, work_dir, repo_dict) -> None:
        self.repo_url = repo_url
        self.token = token
        self.work_dir = work_dir
        self.octokit = octokit
        self.repo_dict = repo_dict
        
    # Data saving
    def data_saving(self, file_name: str, data: str) -> None:
        with open(".\data\\retrieved\{}".format(file_name), "w") as file:
            for line in data:
                file.write(line)
                
    # Api call
    T = TypeVar('T')
    def api_call(self, url) -> List[T]:
        data = self.octokit.request(url,{})
        data_json = json.dumps(data, indent=4)
        data_dict = json.loads(data_json)
        return [data,data_json,data_dict]
    
    # Write MD
    def to_markdown(self, src: str, dst: str) -> None:
        file = []
        with open(r".\data\templates\doc.txt", "r") as template:
            for line in template:
                if r"{}" in line:
                    s = line.replace(r"{}","1")
                file.append(line)
        doc = open(dst, "w")
        doc.writelines(file)
        doc.close()
    
    
    """
    Here is the code in charge of retrieve data from the source repository and save it in files.txt
    """
    # Retrieve repository data
    def repository_data(self) -> None:
        url = "GET /repos/{}/{}".format('laurolmer', 'Acme-L3-D01')
        _, repo_json, repo_dict = self.api_call(url)
        self.data_saving('repo_json.txt', repo_json)
        
    # Retrieve contributors data
    def contributors_data(self) -> None:
        url_contributors = str(self.repo_dict["contributors_url"]).replace("https://api.github.com", "GET ")
        _, contributors_json, _ = self.api_call(url_contributors)
        self.data_saving('contributors.txt', contributors_json)
