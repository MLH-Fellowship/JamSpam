# jam-spam-ml

> A Machine Learning powered GitHub App built with [Probot](https://github.com/probot/probot) to jam the spam PRs on your repo and keep maintainers stress-free (even in Hacktober 🎃)

## Setup

```sh
# Setting up virtual environment for local development
virtualenv venv

# Activate environment
source venv/Scripts/activate

# Install Dependencies
pip install -r requirements.txt

# Start training
python train.py

# Find the spam keywords
python spam_keywords.py
```
