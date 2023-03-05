from __future__ import annotations
from typing import List
from .Contributor import Contributor
from .Commit import Commit
from .Issue import Issue
import json


class Repository:
    def __init__(self, 
                 repo_id: str, 
                 name: str, 
                 full_name: str, 
                 owner: str,
                 description: str, 
                 private: bool, 
                 html_url: str, 
                 api_url: str, 
                 contributors: List[Contributor],
                 events: str,
                 assignees: str,
                 commits: List[Commit],
                 issues: List[Issue],
                 open_issues: int,
                 created_at: str,
                 language: List[str],
                 has_projects: bool) -> None:
        self.id = repo_id
        self.name = name
        self.full_name = full_name
        self.owner = owner
        self.description = description
        self.private = private
        self.html_url = html_url
        self.api_url = api_url
        self.contributors = contributors
        self.events = events
        self.assignees = assignees
        self.commits = commits
        self.issues = issues
        self.open_issues = open_issues
        self.created_at = created_at
        self.language = language
        self.has_projects = has_projects
        
    @staticmethod
    def create(repository_json: json) -> Repository:
        repo_id = repository_json['id']
        name = repository_json['name']
        full_name = repository_json['full_name']
        owner = repository_json['owner']['login']
        description = repository_json['description']
        html_url = repository_json['html_url']
        api_url = repository_json['url']
        private = repository_json['private'] == 'true'
        events = repository_json['events_url']
        assignees = repository_json['assignees_url']
        open_issues = int(repository_json['open_issues'])
        created_at = repository_json['created_at']
        language = [repository_json['language']]
        has_projects = repository_json['has_projects'] == 'true'
        
        return Repository(repo_id, 
                          name, 
                          full_name,
                          owner,
                          description,
                          private,
                          html_url, 
                          api_url,
                          None,
                          events,
                          assignees,
                          None,
                          None,
                          open_issues,
                          created_at,
                          language,
                          has_projects)
        
    def __str__(self) -> str:
        separator = '#'*60
        title = '\t\tREPOSITORY INFORMATION'
        details = 'Name: {0}\nCreated at: {1}\nLanguage: {2}\nDescription: {3}\nOpen issues: {4}\nContributors: {5}'.format(
            self.name, self.created_at, self.language, self.description, self.open_issues, list(map(lambda c: c.nickname,self.contributors))
        )
        return f"{separator}\n{title}\n{separator}\n{details}"