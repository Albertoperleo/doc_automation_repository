from autodoc import *
from clockipy.Clockipy import Clockipy


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
    #repository_url = input('Enter the repository URL:\n')
    clockipy_ws = input("Enter the clockify's workspace name:\n")
    clockify_url = 'https://api.clockify.me/api/v1/workspaces/'
    data_path = create_directories()
    # Api-Key Configuration
    with open(r".\autodoc\token.txt", "r") as token_file:
        line = token_file.readline()
        api_keys = line.split(";")
    try:
     #   octokit = Octokit(api_keys[0])
        clockipy = Clockipy(api_keys[1])

        # repository = get_repository(octokit, repository_url)
        # print(repository)

        clockInfo = get_clockify(clockipy, clockify_url, clockipy_ws)
        # print(clockInfo)

        #templates_path = os.getcwd() + '/templates/'
        #template_name = 'repository_test_template.txt'
        #to_markdown(repository, templates_path, template_name)

    except (ValueError, ConnectionError) as error:
        print(error)
    input('Press Enter to exit...')


if __name__ == '__main__':
    main()
