from typing import List
import os
from autodoc.models import Repository


def to_markdown(repository: Repository, templates_path: str, template_name: str) -> None:
    """Converts files from .txt to .md

    Args:
        repository (Repository): repository with data
        templates_path (str): link to templates dir
        template_name (str): template selected
    """
    if not os.path.exists(templates_path) or not os.path.isdir(templates_path):
        raise 'Could not find templates directory!'
    if not os.path.exists(templates_path + template_name):
        raise f"Could not find template '{template_name}' in templates directory!"
    empty_template = read_file(templates_path + template_name)
    filled_template = fill_base(repository, empty_template)
    file_path = template_name.replace('.txt', '.md')
    save_file(templates_path + file_path, filled_template)


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
    """Reads lines from a given file by path

    Args:
        path (str): path to file

    Returns:
        List[str]: lines from file
    """
    with open(path, "r") as file:
        empty_template = file.readlines()
    return empty_template


def save_file(path: str, data: list) -> None:
    """Saves the given lines into a file

    Args:
        path (str): path to dst file
        data (list): lines to save
    """
    with open(path, "w") as file:
        file.writelines(data)
