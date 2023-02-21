import json

class Issue:
    def __init__(self, issue_events, assignees, comments) -> None:
        self.issue_events = issue_events
        self.assignees = assignees
        self.comments = comments
        
    @staticmethod
    def extract_issue(issue_dict):
        pass