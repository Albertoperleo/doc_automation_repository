from __future__ import annotations
from typing import List

from autodoc.models.Task import Task


class Report:
    def __init__(self, user_id: str, username: str, tasks: List[Task]) -> Report:
        self.user_id = user_id
        self.username = username
        self.tasks = tasks
