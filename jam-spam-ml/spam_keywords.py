from multi_rake import Rake

text_spam = ''  #SPAM TEXT BLOB
text_ham = ''  #HAM TEXT BLOB
spam_feature_array = [
    [
        'add 3 dot',
        'Describe what this patch does to fix the issue.\r\n\r\nLink to any relevant issues or pull requests.\r\n\r\n<!--\r\nCommit checklist:\r\n\r\n* add tests that fail without the patch\r\n* ensure all tests pass with ``pytest``\r\n* add documentation to the relevant docstrings or pages\r\n* add ``versionadded`` or ``versionchanged`` directives to relevant docstrings\r\n* add a changelog entry if this patch changes code\r\n\r\nTests, coverage, and docs will be run automatically when you submit the pull\r\nrequest, but running them yourself can save time.\r\n-->\r\n',
        'diff --git a/.gitattributes b/.gitattributes\nindex 6f9ff673b..a3c08384f 100644\n--- a/.gitattributes\n+++ b/.gitattributes\n@@ -1 +1,2 @@\n CHANGES.rst merge=union\n+... \n',
        ['add 3 dot']
    ],
    [
        'trying to add some more information :-)',
        'Describe what this patch does to fix the issue.\r\n\r\nLink to any relevant issues or pull requests.\r\n\r\n<!--\r\nCommit checklist:\r\n\r\n* add tests that fail without the patch\r\n* ensure all tests pass with ``pytest``\r\n* add documentation to the relevant docstrings or pages\r\n* add ``versionadded`` or ``versionchanged`` directives to relevant docstrings\r\n* add a changelog entry if this patch changes code\r\n\r\nTests, coverage, and docs will be run automatically when you submit the pull\r\nrequest, but running them yourself can save time.\r\n-->\r\n',
        "diff --git a/README.rst b/README.rst\nindex 22e82c478..4f7635f7a 100644\n--- a/README.rst\n+++ b/README.rst\n@@ -2,17 +2,30 @@ Flask\n =====\n \n Flask is a lightweight `WSGI`_ web application framework. It is designed\n-to make getting started quick and easy, with the ability to scale up to\n-complex applications. It began as a simple wrapper around `Werkzeug`_\n+to make getting started quick and easy, also known as one drop at a time,\n+with the ability to scale up to complex applications.\n+It began as a simple wrapper around `Werkzeug`_\n and `Jinja`_ and has become one of the most popular Python web\n application frameworks.\n \n+Using templates you are able to set a basic layout for your pages and\n+mention which element will change. This way you can define your header\n+once and keep it consistent over all the pages of your website, and if you \n+need to change your header, you will only have to update it in one place.\n+\n+Flask uses a specific syntax to create links from a page to another.\n+This is fact generates the link dynamically according to the decorator\n+set to the function linked to. In addition it takes care of where the application is deployed.\n+\n+\n Flask offers suggestions, but doesn't enforce any dependencies or\n project layout. It is up to the developer to choose the tools and\n libraries they want to use. There are many extensions provided by the\n community that make adding new functionality easy.\n \n \n+\n+\n Installing\n ----------\n \n",
        ['Update README.rst']
    ]
]
ham_feature_array = [
    [
        'add 3 dot',
        'Describe what this patch does to fix the issue.\r\n\r\nLink to any relevant issues or pull requests.\r\n\r\n<!--\r\nCommit checklist:\r\n\r\n* add tests that fail without the patch\r\n* ensure all tests pass with ``pytest``\r\n* add documentation to the relevant docstrings or pages\r\n* add ``versionadded`` or ``versionchanged`` directives to relevant docstrings\r\n* add a changelog entry if this patch changes code\r\n\r\nTests, coverage, and docs will be run automatically when you submit the pull\r\nrequest, but running them yourself can save time.\r\n-->\r\n',
        'diff --git a/.gitattributes b/.gitattributes\nindex 6f9ff673b..a3c08384f 100644\n--- a/.gitattributes\n+++ b/.gitattributes\n@@ -1 +1,2 @@\n CHANGES.rst merge=union\n+... \n',
        ['add 3 dot']
    ],
    [
        'trying to add some more information :-)',
        'Describe what this patch does to fix the issue.\r\n\r\nLink to any relevant issues or pull requests.\r\n\r\n<!--\r\nCommit checklist:\r\n\r\n* add tests that fail without the patch\r\n* ensure all tests pass with ``pytest``\r\n* add documentation to the relevant docstrings or pages\r\n* add ``versionadded`` or ``versionchanged`` directives to relevant docstrings\r\n* add a changelog entry if this patch changes code\r\n\r\nTests, coverage, and docs will be run automatically when you submit the pull\r\nrequest, but running them yourself can save time.\r\n-->\r\n',
        "diff --git a/README.rst b/README.rst\nindex 22e82c478..4f7635f7a 100644\n--- a/README.rst\n+++ b/README.rst\n@@ -2,17 +2,30 @@ Flask\n =====\n \n Flask is a lightweight `WSGI`_ web application framework. It is designed\n-to make getting started quick and easy, with the ability to scale up to\n-complex applications. It began as a simple wrapper around `Werkzeug`_\n+to make getting started quick and easy, also known as one drop at a time,\n+with the ability to scale up to complex applications.\n+It began as a simple wrapper around `Werkzeug`_\n and `Jinja`_ and has become one of the most popular Python web\n application frameworks.\n \n+Using templates you are able to set a basic layout for your pages and\n+mention which element will change. This way you can define your header\n+once and keep it consistent over all the pages of your website, and if you \n+need to change your header, you will only have to update it in one place.\n+\n+Flask uses a specific syntax to create links from a page to another.\n+This is fact generates the link dynamically according to the decorator\n+set to the function linked to. In addition it takes care of where the application is deployed.\n+\n+\n Flask offers suggestions, but doesn't enforce any dependencies or\n project layout. It is up to the developer to choose the tools and\n libraries they want to use. There are many extensions provided by the\n community that make adding new functionality easy.\n \n \n+\n+\n Installing\n ----------\n \n",
        ['Update README.rst']
    ]
]


def get_keywords(pr):
    text_keywords = ''

    for item in pr:
        if type(item) is str:
            text_keywords += item + " "
        elif type(item) is list:
            for item2 in item:
                text_keywords += item2 + " "

    return text_keywords

def get_spam_keywords(spam_features, ham_features):
    #POPULATE THE SPAM AND HAM TEXT BLOBS
    text_spam = ''
    text_ham = ''

    for pr in spam_features:
        text_spam += get_keywords(pr)

    for pr in ham_features:
        text_ham += get_keywords(pr)

    #INITIALISE RAKE FOR POPULAR WORDS
    rake = Rake(max_words=1, min_freq=2)

    #EXTRACT POPULAR KEYWORDS FOR SPAM AND HAM
    keywords_spam = rake.apply(text_spam)
    keywords_ham = rake.apply(text_ham)

    print(keywords_ham)
    print(keywords_spam)

    spam = [spam_keyword[0] for spam_keyword in keywords_spam[:30]]
    ham = [ham_keyword[0] for ham_keyword in keywords_ham[:30]]

    #STORE TOP 30 SPAM AND HAM KEYWORDS
    # for i in range(0, 30):
    #     spam.append(keywords_spam[i][0])
    #     ham.append(keywords_ham[i][0])

    # GENERATE KEYWORDS PRESENT IN SPAM WHICH ARE NOT PRESENT IN HAM
    spam_final = []
    for word in spam:
        if word not in ham:
            spam_final.append(word)

    print(spam_final)
    return spam_final
