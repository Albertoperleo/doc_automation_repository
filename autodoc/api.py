import json
from typing import List, TypeVar, Tuple
from octokit import Octokit

from autodoc.models.Report import Report
from clockipy import Clockipy
from autodoc.models import *

import difflib

T = TypeVar('T')
GITHUB_API_HEADERS = {"accept": "application/vnd.github+json"}
DEFAULT_URL_OPTIONS = {"front_path": "", "back_path": ""}
REPORT_BASE_URL = "https://reports.api.clockify.me/v1"
DETAILED_FILTER = {"page": 1, "pageSize": 50}
CLOCKIFY_API_REPORTS_BODY = {
    "dateRangeStart": "2023-02-18T00:00:00.000",
    "dateRangeEnd": "2023-03-17T00:00:00.000",
    "detailedFilter": DETAILED_FILTER,
    "exportType": "JSON"
}


def api_call(api_interface, url: str, req_options: dict, url_options: dict) -> List[T]:
    """
    This function is used to make API calls to the GitHub and Clockify APIs.

    Parameters
    ----------
    api_interface :
        The API interface to use.
    url : str
        The URL to use.
    req_options : dict
        The request options to use.
    url_options : dict
        The URL options to use.

    Returns
    -------
    List[T]
        The data returned by the API call.
    """
    keyword = "github.com" if type(api_interface) == Octokit else "api.clockify.me/api/v1"
    endpoint = parse_url(keyword, url, url_options)
    data = api_interface.request(endpoint, req_options)
    data_dump = json.dumps(data, indent=4)
    return json.loads(data_dump)


def parse_url(keyword: str, url: str, options: dict) -> str:
    """
    Parses the URL and returns the basic URL.

    Parameters
    ----------
    keyword : str
        The keyword to be searched in the URL.
    url : str
        The URL to be parsed.
    options : dict
        The options to be used for parsing the URL.

    Returns
    -------
    str
        The basic URL.
    """
    initial_index = url.rfind(keyword) + len(keyword)
    final_index = url.rfind("{") if "{" in url else None
    basic_url = url[initial_index: final_index]
    method = "POST" if options.get("report") else "GET"
    return f"{method} {options.get('front_path')}{basic_url}{options.get('back_path')}"


"""
Here is the code in charge of retrieve data from the source repository
"""


def get_repository(octokit: Octokit, url: str) -> Repository:
    """
    Get a repository from the given url.

    :param octokit: The Octokit object.
    :param url: The url of the repository.
    :return: The repository.
    """
    url_options = {"front_path": "/repos", "back_path": ""}
    repository_json = api_call(octokit, url, GITHUB_API_HEADERS, url_options)
    repository = Repository.create(repository_json)

    contributors_url = repository_json['contributors_url']
    repository.contributors = get_contributors(octokit, contributors_url)

    commits_url = repository_json['commits_url']
    repository.commits = get_commits(octokit, commits_url)

    issues_url = repository_json['issues_url']
    repository.issues = get_issues(octokit, issues_url)

    return repository


def get_contributors(octokit: Octokit, url: str) -> List[Contributor]:
    """
    Get the contributors of a repository.

    :param octokit: The Octokit object.
    :param url: The URL of the repository.
    :return: A list of Contributor objects.
    """
    contributors_json = api_call(octokit, url, GITHUB_API_HEADERS, DEFAULT_URL_OPTIONS)
    return Contributor.create_contributors(contributors_json)


def get_commits(octokit: Octokit, url: str) -> List[Commit]:
    """
    Get the commits from the given url.

    :param octokit: The Octokit object.
    :param url: The url to get the commits from.
    :return: The commits from the given url.
    """
    commits_json = api_call(octokit, url, GITHUB_API_HEADERS, DEFAULT_URL_OPTIONS)
    return Commit.create_commits(commits_json)


def get_issues(octokit: Octokit, url: str) -> List[Issue]:
    """
    Get the issues from the given URL.

    :param octokit: The Octokit object.
    :param url: The URL to get the issues from.
    :return: The list of issues.
    """
    issues_json = api_call(octokit, url, GITHUB_API_HEADERS, DEFAULT_URL_OPTIONS)
    return Issue.create_issues(issues_json)


"""
Here is the code in charge of retrieve data from clockify
"""


def get_clockify(clockipy: Clockipy, clockify_url: str, clockify_ws: str, repository: Repository) -> Report:
    """
    Get the Clockify report for the given repository.

    :param clockipy: The Clockify API client.
    :param clockify_url: The Clockify API URL.
    :param clockify_ws: The Clockify workspace name.
    :param repository: The repository to get the report for.
    :return: The Clockify report.
    """
    workspaces = api_call(clockipy, clockify_url, {}, DEFAULT_URL_OPTIONS)
    selected_ws = list(filter(lambda ws: clockify_ws in ws['name'], workspaces))[0]

    url_options = DEFAULT_URL_OPTIONS.copy()
    url_options["back_path"] = f"/{selected_ws['id']}/users"
    members = api_call(clockipy, clockify_url, {}, url_options)
    for ws_member in members:
        associate_member(ws_member, repository.contributors)

    url_options["back_path"] = f"/{selected_ws['id']}/reports/detailed"
    url_options["report"] = True
    req_options = {
        "base_url": REPORT_BASE_URL,
        "body": CLOCKIFY_API_REPORTS_BODY
    }
    detail_report = api_call(clockipy, clockify_url, req_options, url_options)

    time_entries = detail_report['timeentries']
    parsed_detail_report = {}
    for entry in time_entries:
        user_name = entry['userName']
        description = entry['description']
        duration = entry['timeInterval']['duration']
        if user_name in parsed_detail_report:
            parsed_detail_report[user_name].append((description, duration))
        else:
            parsed_detail_report[user_name] = [(description, duration)]

    for user, entries in parsed_detail_report.items():
        parsed_detail_report[user] = append_durations(entries)

    return parsed_detail_report


def associate_member(member: json, contributors: List[Contributor]) -> None:
    """
    Associate a Clockify member with a Contributor.

    :param member: A Clockify member.
    :param contributors: A list of Contributors.
    :return: None.
    """
    for contributor in contributors:
        if difflib.SequenceMatcher(None, member['name'], contributor.nickname).ratio() > 0.5:
            contributor.clockify_id = member['id']


def append_durations(entries: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    """
    Append durations for each description.

    :param entries: A list of entries.
    :type entries: List[Tuple[str, float]]
    :return: A list of tuples of description and total duration.
    :rtype: List[Tuple[str, float]]
    """
    duration_per_description = {}
    for entry in entries:
        description = entry[0]
        duration = entry[1]
        if description in duration_per_description:
            duration_per_description[description] += duration
        else:
            duration_per_description[description] = duration

    duration_per_description_tuples = []
    for description, total_duration in duration_per_description.items():
        duration_per_description_tuples.append((description, round(total_duration/3600, 2)))
    return duration_per_description_tuples
