from typing import List, TypeVar, Dict
from octokit import Octokit

from autodoc.models.Report import Report
from clockipy import Clockipy
from autodoc.models import *

A = TypeVar('A')
T = TypeVar('T')
GITHUB_API_HEADERS = {"accept": "application/vnd.github+json"}
CLOCKIFY_API_HEADERS = {}


def api_call(api_interface: A, url: str, header: dict = Dict, front_path: str = '', back_path: str = '') -> List[T]:
    """Retrieve data from GitHub

    Args:
        header (dict):
        url (str): link to data
        api_interface (A): interface to retrieve data where A = {Octokitpy, Clockipy}
        front_path (str): front path to retrieve
        back_path (str): back path to retrieve

    Returns:
        List[T]: json formed data
    """
    endpoint = parse_url(url, front_path, back_path)
    data = api_interface.request(endpoint, header)
    data_dump = json.dumps(data, indent=4)
    return json.loads(data_dump)


def parse_url(url: str, front_path: str, back_path: str) -> str:
    """Parses the url to the api endpoint. If it contains curved braces '{}' means
    that we have an optional path we have to control.
    
    Attention:
        - front_path and back_path: you must add the left '/' inside the path. For example:
            - front_path: '/git'
            - back_path: '/git'

    Args:
        url (str): initial url
        front_path (str): front path to retrieve
        back_path (str): back path to retrieve

    Returns:
        str: endpoint
    """
    if "github.com" in url:
        initial_index = url.rfind("github.com") + len("github.com")
        final_index = url.rfind("{") if "{" in url else None
        basic_url = url[initial_index: final_index]
        return f"GET {front_path}{basic_url}{back_path}"
    if "clockify.me" in url:
        initial_index = url.rfind("api.clockify.me/api/v1") + len("api.clockify.me/api/v1")
        basic_url = url[initial_index:]
        return f"GET {front_path}{basic_url}"


'''
Here is the code in charge of retrieve data from the source repository
'''


def get_repository(octokit: Octokit, url: str) -> Repository:
    """Creates the repository retrieving all the data from GitHub

    Args:
        octokit (Octokit): lib to retrieve data
        url (str): link to GitHub api

    Returns:
        Repository: repository retrieved
    """
    repository_json = api_call(octokit, url, GITHUB_API_HEADERS, front_path='/repos', back_path='')
    repository = Repository.create(repository_json)

    contributors_url = repository_json['contributors_url']
    repository.contributors = get_contributors(octokit, contributors_url)

    commits_url = repository_json['commits_url']
    repository.commits = get_commits(octokit, commits_url)

    issues_url = repository_json['issues_url']
    repository.issues = get_issues(octokit, issues_url)

    return repository


def get_contributors(octokit: Octokit, url: str) -> List[Contributor]:
    """Creates the repository's contributors list

    Args:
        url (str): link to contributors
        octokit (Octokit): lib to retrieve data

    Returns:
        List[Contributor]: repository's contributors list
    """
    contributors_json = api_call(octokit, url, GITHUB_API_HEADERS, front_path='', back_path='')
    return Contributor.create_contributors(contributors_json)


def get_commits(octokit: Octokit, url: str) -> List[Commit]:
    """Creates the repository's commits list

    Args:
        octokit (Octokit): lib to retrieve data
        url (str): link to commits

    Returns:
        List[Commit]: commits list
    """
    commits_json = api_call(octokit, url, GITHUB_API_HEADERS, front_path='', back_path='')
    return Commit.create_commits(commits_json)


def get_issues(octokit: Octokit, url: str) -> List[Issue]:
    """Creates the repository's issues list

    Args:
        octokit (Octokit): lib to retrieve data
        url (str): link to issues

    Returns:
        List[Commit]: issues list
    """
    issues_json = api_call(octokit, url, GITHUB_API_HEADERS, front_path='', back_path='')
    return Issue.create_issues(issues_json)


'''
Here is the code in charge of retrieve data from clockify
'''


def get_clockify(clockipy: Clockipy, clockify_url: str, clockify_ws: str) -> Report:
    """Creates the clockify object retrieving all the data from Clokify

    Args:
        clockipy: lib to retrieve data
        clockify_url: api endpoint

    Returns:
        clokifyInfo
    """
    workspaces = api_call(clockipy, clockify_url, CLOCKIFY_API_HEADERS, front_path='', back_path='')
    selected_ws = list(filter(lambda ws: clockify_ws in ws['name'], workspaces))[0]
    contributors = list(map(lambda ws_member: ws_member['userId'], selected_ws['memberships']))
    print(contributors)
