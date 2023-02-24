from __future__ import annotations
from typing import List
import json

class Issue:
    def __init__(self, 
                 number: int,  
                 user: str,
                 title: str,
                 body: str,
                 labels: List[str],
                 state: str,
                 assignees: List[str],
                 created_at: str,
                 updated_at: str,
                 closed_at: str) -> None:
        self.number = number
        self.user = user
        self.title = title
        self.body = body
        self.labels = labels
        self.state = state
        self.assignees = assignees
        self.created_at = created_at
        self.updated_at = updated_at
        self.closed_at = closed_at
        
        
    @staticmethod
    def create(issue_json: json) -> Issue:
        number = issue_json['number']
        user = issue_json['user']['login']
        title = issue_json['title']
        body = issue_json['body']
        labels = [label['name'] for label in issue_json['labels']]
        state = issue_json['state']
        assignees = [assignee['login'] for assignee in issue_json['assignees']]
        created_at = issue_json['created_at']
        updated_at = issue_json['updated_at']
        closed_at = issue_json['closed_at']
        return Issue(number,
                     user,
                     title,
                     body,
                     labels,
                     state,
                     assignees,
                     created_at,
                     updated_at,
                     closed_at)
        
    @staticmethod
    def create_issues(issues_json: json) -> List[Issue]:
        return [Issue.create(i) for i in issues_json]