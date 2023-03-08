from __future__ import annotations

import json


class Task:
    def __init__(self, user_id, task_id, description, start_date, end_date, duration) -> Task:
        self.user_id = user_id
        self.task_id = task_id
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration

    @staticmethod
    def create(task_json: json):
        return Task(task_json['userId'], task_json['id'], task_json['description'],
                    task_json['timeInterval']['start'], task_json['timeInterval']['end'],
                    task_json['timeInterval']['duration'])
