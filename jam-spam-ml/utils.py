from octokit import Octokit
import csv, requests


def fetch_data_from_github(pull_request: str) -> list:
    """Takes a pull-request link and returns a feature array for it

    Parameters
    ----------
    pull_request : str
        The link to the pull request on GitHub
    
    Returns
    -------
    list
        The feature array contains four parameters and looks like [pr_title, pr_body, pr_diffs, pr_commits]
        pr_title: str -> title of the PR
        pr_body: str -> body of the PR
        pr_diffs: str -> aggregated diffs of the PR
        pr_commits: list -> list of commit messages: str
    """
    
    pr_attrs = pull_request.split('/')
    # ['https:', '', 'github.com', 'owner', 'repo', 'pull', 'pull_number']
    pr_data = Octokit().pulls.get(
        owner=pr_attrs[3], repo=pr_attrs[4], pull_number=int(pr_attrs[6]))
    commits = requests.get(pr_data.json["commits_url"]).json()
    commit_messages = []
    for commit_object in commits:
        commit_messages.append(commit_object['commit']['message'])
    diffs = requests.get(pr_data.json["diff_url"]).text
    return [pr_data.json["title"], pr_data.json["body"], diffs, commit_messages]

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