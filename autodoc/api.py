from typing import TypeVar
from octokit import Octokit
from typing import TypeVar
from .models import *
import json

T = TypeVar('T')
def api_github(url: str, octokit: Octokit) -> List[T]:
    """Retrieve data from GitHub

    Args:
        url (str): link to data
        octokit (Octokit): lib to retrieve data

    Returns:
        json[T]: json formed data
    """
    data = octokit.request(url,{})
    data_dump = json.dumps(data, indent=4)
    data_json = json.loads(data_dump)
    return data_json

def parse_url(url: str) -> str:
    """Parses the url to the api endpoint

    Args:
        url (str): initial url

    Returns:
        str: endpoint
    """
    return url.replace("https://api.github.com", "GET ")
    

'''
Here is the code in charge of retrieve data from the source repository and save it in files.txt
'''

def get_repository(url: str, octokit: Octokit) -> Repository:
    """Creates the repository retrieving all the data from GitHub

    Args:
        url (str): link to GitHub api
        octokit (Octokit): lib to retrieve data

    Returns:
        Repository: repository retrieved
    """
    repository_json = api_github(url, octokit)
    repository = Repository.create(repository_json)
    
    contributors_url = parse_url(repository_json['contributors_url'])
    repository.contributors = get_contributors(contributors_url, octokit)
    
    '''TODO
    Retrieve repository commits
    '''
    
    '''TODO
    Retrieve repository issues
    '''
    
    print(repository)
    return repository
    
def get_contributors(url: str, octokit: Octokit) -> List[Contributor]:
    """Creates the repository's contributors list

    Args:
        url (str): link to contributors
        octokit (Octokit): lib to retrieve data

    Returns:
        List[Contributor]: repository's contributors list
    """
    contributors_json= api_github(url, octokit)
    return Contributor.createContributors(contributors_json)

    """TODO
    Def retrieve commits function
    """
    
    """TODO
    Def retrieve issues function
    """