from utils import read_csv, fetch_data_from_github
from spam_keywords import get_spam_keywords


def main():
    # import URLs list
    SPAM_PRS = read_csv("data/spam.csv")
    HAM_PRS = read_csv("data/ham.csv")

    spam_feature_array = [
        fetch_data_from_github(pr_link) for pr_link in SPAM_PRS[10:15]
    ]
    ham_feature_array = [
        fetch_data_from_github(pr_link) for pr_link in HAM_PRS[10:15]
    ]

    spam_text_corpus = [[
        pr_feature["title"], pr_feature["body"], pr_feature["diffs"],
        pr_feature["commit_messages"]
    ] for pr_feature in spam_feature_array]

    ham_text_corpus = [[
        pr_feature["title"], pr_feature["body"], pr_feature["diffs"],
        pr_feature["commit_messages"]
    ] for pr_feature in ham_feature_array]

    spam_keywords = get_spam_keywords(spam_text_corpus, ham_text_corpus)

    # print(spam_feature_array, ham_feature_array, sep="\n")

    # TODO: populate features into an np-array to be passed into TF-Model


if __name__ == "__main__":
    main()
