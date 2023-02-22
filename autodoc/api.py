from typing import List, TypeVar
from octokit import Octokit
from .models import *
import json

T = TypeVar('T')
def api_github(octokit: Octokit, url: str, front_path: str = '', back_path: str = '') -> List[T]:
    """Retrieve data from GitHub

    Args:
        url (str): link to data
        octokit (Octokit): lib to retrieve data
        front_path (str): front path to retrieve
        back_path (str): back path to retrieve

    Returns:
        List[T]: json formed data
    """
    endpoint = parse_url(url, front_path, back_path)
    data = octokit.request(endpoint, {"accept": "application/vnd.github+json"})
    data_dump = json.dumps(data, indent=4)
    return json.loads(data_dump)

def parse_url(url: str, front_path: str, back_path: str) -> str:
    """Parses the url to the api endpoint

    Args:
        url (str): initial url
        front_path (str): front path to retrieve
        back_path (str): back path to retrieve

    Returns:
        str: endpoint
    """
    dotcom_index = url.rfind(".com")
    url_modified = url[dotcom_index + 4:]
    return f"GET {front_path}{url_modified}{back_path}"
    


'''
Here is the code in charge of retrieve data from the source repository and save it in files.txt
'''

def get_repository(octokit: Octokit, url: str) -> Repository:
    """Creates the repository retrieving all the data from GitHub

    Args:
        octokit (Octokit): lib to retrieve data
        url (str): link to GitHub api

    Returns:
        Repository: repository retrieved
    """
    repository_json = api_github(octokit, url, front_path='/repos', back_path='')
    repository = Repository.create(repository_json)
    
    contributors_url = repository_json['contributors_url']
    repository.contributors = get_contributors(octokit, contributors_url)
    
    '''TODO
    Retrieve repository commits
    '''
    
    '''TODO
    Retrieve repository issues
    '''
    
    print(repository)
    return repository
    
def get_contributors(octokit: Octokit, url: str) -> List[Contributor]:
    """Creates the repository's contributors list

    Args:
        url (str): link to contributors
        octokit (Octokit): lib to retrieve data

    Returns:
        List[Contributor]: repository's contributors list
    """
    contributors_json = api_github(octokit, url, front_path='', back_path='')
    return Contributor.createContributors(contributors_json)
    
def get_commits(octokit: Octokit, url: str) -> List[Commit]:
    """TODO
    Def retrieve commits function
    """
    pass
    
def get_issues(octokit: Octokit, url: str) -> List[Commit]:
    """TODO
    Def retrieve issues function
    """
    pass