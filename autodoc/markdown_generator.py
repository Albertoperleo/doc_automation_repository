from typing import List
import os

from autodoc import Issue
from autodoc.models import Repository


def to_markdown(repository: Repository, workspace: dict, templates_path: str) -> None:

    if not os.path.exists(templates_path) or not os.path.isdir(templates_path):
        raise 'Could not find templates directory!'

    task_template = read_file(templates_path + 'task_template.txt')
    tasks = []
    for issue in repository.issues:
        tasks.append(fill_task(issue, workspace, task_template))
    print(tasks)
    # filled_template = fill_base(repository, empty_template)
    # file_path = template_name.replace('.txt', '.md')
    # save_file(templates_path + file_path, filled_template)

def fill_task(issue: Issue, workspace: dict, task_template: str) -> str:
    #TODO
    print(issue.user)
    print(workspace.get(issue.user))
    return ''

def fill_base(repository: Repository, empty_template: list) -> List[str]:
    """Fills the given template

    Args:
        repository (Repository): repository with data
        empty_template (list): template to fill

    Returns:
        List[str]: lines of file filled
    """
    filled_template = []
    for line in empty_template:
        while (left_brace_index := line.rfind('{')) != -1 and (right_brace_index := line.rfind('}')) != -1:
            pointer = line[left_brace_index + 1: right_brace_index]
            value = getattr(repository, pointer) if hasattr(repository, pointer) else 'not found'
            # if type(value) != str:
            filled_template.append(line := line.replace('{' + pointer + '}', str(value)))
    return filled_template


def read_file(path: str) -> List[str]:
    """
    Reads the file at the given path and returns the lines of the file as a list of strings.

    :param path: The path to the file to read.
    :return: The lines of the file as a list of strings.
    """
    with open(path, "r") as file:
        empty_template = file.readlines()
    return empty_template


def save_file(path: str, data: list) -> None:
    """
    Saves the given data to the given path.

    :param path: The path to the file to save the data to.
    :param data: The data to save to the file.
    :return: None
    """
    with open(path, "w") as file:
        file.writelines(data)
