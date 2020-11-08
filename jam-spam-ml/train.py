from utils import read_csv, fetch_data_from_github, import_local_dataset, fetch_from_remote
from spam_keywords import get_spam_keywords


def main():

    spam_data, ham_data = import_local_dataset()
    # csv_row -> [url, title, body, diffs, commit_messages, files_changed, docs_changed, commits, changes]

    spam_text_corpus = [
        [row[1], row[2], row[4]]  # [title, body, commit_messages]
        for row in spam_data
    ]
    ham_text_corpus = [
        [row[1], row[2], row[4]]  # [title, body, commit_messages]
        for row in ham_data
    ]

    ## TO FETCH FROM REMOTE UNCOMMENT THE BLOCK BELOW
    #
    # spam_feature_array, ham_feature_array = fetch_from_remote(updateLocal=False)
    # spam_text_corpus = [[
    #     pr_feature["title"], pr_feature["body"], pr_feature["commit_messages"]
    # ] for pr_feature in spam_feature_array if type(pr_feature) is dict]
    # ham_text_corpus = [[
    #     pr_feature["title"], pr_feature["body"], pr_feature["commit_messages"]
    # ] for pr_feature in ham_feature_array if type(pr_feature) is dict]

    spam_keywords = get_spam_keywords(spam_text_corpus, ham_text_corpus)

    print(spam_keywords)

    # TODO: populate features into an np-array to be passed into TF-Model


if __name__ == "__main__":
    main()
