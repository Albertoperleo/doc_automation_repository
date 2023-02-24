from __future__ import annotations
from typing import List
import json
from autodoc.models import Contributor


class Commit:
    def __init__(self, 
                 sha: str,
                 author: str,
                 date: str,
                 message: str) -> None:
        self.sha = sha
        self.author = author
        self.date = date
        self.message = message
        
    @staticmethod
    def create(commit_json: json) -> Commit:
        sha = commit_json['sha']
        author = commit_json['author']['login']
        date = commit_json['commit']['author']['date']
        message = commit_json['commit']['message']
        return Commit(sha, author, date, message)
    
    @staticmethod
    def createCommits(commits_json: json) -> List[Commit]:
        return [Commit.create(c) for c in commits_json]