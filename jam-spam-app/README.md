# jam-spam-app

> A GitHub App built with [Probot](https://github.com/probot/probot) to jam the spam PRs on your repo and keep maintainers stress-free (even in Hacktober 🎃)

## Setup

```sh
# Install dependencies
npm install

# Run the bot
npm start
```

## Docker

```sh
# 1. Build container
docker build -t jam-spam-app .

# 2. Start container
docker run -e APP_ID=<app-id> -e PRIVATE_KEY=<pem-value> jam-spam-app
```
