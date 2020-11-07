from octokit import Octokit
import csv, requests, os
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
    commit_messages = []
    number_of_commits = pr_data.json["commits"]
    number_of_changes = pr_data.json["additions"] + pr_data.json["deletions"]
    number_of_files_changed = pr_data.json["changed_files"]
    for commit_object in commits.json:
        commit_messages.append(commit_object['commit']['message'])
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
