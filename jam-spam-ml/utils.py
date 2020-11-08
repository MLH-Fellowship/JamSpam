from octokit import Octokit
import csv, requests, os, sys
from dotenv import load_dotenv

load_dotenv()


def fetch_data_from_github(pull_request: str) -> dict:
    """Takes a pull-request link and returns a feature array for it

    Parameters
    ----------
    pull_request : str
        The link to the pull request on GitHub

    Returns
    -------
    dict
        The feature dict contains parameters fetched from GitHub required to build training model
    """

    pr_attrs = pull_request.split('/')
    # ['https:', '', 'github.com', 'owner', 'repo', 'pull', 'pull_number']
    octokit = Octokit(auth='token', token=os.getenv("TOKEN"))
    # octokit = Octokit()
    pr_data = octokit.pulls.get(owner=pr_attrs[3],
                                repo=pr_attrs[4],
                                pull_number=int(pr_attrs[6]))
    commits = octokit.pulls.list_commits(owner=pr_attrs[3],
                                        repo=pr_attrs[4],
                                        pull_number=int(pr_attrs[6]))
    try:
        commit_messages = ''
        number_of_commits = pr_data.json["commits"]
        number_of_changes = pr_data.json["additions"] + pr_data.json["deletions"]
        number_of_files_changed = pr_data.json["changed_files"]
        for commit_object in commits.json:
            commit_messages += f'{commit_object["commit"]["message"]} '
        diffs = requests.get(pr_data.json["diff_url"]).text
        number_of_docs_changed = get_docs_changed(diffs)

        return {
            "url": pull_request,
            "title": pr_data.json["title"],
            "body": pr_data.json["body"],
            "diffs": diffs,
            "commit_messages": commit_messages,
            "files_changed": number_of_files_changed,
            "docs_changed": number_of_docs_changed,
            "commits": number_of_commits,
            "changes": number_of_changes
        }
    except:
        print(f"Error in  {pull_request}: ", pr_data.json)

def get_docs_changed(diffs: str) -> int:
    """Processes diffs from a Pull Request to extract number of doc-type files changed in the PR

    Parameters
    ----------
    diffs : str
        A string denoting the diffs in the PR

    Returns
    -------
    int
        number of files of documentation type that have been changed in the PR

    """

    # Documentation-type file extensions
    exts = ['md', 'txt', 'rst', '']
    diff_set = [
        line for line in diffs.split('\n')
        if line.startswith('diff') and line.split('.')[-1] in exts
    ]
    return len(diff_set)


def read_csv(file_path: str) -> list:
    """Takes a filepath returns a data with list of PR links from CSV data file

    Parameters
    ----------
    file_path : str
        The path to the CSV file on your system that contains the list of PR links

    Returns
    -------
    list
        List of strings of PR Links
    """

    with open(file=file_path) as f:
        reader = csv.reader(f)
        data = [row[0] for row in reader]
        return data

def import_local_dataset() -> (list, list):

    spam_data = ham_data = []

    maxInt = sys.maxsize

    while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)

    with open("data/spam_fetch.csv", "r", newline='', encoding='utf8') as file:
        read = csv.reader(file)
        spam_data = [row for row in read]

    with open("data/ham_fetch.csv", "r", newline='', encoding='utf8') as file:
        read = csv.reader(file)
        ham_data = [row for row in read]

    return spam_data, ham_data


def fetch_from_remote(updateLocal: bool) -> (list, list):

    # import URLs list
    SPAM_PRS = read_csv("data/spam.csv")
    HAM_PRS = read_csv("data/ham.csv")

    spam_feature_array = [
        fetch_data_from_github(pr_link) for pr_link in SPAM_PRS[0:2]
    ]
    ham_feature_array = [
        fetch_data_from_github(pr_link) for pr_link in HAM_PRS[0:2]
    ]

    spam_list_features = [[
        pr_feature["url"], pr_feature["title"], pr_feature["body"], pr_feature["diffs"],
        pr_feature["commit_messages"], pr_feature["files_changed"], pr_feature["docs_changed"],
        pr_feature["commits"], pr_feature["changes"]
    ] for pr_feature in spam_feature_array]

    ham_list_features = [[
        pr_feature["url"], pr_feature["title"], pr_feature["body"], pr_feature["diffs"],
        pr_feature["commit_messages"], pr_feature["files_changed"], pr_feature["docs_changed"],
        pr_feature["commits"], pr_feature["changes"]
    ] for pr_feature in ham_feature_array]

    if updateLocal is True:
        with open("data/spam_fetch.csv", "w", newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerows(spam_list_features)

        with open("data/ham_fetch.csv", "w", newline='', encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerows(ham_list_features)

    return spam_feature_array, ham_feature_array
