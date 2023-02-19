from lib.octokitpy.octokit import Octokit
import AutoDoc
import os

def create_directories() -> str:
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
    repository = input('Enter the repository URL:\n')
    path = create_directories()
    # Api-Key Configuration
    token = open(r"..\auth\token.txt", "r")
    api_key = token.read()
    token.close()
    try:
        octokit = Octokit(api_key)
        auto_doc = AutoDoc(repository, None, octokit, token, )
    except Exception as error:
        print(error)
    os.system("PAUSE")

if __name__ == '__main__':
    main()
