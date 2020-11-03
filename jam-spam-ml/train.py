from utils import read_csv, fetch_data_from_github

def main():
    # import URLs list
    SPAM_PRS = read_csv("data/sample.csv")
    HAM_PRS = read_csv("data/sample.csv")

    spam_feature_array = [fetch_data_from_github(pr_link) for pr_link in SPAM_PRS]
    ham_feature_array = [fetch_data_from_github(pr_link) for pr_link in HAM_PRS]
    
    print(spam_feature_array, ham_feature_array)

    # TODO: populate features into an np-array to be passed into TF-Model

if __name__ == "__main__":
    main()
