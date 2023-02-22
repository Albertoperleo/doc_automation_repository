from autodoc import *
from octokit import Octokit
import os

def create_directories() -> str:
    """Check if data directory exists. If not, will create:
        ./data/
        | - generated/
        | - retrieved/

    Returns:
        str: path to data directory
    """
    data_path = os.path.join(os.getcwd(), "data")
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    generated_path = os.path.join(data_path, "generated")
    if not os.path.isdir(generated_path):
        os.makedirs(generated_path)
    retrieved_path = os.path.join(data_path, "retrieved")
    if not os.path.isdir(retrieved_path):
        os.makedirs(retrieved_path)
    return data_path

def main():
    repository_url = input('Enter the repository URL:\n')
    path = create_directories()
    # Api-Key Configuration
    with open(r".\autodoc\token.txt", "r") as token_file:
        api_key = token_file.read()
    try:
        octokit = Octokit(api_key)
        repository = get_repository(repository_url, octokit)
    except (ValueError, ConnectionError) as error:
        print(error)
    input('Press Enter to exit...')

if __name__ == '__main__':
    main()
